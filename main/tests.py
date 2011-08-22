#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    test.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-15
# Description:
# TODO:

from django.test import TestCase
from django.test.client import Client
from django.contrib import auth
from modules import parse_docs
from modules.database import Data
import settings


class WebTest(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        auth.models.User.objects.create_user('test', 'test@test.ru', 'nya')

    def testBasic(self):
        data = Data()
        response = self.client.post('', {'login': 'test', 'pass': 'nya'})
        login = self.client.login(username='test', password='nya')
        self.assertEqual(login, True)
        self.assertContains(response, 'logout')

        data.add_doc('jopa0.odt', 'JOPA0', True)
        data.add_doc('jopa1.odt', 'JOPA1', True)
        data.add_doc('jopa2.odt', 'JOPA2', False)

        response = self.client.get('/documents/all/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div id="1">JOPA0</div>')
        self.assertContains(response, '<div id="2">JOPA1</div>')
        self.assertContains(response, '<div id="3">JOPA2</div>')

        response = self.client.get('/documents/parse/')
        self.assertEqual(response.status_code, 200)
        #print response.content

        response = self.client.get('/chains/addcheck/1/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'True')

        data.add_chain(1, 1)
        data.add_chain(1, 2)

        response = self.client.get('/chains/addcheck/1/1/')
        self.assertContains(response, 'False')

        response = self.client.get('/chains/addcheck/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/chains/addcheck/1/')
        self.assertEqual(response.status_code, 404)

        t1 = data.add_tag('tag1', 'tag1')
        t2 = data.add_tag('tag2', 'tag2')
        t3 = data.add_tag('tag3', 'tag3')

        data.add_link(1, t3)
        data.add_link(1, t2)
        data.add_link(1, t1)

        response = self.client.get('/documents/new/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<option value="1">JOPA0</option>')

        response = self.client.post('/documents/new/', {'id_doc': '1'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/documents/new/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tag3: <input type="text" name="4"><br>tag2: <input type="text" name="3"><br>tag1: <input type="text" name="2"><br><br>')

        response = self.client.post('/documents/new/1/', {t1: 'nya1', t2: 'nya2', t3: 'nya3'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/documents/show/1/')
        self.assertContains(response, 'tag2: nya2<br>tag1: nya1<br>tag3: nya3<br>')

        response = self.client.get('/documents/edit/1/')
        self.assertContains(response, '<input type="submit" value="Change">')

        response = self.client.post('/documents/edit/1/', {t1: 'nya1_e', t2: 'nya2_e', t3: 'nya3_e'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/documents/show/1/')
        self.assertContains(response, 'tag2: nya2_e<br>tag1: nya1_e<br>tag3: nya3_e<br>')

        response = self.client.get('/documents/held/1/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/documents/show/1/')
        self.assertContains(response, '<b>Helded:')

        response = self.client.get('/chains/need/')
        self.assertContains(response, '<a href="/documents/new/1/1/">JOPA0 → JOPA0</a><br>')
        self.assertContains(response, '<a href="/documents/new/2/1/">JOPA0 → JOPA1</a><br>')

        response = self.client.get('/chains/add/')
        self.assertContains(response, '<input type="text" name="chains" value="1-1 1-2 ">')

        response = self.client.post('/chains/add/', {'chains': '2-1'})
        response = self.client.get('/chains/add/')
        self.assertContains(response, '<input type="text" name="chains" value="1-1 1-2 2-1 ">')

        # logout
        response = self.client.post('', {'logout': 'logout'} )
        self.assertContains(response, 'Auth')

        response = self.client.get('/documents/all/')
        self.assertEqual(response.status_code, 302)

class DBTest(TestCase):
    def testBasic(self):
        data = Data()
        p = parse_docs.Parser(settings.PRINT_FORMS_DIR)
        print 'All print forms:'
        scanned = p.scan()
        for pf in scanned:
            path_pf = pf[0]
            title_pf = pf[1]
            main_pf = pf[3]
            print u'Path: {0} / Title: {1} / Main: {2}\nTags:'.format(path_pf, title_pf, main_pf)
            for tag in pf[2]:
                tag_name = tag[0]
                tag_desc = tag[1]
                print u'Name: {0} / Description: {1}'.format(tag_name, tag_desc)
            print ''

        id_doc = data.add_doc('jopa.odt', 'JOPA1', True)
        id_doc = data.add_doc('jopa.odt', 'JOPA', True)
        self.assertEqual(id_doc, 1)
        self.assertEqual(data.doc.get(id = id_doc).title, 'JOPA')

        id_doc2 = data.add_doc('jopa2.odt', 'JOPA2', False)
        self.assertEqual(id_doc2, 2)

        id_doc3 = data.add_doc('jopa3.odt', 'JOPA3', False)
        self.assertEqual(id_doc3, 3)

        id_tag = data.add_tag('FIO', 'Name and Surname')
        id_tag = data.add_tag('FIO', 'Name and Surname 2')
        self.assertEqual(id_tag, 1)
        self.assertEqual(data.tag.get(id=1).description, 'Name and Surname 2')

        id_tag2 = data.add_tag('date', u'Date')
        self.assertEqual(id_tag2, 2)

        id_link = data.add_link(1, 1)
        id_link = data.add_link(1, 1)
        self.assertEqual(id_link, 1)

        id_link2 = data.add_link(1, 2)
        id_link3 = data.add_link(2, 2)

        self.assertEqual((id_link2, id_link3), (2, 3))

        id_chain = data.add_chain(1, 2)
        id_chain = data.add_chain(1, 2)
        self.assertEqual(id_chain, 1)

        id_chain2 = data.add_chain(3, 1)
        self.assertEqual(id_chain2, 2)

        id_num = data.add_number()
        self.assertEqual(id_num, 1)

        id_num = data.add_number(1)
        self.assertEqual(id_num, 2)

        res_add = data.add_data(1, 1, 1, 'gggg')
        self.assertEqual(res_add[0], True)

        res_add = data.add_data(3, 1, 1, 'gggg')
        self.assertEqual(res_add[0], False)

        res_add = data.add_data(2, 3, 1, 'gggg')
        self.assertEqual(res_add[0], False)

        r = data.change_data(1, 1, 'lololo')[0]
        self.assertEqual(r, True)

        r = data.change_number(1, False)[0]
        self.assertEqual(r, True)

        r = data.change_number(1, True)[0]
        self.assertEqual(r, True)

        self.assertEqual(data.id_doc_from_number(1), 1)

        docs = data.get_slave_docs(1, 1)
        self.assertEqual(docs[0], '2')

        slaves = data.get_all_need_slave()
        self.assertEqual(slaves[0][0], '2')


# vi: ts=4
