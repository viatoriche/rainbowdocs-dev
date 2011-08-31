#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
"""Module parser for printforms - ODF"""

from modules.odftools import odf
import os
import re

class Parser():
    """Class: Parser ODF files"""

    def __init__(self, dir_printforms):
        self.dir_printforms = dir_printforms

    def find_tags(self, txt):
        """find {% tagname|description %}"""

        tags = []
        for tag in re.findall(r'{%\s*(.+)\s*%}', txt):
            split_tag = tag.split('|')
            name = split_tag[0].strip()
            try:
                desc = split_tag[1].strip()
            except IndexError:
                desc = name
            tags.append( (name, desc) )
        return tags

    def get_title(self, txt):
        """get title from {{ begin_title }} TITLE {{ end_title }} template"""

        txt = re.sub(r'[\n\r]', '', txt)
        txt = re.sub(r'{{\s*end_title\s*}}', '{{ end_title }}\n', txt)
        titles = re.findall(
                    r'{{\s*begin_title\s*}}(.*){{\s*end_title\s*}}', txt)
        return ' '.join(titles)

    def get_main(self, txt):
        """Get main, return True if {{ main are finded }}"""

        try:
            re.search(r'{{\s*main\s*}}', txt).group(0)
            return True
        except AttributeError:
            return False

    def get_doc(self, filename):
        """get odf.doc from filename"""
        try:
            return odf.load(self.dir_printforms +'/'+ filename)
        except odf.ReadError:
            raise odf.ReadError

    def create_form(self, printform, dest, number, date, date_held, tags, author = ''):
        """create odf printform and dump to dest"""
        try:
            doc = self.get_doc(printform)
        except odf.ReadError:
            return False

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
        """scan printform dir for parse odf_file-docs
        ext: ods, odt
        """

        odf_files = []
        files = os.listdir(self.dir_printforms)
        for getfile in files:
            if getfile.endswith('ods'):
                odf_files.append(getfile)
            if getfile.endswith('odt'):
                odf_files.append(getfile)

        for odf_file in odf_files:
            txt = self.get_doc(odf_file).toText()
            tags = self.find_tags(txt)
            title = self.get_title(txt)
            main = self.get_main(txt)
            yield (odf_file, title, tags, main)

# vi: ts=4
