#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
"""Test odf"""

import sys
sys.path.append('/home/viator/Programming/python/openchain/openchain-dev')
sys.path.append('/home/viator/Programming/python/openchain/openchain-dev/modules/')

import odf
import document
import xml.dom.minidom as dom
import parse_docs
import re
from settings import PRINT_FORMS_DIR as filedir

def add_num_tags(node, num, tagname):
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

def main():
    """Main function, start module"""
    doc = parse_docs.get_doc('test.ods')
    doc = parse_docs.get_ods_doc_by_table_num(doc, 0)
    doc = clone_cycle(doc, 5, 'cycle_line')
    odf.dump(doc, '/tmp/dump.ods')

if __name__ == '__main__':
    main()

# vi: ts=4 sw=4

