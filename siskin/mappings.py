# coding: utf-8
# pylint: disable=C0103,W0232,C0301,W0703

# Copyright 2019 by Leipzig University Library, http://ub.uni-leipzig.de
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
Static mappings for reuse
"""

from collections import defaultdict

formats = defaultdict(dict)
languages = {}
roles = {}


#################################################################################
# Formate
#################################################################################

formats["Unknown"]["Leader"] = "     xxx  22        4500"
formats["Unknown"]["p007"] = "tu"
formats["Unknown"]["e007"] = "cr"
formats["Unknown"]["008"] = ""
formats["Unknown"]["336b"] = ""
formats["Unknown"]["338b"] = ""
formats["Unknown"]["655a"] = ""
formats["Unknown"]["6552"] = ""
formats["Unknown"]["935c"] = ""

formats["Multipart"]["Leader"] = "     cam  22       a4500"
formats["Multipart"]["p007"] = "tu"
formats["Multipart"]["e007"] = "cr"
formats["Multipart"]["008"] = ""
formats["Multipart"]["336b"] = ""
formats["Multipart"]["338b"] = ""
formats["Multipart"]["655a"] = ""
formats["Multipart"]["6552"] = ""
formats["Multipart"]["935c"] = ""

formats["Kit"]["Leader"] = "     com  22       a4500"
formats["Kit"]["p007"] = "ou"
formats["Kit"]["e007"] = "ou"
formats["Kit"]["008"] = ""
formats["Kit"]["336b"] = ""
formats["Kit"]["338b"] = ""
formats["Kit"]["655a"] = ""
formats["Kit"]["6552"] = ""
formats["Kit"]["935c"] = ""

formats["Manuscript"]["Leader"] = "     ctm  22        4500"
formats["Manuscript"]["p007"] = "tu"
formats["Manuscript"]["e007"] = "cr"
formats["Manuscript"]["008"] = ""
formats["Manuscript"]["336b"] = "txt"
formats["Manuscript"]["338b"] = "nc"
formats["Manuscript"]["655a"] = ""
formats["Manuscript"]["6552"] = ""
formats["Manuscript"]["935c"] = ""

#formats["Braille"]["Leader"] = ""
#formats["Braille"]["p007"] = ""
#formats["Braille"]["e007"] = ""
#formats["Braille"]["008"] = ""
#formats["Braille"]["336b"] = ""
#formats["Braille"]["338b"] = ""
#formats["Braille"]["655a"] = ""
#formats["Braille"]["6552"] = ""
#formats["Braille"]["935c"] = ""

formats["Image"]["Leader"] = "     ckm  22        4500"
formats["Image"]["p007"] = "kv"
formats["Image"]["e007"] = "cr"
formats["Image"]["008"] = ""
formats["Image"]["336b"] = "sti"
formats["Image"]["338b"] = "no"
formats["Image"]["655a"] = ""
formats["Image"]["6552"] = ""
formats["Image"]["935c"] = ""

formats["Thesis"]["Leader"] = "     cam  22        4500"
formats["Thesis"]["p007"] = "tu"
formats["Thesis"]["e007"] = "cr"
formats["Thesis"]["008"] = ""
formats["Thesis"]["336b"] = "txt"
formats["Thesis"]["338b"] = "nc"
formats["Thesis"]["655a"] = "Hochschulschrift"
formats["Thesis"]["6552"] = "gnd-content"
formats["Thesis"]["935c"] = ""

formats["Score"]["Leader"] = "     cam  22        4500"
formats["Score"]["p007"] = "tu"
formats["Score"]["e007"] = "cr"
formats["Score"]["008"] = ""
formats["Score"]["336b"] = ""
formats["Score"]["338b"] = ""
formats["Score"]["655a"] = ""
formats["Score"]["6552"] = ""
formats["Score"]["935c"] = "muno"

formats["Microform"]["Leader"] = "     cam  22        4500"
formats["Microform"]["p007"] = "hu"
formats["Microform"]["e007"] = "hu"
formats["Microform"]["008"] = ""
formats["Microform"]["336b"] = "txt"
formats["Microform"]["338b"] = "hj"
formats["Microform"]["655a"] = ""
formats["Microform"]["6552"] = ""
formats["Microform"]["935c"] = ""

formats["Map"]["Leader"] = "     cem  22        4500"
formats["Map"]["p007"] = "au"
formats["Map"]["e007"] = "cr"
formats["Map"]["008"] = ""
formats["Map"]["336b"] = "sti"
formats["Map"]["338b"] = "nc"
formats["Map"]["655a"] = "Atlas"
formats["Map"]["6552"] = "gnd-content"
formats["Map"]["935c"] = ""

formats["Book"]["Leader"] = "     cam  22        4500"
formats["Book"]["p007"] = "tu"
formats["Book"]["e007"] = "cr"
formats["Book"]["008"] = ""
formats["Book"]["336b"] = "txt"
formats["Book"]["338b"] = "nc"
formats["Book"]["655a"] = ""
formats["Book"]["6552"] = ""
formats["Book"]["935c"] = ""

formats["Series"]["Leader"] = "     cas  22        4500"
formats["Series"]["p007"] = "tu"
formats["Series"]["e007"] = "cr"
formats["Series"]["008"] = ""
formats["Series"]["336b"] = ""
formats["Series"]["338b"] = ""
formats["Series"]["655a"] = ""
formats["Series"]["6552"] = ""
formats["Series"]["935c"] = ""

formats["Newspaper"]["Leader"] = "     cas  22        4500"
formats["Newspaper"]["p007"] = "tu"
formats["Newspaper"]["e007"] = "cr"
formats["Newspaper"]["008"] = "n"
formats["Newspaper"]["336b"] = ""
formats["Newspaper"]["338b"] = ""
formats["Newspaper"]["655a"] = ""
formats["Newspaper"]["6552"] = ""
formats["Newspaper"]["935c"] = "zt"

formats["Journal"]["Leader"] = "     cas  22        4500"
formats["Journal"]["p007"] = "tu"
formats["Journal"]["e007"] = "cr"
formats["Journal"]["008"] = "p"
formats["Journal"]["336b"] = ""
formats["Journal"]["338b"] = ""
formats["Journal"]["655a"] = ""
formats["Journal"]["6552"] = ""
formats["Journal"]["935c"] = ""

formats["Article"]["Leader"] = "     cab  22        4500"
formats["Article"]["p007"] = "tu"
formats["Article"]["e007"] = "cr"
formats["Article"]["008"] = ""
formats["Article"]["336b"] = ""
formats["Article"]["338b"] = ""
formats["Article"]["655a"] = ""
formats["Article"]["6552"] = ""
formats["Article"]["935c"] = ""

formats["Chapter"]["Leader"] = "     caa  22        4500"
formats["Chapter"]["p007"] = "tu"
formats["Chapter"]["e007"] = "cr"
formats["Chapter"]["008"] = ""
formats["Chapter"]["336b"] = ""
formats["Chapter"]["338b"] = ""
formats["Chapter"]["655a"] = ""
formats["Chapter"]["6552"] = ""
formats["Chapter"]["935c"] = ""

formats["Loose-leaf"]["Leader"] = "     cai  22        4500"
formats["Loose-leaf"]["p007"] = "td"
formats["Loose-leaf"]["e007"] = "td"
formats["Loose-leaf"]["008"] = ""
formats["Loose-leaf"]["336b"] = ""
formats["Loose-leaf"]["338b"] = ""
formats["Loose-leaf"]["655a"] = "Loseblattsammlung"
formats["Loose-leaf"]["6552"] = "gnd-carrier"
formats["Loose-leaf"]["935c"] = "lo"

formats["Audio-Cassette"]["Leader"] = "     cjm  22        4500"
formats["Audio-Cassette"]["e007"] = "ss"
formats["Audio-Cassette"]["p007"] = "ss"
formats["Audio-Cassette"]["008"] = ""
formats["Audio-Cassette"]["336b"] = "prm"
formats["Audio-Cassette"]["338b"] = "ss"
formats["Audio-Cassette"]["655a"] = ""
formats["Audio-Cassette"]["6552"] = ""
formats["Audio-Cassette"]["935c"] = "muto"

formats["Video-Cassette"]["Leader"] = "     cgm  22        4500"
formats["Video-Cassette"]["e007"] = "vf"
formats["Video-Cassette"]["p007"] = "vf"
formats["Video-Cassette"]["008"] = ""
formats["Video-Cassette"]["336b"] = "tdi"
formats["Video-Cassette"]["338b"] = "vf"
formats["Video-Cassette"]["655a"] = "Film"
formats["Video-Cassette"]["6552"] = "gnd-content"
formats["Video-Cassette"]["935c"] = "vide"

formats["Blu-Ray-Disc"]["Leader"] = "     cgm  22        4500"
formats["Blu-Ray-Disc"]["e007"] = "vd"
formats["Blu-Ray-Disc"]["p007"] = "vd"
formats["Blu-Ray-Disc"]["008"] = ""
formats["Blu-Ray-Disc"]["336b"] = "tdi"
formats["Blu-Ray-Disc"]["338b"] = "vd"
formats["Blu-Ray-Disc"]["655a"] = "Blu-Ray-Disc"
formats["Blu-Ray-Disc"]["6552"] = "gnd-carrier"
formats["Blu-Ray-Disc"]["935c"] = "vide"

formats["DVD-Video"]["Leader"] = "     cgm  22        4500"
formats["DVD-Video"]["e007"] = "co"
formats["DVD-Video"]["p007"] = "co"
formats["DVD-Video"]["008"] = ""
formats["DVD-Video"]["336b"] = "tdi"
formats["DVD-Video"]["338b"] = "vd"
formats["DVD-Video"]["655a"] = "DVD-Video"
formats["DVD-Video"]["6552"] = "gnd-carrier"
formats["DVD-Video"]["935c"] = "vide"

formats["DVD-Audio"]["Leader"] = "     cjm  22        4500"
formats["DVD-Audio"]["p007"] = "co"
formats["DVD-Audio"]["e007"] = "co"
formats["DVD-Audio"]["008"] = ""
formats["DVD-Audio"]["336b"] = "prm"
formats["DVD-Audio"]["338b"] = "sd"
formats["DVD-Audio"]["655a"] = "DVD-Audio"
formats["DVD-Audio"]["6552"] = "gnd-carrier"
formats["DVD-Audio"]["935c"] = "muto"

formats["DVD-ROM"]["Leader"] = "     cam  22        4500"
formats["DVD-ROM"]["p007"] = "co"
formats["DVD-ROM"]["e007"] = "co"
formats["DVD-ROM"]["008"] = ""
formats["DVD-ROM"]["336b"] = "txt"
formats["DVD-ROM"]["338b"] = "dvd"
formats["DVD-ROM"]["655a"] = "DVD-ROM"
formats["DVD-ROM"]["6552"] = "gnd-carrier"
formats["DVD-ROM"]["935c"] = ""

formats["CD-Video"]["Leader"] = "     cgm  22        4500"
formats["CD-Video"]["p007"] = "co"
formats["CD-Video"]["e007"] = "co"
formats["CD-Video"]["008"] = ""
formats["CD-Video"]["336b"] = "tdi"
formats["CD-Video"]["338b"] = "vd"
formats["CD-Video"]["655a"] = "CD"
formats["CD-Video"]["6552"] = "gnd-carrier"
formats["CD-Video"]["935c"] = "vide"

formats["CD-Audio"]["Leader"] = "     cjm  22        4500"
formats["CD-Audio"]["p007"] = "sd"
formats["CD-Audio"]["e007"] = "sd"
formats["CD-Audio"]["008"] = ""
formats["CD-Audio"]["336b"] = "prm"
formats["CD-Audio"]["338b"] = "sd"
formats["CD-Audio"]["655a"] = "CD"
formats["CD-Audio"]["6552"] = "gnd-carrier"
formats["CD-Audio"]["935c"] = "muto"

formats["CD-ROM"]["Leader"] = "     cam  22        4500"
formats["CD-ROM"]["p007"] = "co"
formats["CD-ROM"]["e007"] = "co"
formats["CD-ROM"]["008"] = ""
formats["CD-ROM"]["336b"] = "txt"
formats["CD-ROM"]["338b"] = "cd"
formats["CD-ROM"]["655a"] = ""
formats["CD-ROM"]["6552"] = "gnd-carrier"
formats["CD-ROM"]["935c"] = ""

formats["Floppy-Disk"]["Leader"] = "     cam  22        4500"
formats["Floppy-Disk"]["p007"] = "cj"
formats["Floppy-Disk"]["e007"] = "cj"
formats["Floppy-Disk"]["008"] = ""
formats["Floppy-Disk"]["336b"] = ""
formats["Floppy-Disk"]["338b"] = ""
formats["Floppy-Disk"]["655a"] = "Diskette"
formats["Floppy-Disk"]["6552"] = "gnd-carrier"
formats["Floppy-Disk"]["935c"] = ""

formats["Online-Video"]["Leader"] = "     ngm  22        4500"
formats["Online-Video"]["p007"] = "cr"
formats["Online-Video"]["e007"] = "cr"
formats["Online-Video"]["008"] = ""
formats["Online-Video"]["336b"] = "tdi"
formats["Online-Video"]["338b"] = "cr"
formats["Online-Video"]["655a"] = "Film"
formats["Online-Video"]["6552"] = "gnd-content"
formats["Online-Video"]["935c"] = "vide"

formats["Online-Audio"]["Leader"] = "     cam  22        4500"
formats["Online-Audio"]["p007"] = "cr"
formats["Online-Audio"]["e007"] = "cr"
formats["Online-Audio"]["008"] = ""
formats["Online-Audio"]["336b"] = "prm"
formats["Online-Audio"]["338b"] = "cr"
formats["Online-Audio"]["655a"] = ""
formats["Online-Audio"]["6552"] = ""
formats["Online-Audio"]["935c"] = "muto"

formats["Website"]["Leader"] = "     cai  22        4500"
formats["Website"]["p007"] = "cr"
formats["Website"]["e007"] = "cr"
formats["Website"]["008"] = ""
formats["Website"]["336b"] = "txt"
formats["Website"]["338b"] = "cr"
formats["Website"]["655a"] = "Website"
formats["Website"]["6552"] = "gnd-content"
formats["Website"]["935c"] = ""

formats["Object"]["Leader"] = "     crm  22        4500"
formats["Object"]["p007"] = "zz"
formats["Object"]["e007"] = "zz"
formats["Object"]["008"] = ""
formats["Object"]["336b"] = ""
formats["Object"]["338b"] = "nr"
formats["Object"]["655a"] = ""
formats["Object"]["6552"] = ""
formats["Object"]["935c"] = "gegenst"

#################################################################################
# Sprachen
#################################################################################

languages["english"] = "eng"
languages["french"] = "fre"
languages["german"] = "ger"
languages["greek"] = "gre"
languages["italian"] = "ita"
languages["latin"] = "lat"
languages["polish"] = "pol"
languages["russian"] = "rus"
languages["sanskrit"] = "san"
languages["spanish"] = "spa"

languages["ar"] = "ara"
languages["bo"] = "tib"
languages["cs"] = "cze"
languages["da"] = "dan"
languages["de"] = "ger"
languages["el"] = "gre"
languages["en"] = "eng"
languages["es"] = "spa"
languages["fr"] = "fre"
languages["he"] = "heb"
languages["hi"] = "hin"
languages["it"] = "ita"
languages["la"] = "lat"
languages["nl"] = "dut"
languages["pl"] = "pol"
languages["ru"] = "rus"
languages["sa"] = "san"
languages["sp"] = "spa"
languages["ur"] = "urd"
languages["yi"] = "yid"

#################################################################################
# Personenrollen
#################################################################################

roles["author"] = "aut"
roles["composer"] = "cmp"
roles["editor"] = "edt"
