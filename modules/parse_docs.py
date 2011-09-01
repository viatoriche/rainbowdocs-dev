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
        """return parse_docs.get_doc() with dir_printforms"""
        return get_doc(self.dir_printforms +'/'+ filename)

    def ods_split_by_table(self, filename):
        """return parse_docs.ods_split_by_table() wirh dir_printforms"""
        return ods_split_by_table(self.dir_printforms +'/'+ filename)


    def create_form(self,
                    printform,
                    type_odf,
                    list_odf,
                    dest,
                    number,
                    date,
                    date_held,
                    tags,
                    # Templates for clone (tagname, count)
                    tags_cycle,
                    author = ''):

        """create odf printform and dump to dest"""
        try:
            doc = self.get_doc(printform)
        except odf.ReadError:
            return False

        if type_odf == 'ods':
            doc = get_ods_doc_by_table_num(doc, int(list_odf))
            for tagname, count in tags_cycle:
                doc = clone_cycle(doc, count, tagname)

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
            if odf_file.endswith('odt'):
                txt = self.get_doc(odf_file).toText()

                tags = self.find_tags(txt)
                title = self.get_title(txt)
                main = self.get_main(txt)
                type_odf = 'odt'
                ods_list = 0
                yield (odf_file, title, tags, main, type_odf, ods_list)
            elif odf_file.endswith('ods'):
                for odf_list, doc in enumerate(
                        self.ods_split_by_table(odf_file)):
                    txt = doc.toText()

                    title = self.get_title(txt)
                    if title == '':
                        continue

                    tags = self.find_tags(txt)
                    main = self.get_main(txt)
                    type_odf = 'ods'
                    yield (odf_file, title, tags, main, type_odf, odf_list)


def xml_to_text(xml):
    """Get textdata from xml"""
    return '\n'.join([node.data for node in document.doc_order_iter(xml)
                     if node.nodeType == node.TEXT_NODE])

# Tested
def check_cycle_template(tagname):
    try:
        re.search(r'^cycle_[a-zA-Z0-9]+$', tagname).group(0)
        return True
    except AttributeError:
        return False

# Tested
def check_cycle(tagname):
    try:
        re.search(r'^cycle_[a-zA-Z0-9]+_.+$', tagname).group(0)
        return True
    except AttributeError:
        return False

# Tested
def get_template_from_tagname(tagname):
    return re.search(r'^(cycle_[a-zA-Z0-9]+)_.+$', tagname).group(1)

# Tested
def get_tagname_from_tag_with_num(tagname):
    return re.search(r'^(cycle_[a-zA-Z0-9]+_\w+)_\d+$', tagname).group(1)

# Tested
def get_num_from_tag_with_num(tagname):
    return re.search(r'^cycle_[a-zA-Z0-9]+_\w+_(\d+)$', tagname).group(1)

def get_ods_doc_by_table_num(doc, table_num):
    """Return document with one table

    Input:
        doc - docuemnt.Document
        table_num - number of table [0..n]
    Output:
        doc - document.Document
    """

    content = doc.content
    elem = content.documentElement
    tables = elem.getElementsByTagName('table:table')
    body = elem.getElementsByTagName('office:spreadsheet')

    del tables[table_num]
    for del_table in tables:
        body[0].removeChild(del_table)

    return doc


def ods_split_by_table(odf_file):
    """Split ODS document by tables, and return list of docs

    Input: ofd_file - path to file
    Output: yield doc
    """
    doc = get_doc(odf_file)
    content = doc.content
    elem = content.documentElement
    tables = elem.getElementsByTagName('table:table')
    for table_num, table in enumerate(tables):
        doc = get_doc(odf_file)
        yield get_ods_doc_by_table_num(doc, table_num)


def add_num_tags(node, num, tagname):
    """Add num for tagname in node and all childnodes

    Recurse function

    Input:
        node - Node (xml.dom)
        num - number for concat
        tagname - tagname-template
    """
    if node.nodeType == node.TEXT_NODE:
        txt = node.data
        txt = txt.replace('%}', '%}\n')
        for tag in re.findall(r'{%\s*(.+)\s*%}', txt):
            split_tag = tag.split('|')
            name = split_tag[0].strip()
            if name.find(tagname) != -1:
                txt = txt.replace(name, name + '_' + str(num))

        txt = txt.replace('%}\n', '%}')
        node.data = txt
    else:
        for nodechild in node.childNodes:
            add_num_tags(nodechild, num, tagname)


def clone_cycle(doc, count, tagname):
    """Clone need rows by cycle-tagname template

    Input:
        doc - Document
        count - Count of rows
        tagname - template
    Output:
        doc
    """
    content = doc.content
    tables = content.getElementsByTagName('table:table')
    rows = content.getElementsByTagName('table:table-row')
    for row in rows:
        txt = row.toxml()
        if txt.find(tagname) != -1:
            find_row = row
            break

    for row_line in xrange(count):
        new_row = find_row.cloneNode(1)
        add_num_tags(new_row, row_line, tagname)

        tables[0].insertBefore(new_row, find_row)

    tables[0].removeChild(find_row)
    return doc


def get_doc(filename):
    """get odf.doc from filename"""
    try:
        return odf.load(filename)
    except odf.ReadError:
        raise odf.ReadError

# vi: ts=4
