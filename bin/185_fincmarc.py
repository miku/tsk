#!/usr/bin/env python
# coding: utf-8
#
# Copyright 2020 by Leipzig University Library, http://ub.uni-leipzig.de
#                   The Finc Authors, http://finc.info
#                   Martin Czygan, <martin.czygan@uni-leipzig.de>
#                   Robert Schenk, <robert.schenk@uni-leipzig.de>
#
# This file is part of some open source application.
#
# Some open source application is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# Some open source application is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""

Source: DABI
SID: 185
Ticket: #15924
Origin: local file

config:

[dabi]
input = path/to/json

"""


import argparse
import datetime
import json
import sys
import os.path

import marcx
import pymarc
from gluish.intervals import monthly
from siskin.configuration import Config
from gluish.intervals import monthly, weekly
from gluish.parameter import ClosestDateParameter
from siskin.mappings import formats
from siskin.utils import (check_isbn, check_issn, marc_build_field_008, marc_build_field_773g)


def get_field(jsonrecord, field):
    """
    Returns a field or an empty string.
    """
    value = jsonrecord[field]
    if value == None or value == "NULL":
        value = ""
    return str(value)


dabi_to_ddc = {
                "00": "020",
                "1.8": "020",
                "1.8.1": "020",
                "1.8.2": "020",
                "1.8.3": "020",
                "6": "020",
                "6.1": "020",
                "6.2": "020",
                "6.3": "020",
                # shortended for testing 
}


SID = "185"

# 1. Parse arguments

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-i", "--input", dest="inputfilename", help="inputfile")
parser.add_argument("--overwrite", dest="overwrite", help="overwrite existing outputfile", nargs="?", const=True, default=False)
parser.add_argument("--format", dest="outputformat", help="outputformat mrc or xml", default="mrc")
parser.add_argument("--interval", dest="interval", help="interval for update", default="monthly")

args = parser.parse_args()
inputfilename = args.inputfilename
overwrite = args.overwrite
outputformat = args.outputformat
interval = args.interval

if interval != "monthly" and interval != "weekly" and interval != "daily" and interval != "manually":
    sys.exit("Unsupported interval: " + interval)

if interval == "manually" and not overwrite:
    sys.exit("Interval is manually. Use --overwrite to force a new output.")

today = datetime.date.today()
if interval == "monthly":
    date = monthly(today)
elif interval == "weekly":
    date = weekly(today)
elif interval == "daily" or interval == "manually":
    date = today

date = str(date).replace("-", "")
outputfilename = SID + "-output-" + date + "-fincmarc." + outputformat

if os.path.isfile(outputfilename) and not overwrite:
    sys.exit("Outputfile already exists. Use --overwrite.")

if outputformat == "xml":
    outputfile = pymarc.XMLWriter(open(outputfilename, "wb"))
elif outputformat == "mrc":
    outputfile = open(outputfilename, "wb")
else:
    sys.exit("Unsupported format: " + outputformat + " (Use mrc or xml instead).")


# 2. Acquise data

if not inputfilename:    
    config = Config.instance()
    inputfilename = config.get("dabi", "input")

inputfile = open(inputfilename, "r")
jsonrecords = inputfile.readlines()


# 3. Process data

for jsonrecord in jsonrecords:

    jsonrecord = json.loads(jsonrecord)
    marcrecord = marcx.Record(force_utf8=True)
    marcrecord.strict = False

    # Formatfestelegung
    format = "Article"

    # Leader
    leader = formats[format]["Leader"]
    marcrecord.leader = leader

    # Identifikator
    f001 = get_field(jsonrecord, "artikel_id")
    if not f001:
        continue
    marcrecord.add("001", data="185-" + f001)

    # Zugangsfacette
    url = get_field(jsonrecord, "url")
    if url:
        f007 = formats[format]["e007"]
    else:
        f007 = formats[format]["p007"]
    marcrecord.add("007", data=f007)

    # Periodizität
    year = get_field(jsonrecord, "jahr")
    periodicity = formats[format]["008"]
    language = "ger"
    f008 = marc_build_field_008(year, periodicity, language)
    marcrecord.add("008", data=f008)

    # ISSN
    identifier = get_field(jsonrecord, "issn")
    f022a = check_issn(identifier)
    marcrecord.add("022", a=f022a)

    # Sprache
    language = "ger"
    marcrecord.add("041", a=language)

    # DDC
    dabi = get_field(jsonrecord, "notationen")
    dabi = dabi.split(";")[0]
    dabi = dabi.replace("a", ".")
    f082 = dabi_to_ddc.get(dabi, "")
    marcrecord.add("082", a=f082)

    # 1. Urheber
    authors = get_field(jsonrecord, "autoren")
    authors = authors.split("; ")
    f100a = authors[0]
    f100a = f100a.strip()
    marcrecord.add("100", a=f100a, _4="aut")

    # Haupttitel und Titelzusatz
    f245a = get_field(jsonrecord, "titel")
    f245b = get_field(jsonrecord, "untertitel")
    marcrecord.add("245", a=f245a, b=f245b)

    # Erscheinungsvermerk
    f260a = get_field(jsonrecord, "ort")
    f260b = get_field(jsonrecord, "verlag")
    f260c = get_field(jsonrecord, "jahr")
    marcrecord.add("260", a=f260a, b=f260b, c=f260c)

    # RDA-Inhaltstyp
    f336b = formats[format]["336b"]
    marcrecord.add("336", b=f336b)

    # RDA-Datenträgertyp
    f338b = formats[format]["338b"]
    marcrecord.add("338", b=f338b)

    # Fußnote
    f500a = get_field(jsonrecord, "bemerkungen")
    marcrecord.add("500", a=f500a)
    f500a = get_field(jsonrecord, "oa_status")
    marcrecord.add("500", a=f500a)

    # Zusammenfassung
    f520a = get_field(jsonrecord, "abstract")
    marcrecord.add("520", a=f520a)

    # GND-Inhalts- und Datenträgertyp
    f655a = formats[format]["655a"]
    f6552 = formats[format]["6552"]
    marcrecord.add("655", a=f655a, _2=f6552)

    # weitere Urheber
    if authors:
        for f700a in authors[1:]:
            f700a = f700a.strip()
            marcrecord.add("700", a=f700a, _4="aut")

    # Herausgeber
    editors = get_field(jsonrecord, "herausgeber")
    if "Schelle-Wolff" in editors:
        editors = editors.split(", ")
    else:
        editors = editors.split("; ")
    for f700a in editors:
        if f700a:
            f700a = f700a.strip()
            marcrecord.add("700", a=f700a, _4="edt")

    # Zeitschrift
    f773t = get_field(jsonrecord, "zs_titel")
    volume = get_field(jsonrecord, "band")
    issue = get_field(jsonrecord, "heft")
    year = get_field(jsonrecord, "jahr")
    spage = get_field(jsonrecord, "anfangsseite")
    epage = get_field(jsonrecord, "endseite")
    f773g = marc_build_field_773g(volume, year, issue, spage, epage)
    marcrecord.add("773", t=f773t, g=f773g)

    # Link zur Ressource
    url = get_field(jsonrecord, "url")
    if url:
        marcrecord.add("856", q="text/html", _3="Link zur Ressource", u=url)

    # Link zur Zeitschrift
    url = get_field(jsonrecord, "zs_link")
    if url:
        marcrecord.add("856", q="text/html", _3="Link zur Zeitschrift", u=url)

    # SWB-Inhaltstyp
    f935c = formats[format]["935c"]
    marcrecord.add("935", c=f935c)

    collections = ["a", f001, "b", "185", "c", "sid-185-col-dabi"]
    marcrecord.add("980", subfields=collections)

    if outputformat == "xml":
        outputfile.write(marcrecord)
    else:
        outputfile.write(marcrecord.as_marc())

outputfile.close()
