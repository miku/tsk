#!/usr/bin/env python
# coding: utf-8

"""
siskin is a set of tasks for library metadata management.
~~~~~~
"""

try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(name='siskin',
      version='0.0.28',
      description='Various sources and workflows.',
      url='https://github.com/miku/siskin',
      author='Martin Czygan',
      author_email='martin.czygan@gmail.com',
      packages=[
        'siskin',
        'siskin.sources',
        'siskin.workflows'
      ],
      package_dir={'siskin': 'siskin'},
      # adjust the globs here (http://stackoverflow.com/a/3712682/89391)
      package_data={'siskin': ['assets/*.xsl',
                               'assets/*.php',
                               'assets/*.conf',
                               'assets/*.txt',
                               'assets/ambience/*']},
      scripts=[
        'bin/taskcat',
        'bin/taskdo',
        'bin/taskfast',
        'bin/taskhome',
        'bin/taskindex-delete',
        'bin/taskless',
        'bin/taskls',
        'bin/taskman',
        'bin/tasknames',
        'bin/taskoutput',
        'bin/taskredo',
        'bin/taskrm',
        'bin/tasktree',
        'bin/taskversion',
        'bin/taskwc',
      ],
      install_requires=[
        'BeautifulSoup==3.2.1',
        'MySQL-python==1.2.5',
        'argparse==1.2.1',
        'astroid==1.1.1',
        'colorama==0.2.7',
        'decorator==3.4.0',
        'elasticsearch==1.0.0',
        'gluish==0.1.58',
        'gspread==0.2.1',
        'jsonpath-rw==1.3.0',
        'logilab-common==0.61.0',
        'luigi==1.0.16',
        'lxml==3.3.5',
        'marcx==0.1.15',
        'nose==1.3.3',
        'numpy==1.8.1',
        'openpyxl==1.8.6',
        'pandas==0.14.0',
        'ply==3.4',
        'prettytable==0.7.2',
        'pyisbn==1.0.0',
        'pylint==1.2.1',
        'pymarc==3.0.1',
        'python-dateutil==2.2',
        'pytz==2014.4',
        'requests==2.3.0',
        'six==1.6.1',
        'sqlitebck==1.2.1',
        'urllib3==1.8.2',
        'wsgiref==0.1.2',
      ],
)
