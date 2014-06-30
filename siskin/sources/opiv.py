# coding: utf-8
# pylint: disable=F0401,C0111,W0232,E1101,E1103,C0301

"""
OPIV.

Configuration keys:

[opiv]

src = [user@server:[port]]/path/to/directory
"""

from gluish.common import Directory
from gluish.format import TSV
from gluish.parameter import ClosestDateParameter
from gluish.path import iterfiles
from gluish.utils import shellout
from siskin.configuration import Config
from siskin.task import DefaultTask
import datetime
import luigi

config = Config.instance()

class OpivTask(DefaultTask):
    TAG = '031'

class OpivSync(OpivTask):
    """ Just copy over the marc files. """
    date = ClosestDateParameter(default=datetime.date.today())

    def requires(self):
        return Directory(path=self.taskdir())

    def run(self):
        shellout("rsync -avz {src} {dst}", src=config.get('opiv', 'src'), dst=self.taskdir())
        with self.output().open('w') as output:
            for path in iterfiles(self.taskdir(), fun=lambda p: '-luigi-tmp-' not in p):
                output.write_tsv(path)

    def output(self):
        return luigi.LocalTarget(path=self.path(), format=TSV)
