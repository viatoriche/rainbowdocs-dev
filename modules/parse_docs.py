#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    parse_docs.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-15
# Description:
# TODO:

from modules.odftools import odf
import os
import re

class Parser():
    def __init__(self, dir_printforms):
        self.dir_printforms = dir_printforms

    def find_tags(self, txt): # find {% tagname|description %}
        tags = []
        for t in re.findall(r'{%\s*(.+)\s*%}', txt):
            st = t.split('|')
            name = st[0].strip()
            try:
                desc = st[1].strip()
            except:
                desc = name
            tags.append( (name, desc) )
        return tags

    def get_title(self, txt):
        txt = re.sub(r'[\n\r]','',txt)
        txt = re.sub(r'{{\s*end_title\s*}}', '{{ end_title }}\n', txt)
        titles = re.findall(r'{{\s*begin_title\s*}}(.*){{\s*end_title\s*}}', txt)
        return ' '.join(titles)

    def get_main(self, txt):
        try:
            re.search(r'{{\s*main\s*}}', txt).group(0)
            return True
        except:
            return False

    def get_doc(self, filename):
        return odf.load(self.dir_printforms +'/'+ filename)

    def create_form(self, printform, dest, number, date, date_held, tags, author = ''):
        doc = self.get_doc(printform)
        doc.replace(r'{{\s*main\s*}}', '')
        doc.replace(r'{{\s*author\s*}}', author)
        doc.replace(r'{{\s*begin_title\s*}}', '')
        doc.replace(r'{{\s*end_title\s*}}', '')
        doc.replace(r'{{\s*number\s*}}', number)
        doc.replace(r'{{\s*date\s*}}', date)
        doc.replace(r'{{\s*date_held\s*}}', date_held)
        for tag in tags:
            tagname = u'{0}'.format(tag.strip())
            doc.replace(r'{%\s*'+tagname+r'.+%}', tags[tag])
        doc.replace(r'{%.*%}', '')
        odf.dump(doc, dest)
        return True

    def scan(self):
        odf_files = []
        files = os.listdir(self.dir_printforms)
        for f in files:
            if f.endswith('ods'): odf_files.append(f)
        for f in files:
            if f.endswith('odt'): odf_files.append(f)

        for odf in odf_files:
            txt = self.get_doc(odf).toText()
            tags = self.find_tags(txt)
            title = self.get_title(txt)
            main = self.get_main(txt)
            yield (odf, title, tags, main)

# vi: ts=4
