# coding: utf-8

from gluish.benchmark import timed
from gluish.common import Executable
from gluish.intervals import weekly
from gluish.parameter import ClosestDateParameter
from gluish.utils import shellout
from gluish.format import TSV
from siskin.sources.crossref import CrossrefIntermediateSchema, CrossrefUniqISSNList
from siskin.sources.degruyter import DegruyterIntermediateSchema, DegruyterISSNList
from siskin.sources.doaj import DOAJIntermediateSchema, DOAJISSNList
from siskin.sources.gbi import GBIIntermediateSchema, GBIISSNList
from siskin.sources.holdings import HoldingsFile
from siskin.sources.jstor import JstorIntermediateSchema, JstorISSNList
from siskin.task import DefaultTask
import datetime
import itertools
import luigi
import tempfile

class AITask(DefaultTask):
    TAG = 'ai'

    def closest(self):
        return weekly(self.date)

class DownloadFile(AITask):
    """ Download a file. TODO(miku): move this out here. """

    date = luigi.DateParameter(default=datetime.date.today())
    url = luigi.Parameter()

    @timed
    def run(self):
        output = shellout("""curl -L --fail "{url}" > {output}""", url=self.url)
        luigi.File(output).move(self.output().path)

    def output(self):
        return luigi.LocalTarget(path=self.path(ext='file', digest=True))

class DownloadAndUnzipFile(AITask):
    """ Download a file and unzip it. TODO(miku): move this out here. """
    date = luigi.DateParameter(default=datetime.date.today())
    url = luigi.Parameter()

    @timed
    def run(self):
        output = shellout("""curl -L --fail "{url}" > {output}""", url=self.url)
        output = shellout("""unzip -qq -p {input} > {output}""", input=output)
        luigi.File(output).move(self.output().path)

    def output(self):
        return luigi.LocalTarget(path=self.path(ext='file', digest=True))

class AIISSNStats(AITask):
    """ Match ISSN lists. """
    date = ClosestDateParameter(default=datetime.date.today())

    def requires(self):
        return {
            'crossref': CrossrefUniqISSNList(date=self.date),
            'degruyter': DegruyterISSNList(date=self.date),
            'doaj': DOAJISSNList(date=self.date),
            'gbi': GBIISSNList(date=self.date),
            'jstor': JstorISSNList(date=self.date)
        }

    @timed
    def run(self):
        def loadset(target):
            s = set()
            with target.open() as handle:
                for row in handle.iter_tsv(cols=('issn',)):
                    s.add(row.issn)
            return s

        with self.output().open('w') as output:
            for k1, k2 in itertools.combinations(self.input().keys(), 2):
                s1 = loadset(self.input().get(k1))
                s2 = loadset(self.input().get(k2))
                output.write_tsv(k1, k2, len(s1), len(s2), len(s1.intersection(s2)))

    def output(self):
        return luigi.LocalTarget(path=self.path(), format=TSV)

class AIISSNOverlaps(AITask):
    """ Match ISSN lists. """
    date = ClosestDateParameter(default=datetime.date.today())

    def requires(self):
        return {
            'crossref': CrossrefUniqISSNList(date=self.date),
            'degruyter': DegruyterISSNList(date=self.date),
            'doaj': DOAJISSNList(date=self.date),
            'gbi': GBIISSNList(date=self.date),
            'jstor': JstorISSNList(date=self.date)
        }

    @timed
    def run(self):
        def loadset(target):
            s = set()
            with target.open() as handle:
                for row in handle.iter_tsv(cols=('issn',)):
                    s.add(row.issn)
            return s

        with self.output().open('w') as output:
            for k1, k2 in itertools.combinations(self.input().keys(), 2):
                s1 = loadset(self.input().get(k1))
                s2 = loadset(self.input().get(k2))
                for issn in sorted(s1.intersection(s2)):
                    output.write_tsv(k1, k2, issn)

    def output(self):
        return luigi.LocalTarget(path=self.path(), format=TSV)

class AIIntermediateSchema(AITask):
    """ Create an intermediate schema record from all AI sources. """

    date = ClosestDateParameter(default=datetime.date.today())

    def requires(self):
        return [CrossrefIntermediateSchema(date=self.date),
                DegruyterIntermediateSchema(date=self.date),
                DOAJIntermediateSchema(date=self.date),
                GBIIntermediateSchema(date=self.date),
                JstorIntermediateSchema(date=self.date)]

    @timed
    def run(self):
        _, stopover = tempfile.mkstemp(prefix='siskin-')
        for target in self.input():
            shellout("cat {input} >> {output}", input=target.path, output=stopover)
        luigi.File(stopover).move(self.output().path)

    def output(self):
        return luigi.LocalTarget(path=self.path(ext='ldj'))

class AIExport(AITask):
    """ Create a SOLR-importable file. """

    date = ClosestDateParameter(default=datetime.date.today())

    def requires(self):
        return {
            'crossref': CrossrefIntermediateSchema(date=self.date),
            'degruyter': DegruyterIntermediateSchema(date=self.date),
            'doaj': DOAJIntermediateSchema(date=self.date),
            'gbi': GBIIntermediateSchema(date=self.date),
            'jstor' : JstorIntermediateSchema(date=self.date),

            'DE-105': DownloadAndUnzipFile(date=self.date, url='https://goo.gl/Gq199T'),
            'DE-14': DownloadAndUnzipFile(date=self.date, url='https://goo.gl/Tz3vbk'),
            'DE-15': DownloadAndUnzipFile(date=self.date, url='https://goo.gl/inyKLr'),
            'DE-Bn3': DownloadAndUnzipFile(date=self.date, url='https://goo.gl/oq8LDD'),
            'DE-Ch1': DownloadAndUnzipFile(date=self.date, url='https://goo.gl/uJwoUf'),
            'DE-Gla1': DownloadAndUnzipFile(date=self.date, url='https://goo.gl/6506Dz'),
            'DE-Zi4': DownloadAndUnzipFile(date=self.date, url='https://goo.gl/Ld0LCw'),
            'DE-J59': DownloadAndUnzipFile(date=self.date, url='https://goo.gl/44xEbF'),

            'DE-15-FID': DownloadFile(date=self.date, url='https://goo.gl/8P6JtB'),

            'app': Executable(name='span-export', message='http://git.io/vI8NV'),
        }

    @timed
    def run(self):
        """
        TODO(miku): Move source/ISIL matrix and filter method out of here.
        """
        _, stopover = tempfile.mkstemp(prefix='siskin-')

        # DE-15 and DE-14 get DOAJ
        shellout("""span-export -any DE-15 -any DE-14 {input} | gzip >> {output}""",
                 input=self.input().get('doaj').path, output=stopover)

        # JSTOR detached from all for now, cf. #5472
        shellout("""span-export {input} | gzip >> {output}""", input=self.input().get('jstor').path, output=stopover)

        # prepare holding file -f arguments for span-export
        hkeys = ('DE-105', 'DE-14', 'DE-15', 'DE-Bn3', 'DE-Ch1', 'DE-Gla1', 'DE-Zi4', 'DE-J59')
        files = " ".join(["-f %s:%s" % (k, v.path) for k, v in self.input().items() if k in hkeys])

        # prepare issn list -l arguments for span-export
        fkeys = ('DE-15-FID',)
        lists = " ".join(["-l %s:%s" % (k, v.path) for k, v in self.input().items() if k in fkeys])

        # apply both filters on following sources
        for source in ('crossref', 'degruyter', 'gbi'):
            shellout("span-export -skip {files} {lists} {input} | gzip >> {output}", files=files,
                     lists=lists, input=self.input().get(source).path, output=stopover)

        luigi.File(stopover).move(self.output().path)

    def output(self):
        return luigi.LocalTarget(path=self.path(ext='ldj.gz'))
