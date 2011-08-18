#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    parse_docs.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-15
# Description:
# TODO:

from openchain.modules.odftools import odf
import os
import re

class Parser():
    def __init__(self, dir_printforms):
        self.dir_printforms = dir_printforms

    def find_tags(self, txt): # find {% tagname|description %}
        tags = []
        for t in re.findall(r'{%\s+(.+)\s+%}', txt):
            st = t.split('|')
            name = st[0]
            try:
                desc = st[1]
            except:
                desc = name
            tags.append( (name, desc) )
        return tags

    def get_title(self, txt):
        return re.search(r'{{ begin_title }}(.+){{ end_title }}', txt).group(1)

    def get_doc(self, filename):
        return odf.load('{0}/{1}'.format(self.dir_printforms, filename))

    def scan(self):
        odt_files = []
        files = os.listdir(self.dir_printforms)
        for f in files:
            if f.endswith('odt'): odt_files.append(f)

        for odt in odt_files:
            txt = self.get_doc(odt).toText()
            tags = self.find_tags(txt)
            title = self.get_title(txt)
            yield (odt, title, tags)

def main():
    return 0

if __name__ == "__main__":
    main()

# vi: ts=4
