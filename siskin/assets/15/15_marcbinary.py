#!/usr/bin/env python3
# coding: utf-8
# pylint: disable=C0103,C0301

"""
Custom conversion for IMSLP XML. Usually a set of files within a given
directory, refs #1240.

Usage:

    $ python 15_marcbinary.py [INPUT-DIRECTORY [, OUTPUT-FILE]]

"""

from __future__ import print_function

import io
import os
import re
import sys
from xml.sax.saxutils import escape, unescape

import marcx

# escape() and unescape() takes care of &, < and >.
html_escape_table = {
    '"': "&quot;",
    "'": "&apos;"
}
html_unescape_table = {v: k for k, v in html_escape_table.items()}


def html_escape(text):
    """ Escape HTML, see also: https://wiki.python.org/moin/EscapingHtml"""
    return escape(text, html_escape_table)


def html_unescape(text):
    """ Unescape HTML, see also: https://wiki.python.org/moin/EscapingHtml"""
    return unescape(text, html_unescape_table)

langmap = {
    "English": "eng",
    "German": "ger",
    "French": "fre",
    "Italian": "ita",
    "Russian": "rus",
    "Spanish": "spa",
    "Icelandic": "ice",
    "Polish": "pol",
    "Norwegian": "nor",
    "Latin": "lat",
    "Danish": "dan",
    "Finnish": "fin",
    "Welsh": "wel",
    "Swedish": "swe",
    "Neapolitan": "nap",
    "Hungarian": "hun",
    "Catalan": "cat",
    "Croatian": "hrv",
    "Czech": "cze",
    "Portuguese": "por",
    "Hebrew": "heb"
}

input_directory = "IMSLP"
output_filename = "15_output.mrc"

if len(sys.argv) > 1:
    input_directory = sys.argv[1]
if len(sys.argv) > 2:
    output_filename = sys.argv[2]

outputfile = io.open(output_filename, "wb")


for root, dirs, files in os.walk(input_directory):
    for filename in files:
        if not filename.endswith(".xml"):
            continue
        filepath = os.path.join(root, filename)
        inputfile = io.open(filepath, "r", encoding="utf-8")

        id = False
        title = False
        ptitle = False
        pub_year = False
        comp_year = False
        language = False
        subject1 = False  # Piece Style
        subject2 = False  # Instrumentation
        subject3 = False  # timeperiod
        footnote = False
        composer = False
        librettist = False
        url = False

        f001 = ""
        f041a = ""
        f100a = ""
        f1000 = ""
        f245a = ""
        f246a = ""
        f260c = ""
        f500a = ""
        f590a = ""
        f590b = ""
        f650a = []
        f689a = ""
        f700a = ""
        f856u = ""

        for line in inputfile:

            regexp = re.search(r"<recordId>(.*)<\/recordId>", line)
            if regexp:
                f001 = regexp.group(1)
                continue

            # Sprache

            if language:
                regexp = re.search(r"<string>(.*)<\/string>", line)
                if regexp:
                    language = regexp.group(1)
                    regexp = re.search(r"^(.*?)\W.*", language)
                    if regexp:
                        f041a = regexp.group(1)
                    else:
                        f041a = language
                    f041a = langmap.get(f041a, "")
                    if f041a == "":
                        print(r"Die Sprache %s fehlt in der Map!" % language)
                        f041 = "eng"

            regexp = re.search("name=\"Language\"", line)
            if regexp:
                language = True
                continue
            else:
                language = False

            # Komponist

            if composer:
                regexp = re.search(r"<string>(.*)<\/string>", line)
                if regexp:
                    f100a = regexp.group(1)

            regexp = re.search(r"name=\"composer\"", line)
            if regexp:
                composer = True
                continue
            else:
                composer = False

            # Sachtitel

            if title:
                regexp = re.search(r"<string>(.*)<\/string>", line)
                if regexp:
                    f245a = regexp.group(1)
                    f245a = html_unescape(f245a)

            regexp = re.search(r"name=\"worktitle\"", line)
            if regexp:
                title = True
                continue
            else:
                title = False

            # Alternativtitel

            if ptitle:
                regexp = re.search(r"<string>(.*)<\/string>", line)
                if regexp:
                    f246a = regexp.group(1)
                    f246a = html_unescape(f246a)

            regexp = re.search(r"name=\"Alternative Title\"", line)
            if regexp:
                ptitle = True
                continue
            else:
                ptitle = False

            # Erscheinungsjahr

            if pub_year:
                regexp = re.search(r"<string>(\d\d\d\d)<\/string>", line)
                if regexp:
                    f260c = regexp.group(1)
                else:
                    f260c = ""

            regexp = re.search(r"name=\"Year of First Publication\"", line)
            if regexp:
                pub_year = True
                continue
            else:
                pub_year = False

            # Kompositionsjahr

            if comp_year:
                regexp = re.search(r"<string>(\d\d\d\d)<\/string>", line)
                if regexp:
                    f650y = regexp.group(1)
                else:
                    f650y = ""

            regexp = re.search(r"name=\"Year/Date of Composition\"", line)
            if regexp:
                comp_year = True
                continue
            else:
                comp_year = False

            # Librettist

            if librettist:
                regexp = re.search(r"<string>\[\[:Category:(.*?)\|.*<\/string>", line)
                if regexp:
                    f700a = regexp.group(1)

            regexp = re.search(r"name=\"Librettist\"", line)
            if regexp:
                librettist = True
                continue
            else:
                librettist = False

            # Fußnote

            if footnote:

                regexp = re.search(r"<string>\[\[:Category:.*?\|(.*?)\]\]\sand\s\[\[:Category:.*?\|(.*?)\]\]<\/string>", line)
                if regexp:
                    person1, person2 = regexp.groups()
                    f500a = person1 + " and " + person2
                else:
                    regexp = re.search(r"<string>\[\[:Category:.*?\|(.*?)\]\]<\/string>", line)
                    if regexp:
                        f500a = regexp.group(1)

            regexp = re.search(r"name=\"Dedication\"", line)
            if regexp:
                footnote = True
                continue
            else:
                footnote = False

            # Stil (Piece Style)

            if subject1:
                regexp = re.search(r"<string>(.*)<\/string>", line)
                if regexp:
                    s = regexp.group(1)
                    s = s.title()
                    f650a.append(s)
                    f590a = s

            regexp = re.search(r"name=\"Piece Style\"", line)
            if regexp:
                subject1 = True
                continue
            else:
                subject1 = False

            # Besetzung (Instrumentation)

            if subject2:
                regexp = re.search(r"<string>(.*)<\/string>", line)
                if regexp:
                    s = regexp.group(1)
                    s = s.title()
                    f650a.append(s)
                    f590b = s

            regexp = re.search(r"name=\"Instrumentation\"", line)
            if regexp:
                subject2 = True
                continue
            else:
                subject2 = False

            # zeitliche Einordnung (Timeperiod)

            if subject3:
                regexp = re.search(r"<string>(.*)<\/string>", line)
                if regexp:
                    f650a.append(regexp.group(1))

            regexp = re.search(r"name=\"timeperiod\"", line)
            if regexp:
                subject3 = True
                continue
            else:
                subject3 = False

            # URL

            if url:
                regexp = re.search(r"<string>(.*)<\/string>", line)
                if regexp:
                    f856u = regexp.group(1)

            regexp = re.search(r"name=\"permlink\"", line)
            if regexp:
                url = True
                continue
            else:
                url = False

            # VIAF

            regexp = re.search(r"<viafId>(\d+)</viafId>", line)  # Feld manchmal vorhanden, aber leer
            if regexp:
                f1000 = regexp.group(1)
                f1000 = "(VIAF)" + f1000

        marcrecord = marcx.Record(force_utf8=True)
        marcrecord.strict = False
        marcrecord.leader = "     ncs  22        450 "
        marcrecord.add("001", data="finc-15-%s" % f001)
        marcrecord.add("007", data="qu")
        marcrecord.add("008", data="130227uu20uuuuuuxx uuup%s  c" % f041a)
        marcrecord.add("041", a=f041a)
        marcrecord.add("100", a=f100a, _0=f1000)
        marcrecord.add("245", a=f245a)
        marcrecord.add("246", a=f246a)
        marcrecord.add("260", c=f260c)
        marcrecord.add("500", a=f500a)
        marcrecord.add("590", subfields=["a", f590a, "b", f590b])
        marcrecord.add("650", y=f650y)
        marcrecord.add("700", a=f700a)

        subtest = []
        for subject in f650a:
            if subject not in subtest:
                subtest.append(subject)
                marcrecord.add("689", a=subject)

        marcrecord.add("856", q="text/html", _3="Petrucci-Musikbibliothek", u=f856u)

        marcrecord.add("970", c="PN")

        marcrecord.add("980", a=f001, b="15", c="Petrucci-Musikbibliothek")

        outputfile.write(marcrecord.as_marc())

        inputfile.close()

    # print(i)
    # if i == 10000:
    #    break


outputfile.close()
