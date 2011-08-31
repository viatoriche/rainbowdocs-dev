#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
"""Module parser for printforms - ODF"""

from modules.odftools import odf, document
import os
import re
from copy import copy
import xml.dom.minidom as dom

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

    def create_form(self,
                    printform,
                    type_odf,
                    list_odf,
                    dest,
                    number,
                    date,
                    date_held,
                    tags,
                    author = ''):

        """create odf printform and dump to dest"""
        try:
            doc = self.get_doc(printform)
        except odf.ReadError:
            return False

        if type_odf == 'ods':
            lists = []
            for content in self.ods_get_content(printform):
                lists.append(content)

            content = lists[list_odf]
            content = content.encode('UTF-8')
            doc.content = dom.parseString(content)


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

    def xml_to_text(self, xml):
        """Get textdata from xml"""
        return '\n'.join([node.data for node in document.doc_order_iter(xml)
                    if node.nodeType == node.TEXT_NODE])


    def ods_get_content(self, odf_file):
        """Split ods to lists"""

        ods_doc = self.get_doc(odf_file)
        content = ods_doc.toXml().replace('<table:table table:name=',
                            '_SPLIT_TABLE_HERE_<table:table table:name=')
        content = content.split('_SPLIT_TABLE_HERE_')
        begin_content = content[0]
        end_content = u'</office:spreadsheet></office:body></office:document-content>'
        content = content[1:]
        end_num = len(content)-1
        content[end_num] = content[end_num].replace(
                    u'</office:spreadsheet></office:body></office:document-content>', '')
        for data in content:
            yield begin_content+data+end_content

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
            if odf_file.endswith('odt'):
                txt = self.get_doc(odf_file).toText()

                tags = self.find_tags(txt)
                title = self.get_title(txt)
                main = self.get_main(txt)
                type_odf = 'odt'
                ods_list = 0
                yield (odf_file, title, tags, main, type_odf, ods_list)
            elif odf_file.endswith('ods'):
                for odf_list, content in enumerate(self.ods_get_content(odf_file)):
                    content = content.encode('UTF-8')
                    xml = dom.parseString(content)
                    txt = self.xml_to_text(xml)

                    title = self.get_title(txt)
                    if title == '':
                        continue

                    tags = self.find_tags(txt)
                    main = self.get_main(txt)
                    type_odf = 'ods'
                    yield (odf_file, title, tags, main, type_odf, odf_list)


# vi: ts=4
