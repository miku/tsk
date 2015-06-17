#!/usr/bin/env python

"""
CrossRef is an association of scholarly publishers that develops shared
infrastructure to support more effective scholarly communications.

Our citation-linking network today covers over 68 million journal articles
and other content items (books chapters, data, theses, technical reports)
from thousands of scholarly and professional publishers around the globe.
"""

from gluish.benchmark import timed
from gluish.common import Executable
from gluish.format import TSV
from gluish.intervals import monthly
from gluish.parameter import ClosestDateParameter
from gluish.utils import date_range, shellout
from siskin.task import DefaultTask
from siskin.utils import URLCache, ElasticsearchMixin
import datetime
import elasticsearch
import json
import luigi
import os
import requests
import tempfile
import urllib

class CrossrefTask(DefaultTask):
    """
    Crossref related tasks. See: http://www.crossref.org/
    """
    TAG = 'crossref'

    def closest(self):
        """ Update frequency. """
        return monthly(date=self.date)

class CrossrefHarvestChunk(CrossrefTask):
    """
    API docs can be found under: http://api.crossref.org/

    The output file is line delimited JSON, just the concatenated responses.
    """
    begin = luigi.DateParameter()
    end = luigi.DateParameter()
    filter = luigi.Parameter(default='deposit', description='index, deposit, update')

    rows = luigi.IntParameter(default=1000, significant=False)
    max_retries = luigi.IntParameter(default=10, significant=False)

    @timed
    def run(self):
        cache = URLCache(directory=os.path.join(tempfile.gettempdir(), '.urlcache'))
        adapter = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
        cache.sess.mount('http://', adapter)

        filter = "from-{self.filter}-date:{self.begin},until-{self.filter}-date:{self.end}".format(self=self)
        rows, offset = self.rows, 0

        with self.output().open('w') as output:
            while True:
                params = {"rows": rows, "offset": offset, "filter": filter}
                url = 'http://api.crossref.org/works?%s' % (urllib.urlencode(params))
                for attempt in range(1, 3):
                    body = cache.get(url)
                    try:
                        content = json.loads(body)
                    except ValueError as err:
                        if attempt == 2:
                            self.logger.debug("URL was %s" % url)
                            self.logger.debug(err)
                            self.logger.debug(body[:100])
                            raise
                        if os.path.exists(cache.get_cache_file(url)):
                            self.logger.debug("trying to recover by removing cached entry")
                            os.remove(cache.get_cache_file(url))
                    else:
                        break
                items = content["message"]["items"]
                self.logger.debug("%s: %s" % (url, len(items)))
                if len(items) == 0:
                    break
                output.write(body + "\n")
                offset += rows

    def output(self):
        return luigi.LocalTarget(path=self.path(ext='ldj'))

class CrossrefHarvest(luigi.WrapperTask, CrossrefTask):
    """
    Harvest everything in incremental steps. Yield the targets sorted by date (ascending).
    """
    begin = luigi.DateParameter(default=datetime.date(2006, 1, 1))
    end = luigi.DateParameter(default=datetime.date.today())
    update = luigi.Parameter(default='months', description='days, weeks or months')

    def requires(self):
        if self.update not in ('days', 'weeks', 'months'):
            raise RuntimeError('update can only be: days, weeks or months')
        dates = date_range(self.begin, self.end, 1, self.update)
        tasks = [CrossrefHarvestChunk(begin=dates[i], end=dates[i + 1])
                 for i in range(len(dates) - 1)]
        return sorted(tasks)

    def output(self):
        return self.input()

class CrossrefItems(CrossrefTask):
    """
    Combine all harvested files into a single LDJ file.
    Flatten and deduplicate. Stub.
    """
    begin = luigi.DateParameter(default=datetime.date(2006, 1, 1))
    date = ClosestDateParameter(default=datetime.date.today())

    def requires(self):
        return CrossrefHarvest(begin=self.begin, end=self.closest())

    @timed
    def run(self):
        """ Extract all items from chunks. """
        with self.output().open('w') as output:
            for target in self.input():
                with target.open() as handle:
                    for line in handle:
                        content = json.loads(line)
                        if not content.get("status") == "ok":
                            raise RuntimeError("invalid response status: %s" % content)
                        items = content["message"]["items"]
                        for item in items:
                            output.write(json.dumps(item))
                            output.write("\n")

    def output(self):
        return luigi.LocalTarget(path=self.path(ext='ldj'))

class CrossrefUniqItems(CrossrefTask):
    """ Compact file, keep only most recent entries. """
    begin = luigi.DateParameter(default=datetime.date(2006, 1, 1))
    date = ClosestDateParameter(default=datetime.date.today())

    def requires(self):
	return {'items': CrossrefItems(begin=self.begin, date=self.date),
		'ldjtab': Executable(name='ldjtab')}

    @timed
    def run(self):
        infile = self.input().get('items').path
        output = shellout("ldjtab -padlength 10 -key DOI {input} > {output}", input=infile)
        linenumbers = shellout("tac {input} | sort -u -k1,1 | cut -f2 | sed 's/^0*//' | sort -n > {output}", input=output)
class CrossrefIntermediateSchema(CrossrefTask):
    """ Convert to intermediate format via span. """

    date = ClosestDateParameter(default=datetime.date.today())

    def requires(self):
       return {'span': Executable(name='span-import', message='http://git.io/vI8NV'),
               'file': CrossrefUniqItems(date=self.date)}

    @timed
    def run(self):
        output = shellout("span-import -i crossref {input} > {output}", input=self.input().get('file').path)
        luigi.File(output).move(self.output().path)

    def output(self):
        return luigi.LocalTarget(path=self.path(ext='ldj'))

class CrossrefISSNList(CrossrefTask):
    """ Just dump a list of all ISSN values. With dups and all. """
    begin = luigi.DateParameter(default=datetime.date(2006, 1, 1))
    date = ClosestDateParameter(default=datetime.date.today())

    def requires(self):
        return CrossrefUniqItems(begin=self.begin, date=self.date)

    @timed
    def run(self):
        output = shellout("jq -r '.ISSN[]' {input} 2> /dev/null > {output}", input=self.input().path)
        luigi.File(output).move(self.output().path)

    def output(self):
        return luigi.LocalTarget(path=self.path(), format=TSV)

class CrossrefUniqISSNList(CrossrefTask):
    """ Just dump a list of all ISSN values. Sorted and uniq. """
    begin = luigi.DateParameter(default=datetime.date(2006, 1, 1))
    date = ClosestDateParameter(default=datetime.date.today())

    def requires(self):
        return CrossrefISSNList(begin=self.begin, date=self.date)

    @timed
    def run(self):
        output = shellout("sort -u {input} > {output}", input=self.input().path)
        luigi.File(output).move(self.output().path)

    def output(self):
        return luigi.LocalTarget(path=self.path(), format=TSV)

class CrossrefIndex(CrossrefTask, ElasticsearchMixin):
    """
    Vanilla records into elasticsearch.
    """

    begin = luigi.DateParameter(default=datetime.date(2006, 1, 1))
    date = ClosestDateParameter(default=datetime.date.today())
    index = luigi.Parameter(default='crossref')

    def requires(self):
        return CrossrefUniqItems(begin=self.begin, date=self.date)

    @timed
    def run(self):
        es = elasticsearch.Elasticsearch()
        shellout("curl -XDELETE {host}:{port}/{index}", host=self.es_host, port=self.es_port, index=self.index)
        mapping = {
            'default': {
                'date_detection': False,
                '_id': {
                    'path': 'URL'
                },
            }
        }
        es.indices.create(index=self.index)
        es.indices.put_mapping(index='bsz', doc_type='default', body=mapping)
        shellout("esbulk -verbose -index {index} {input}", index=self.index, input=self.input().path)
        with self.output().open('w'):
            pass

    def output(self):
        return luigi.LocalTarget(path=self.path())

class CrossrefHarvestGeneric(CrossrefTask):
    """
    Basic harvest of members, funders, etc.
    """
    begin = luigi.DateParameter(default=datetime.date(2006, 1, 1))
    date = ClosestDateParameter(default=datetime.date.today())
    kind = luigi.Parameter(default='members')

    rows = luigi.IntParameter(default=1000, significant=False)
    max_retries = luigi.IntParameter(default=10, significant=False)

    @timed
    def run(self):
        cache = URLCache(directory=os.path.join(tempfile.gettempdir(), '.urlcache'))
        adapter = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
        cache.sess.mount('http://', adapter)

        rows, offset = self.rows, 0

        with self.output().open('w') as output:
            while True:
                params = {"rows": rows, "offset": offset}
                url = 'http://api.crossref.org/%s?%s' % (self.kind, urllib.urlencode(params))
                for attempt in range(1, 3):
                    body = cache.get(url)
                    try:
                        content = json.loads(body)
                    except ValueError as err:
                        if attempt == 2:
                            self.logger.debug("URL was %s" % url)
                            self.logger.debug(err)
                            self.logger.debug(body[:100])
                            raise
                        if os.path.exists(cache.get_cache_file(url)):
                            self.logger.debug("trying to recover by removing cached entry")
                            os.remove(cache.get_cache_file(url))
                    else:
                        break
                items = content["message"]["items"]
                self.logger.debug("%s: %s" % (url, len(items)))
                if len(items) == 0:
                    break
                output.write(body)
                output.write("\n")
                offset += rows

    def output(self):
        return luigi.LocalTarget(path=self.path(ext='ldj'))

class CrossrefGenericItems(CrossrefTask):
    """
    Flatten and deduplicate. Stub.
    """
    begin = luigi.DateParameter(default=datetime.date(2006, 1, 1))
    date = ClosestDateParameter(default=datetime.date.today())
    kind = luigi.Parameter(default='members')

    def requires(self):
        return CrossrefHarvestGeneric(begin=self.begin, date=self.closest(), kind=self.kind)

    @timed
    def run(self):
        with self.output().open('w') as output:
            with self.input().open() as handle:
                for line in handle:
                    content = json.loads(line)
                    if not content.get("status") == "ok":
                        raise RuntimeError("invalid response status")
                    items = content["message"]["items"]
                    for item in items:
                        output.write(json.dumps(item))
                        output.write("\n")

    def output(self):
        return luigi.LocalTarget(path=self.path(ext='ldj'))

class CrossrefCoverage(CrossrefTask):
    """
    Determine coverage of ISSNs. Coverage means, there is at least one
    article with a given ISSN in crossref. Not included in the analysis
    are actual articles and coverage ranges.
    """
    date = ClosestDateParameter(default=datetime.date.today())

    isil = luigi.Parameter(description='isil, for meaningful file names')
    hfile = luigi.Parameter(description='path to a holdings file', significant=False)

    def requires(self):
        return CrossrefUniqISSNList(date=self.date)

    def run(self):
        """
        TODO(miku): This contains things, that would better be factored out in separate tasks.
        """
        titles = {}
        output = shellout("span-gh-dump {hfile} > {output}", hfile=self.hfile)
        with luigi.File(output, format=TSV).open() as handle:
            for row in handle.iter_tsv(cols=('issn', 'title')):
                titles[row.issn] = row.title

        issns_held = set()
        output = shellout("xmlstarlet sel -t -v '//issn' {hfile} | sort | uniq > {output}", hfile=self.hfile)
        with luigi.File(output, format=TSV).open() as handle:
            for row in handle.iter_tsv(cols=('issn',)):
                issns_held.add(row.issn)

        issns_crossref = set()
        with self.input().open() as handle:
            for row in handle.iter_tsv(cols=('issn',)):
                issns_crossref.add(row.issn)

        covered = issns_held.intersection(issns_crossref)

        with self.output().open('w') as output:
            for issn in issns_held:
                if issn in covered:
                    output.write_tsv("COVERED", issn, titles[issn])
                else:
                    output.write_tsv("NOT_COVERED", issn, titles[issn])

    def output(self):
        return luigi.LocalTarget(path=self.path(), format=TSV)

class CrossrefDOIResponses(CrossrefTask):
    """
    For each DOI in crossref, make a GET API request to doi.org and record the
    results.
    """
    pass
