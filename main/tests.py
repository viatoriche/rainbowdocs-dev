#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)

"""Integrity Test for application"""

from django.test import TestCase
from django.test.client import Client
from django.contrib import auth
from modules.database import DataBase


class WebTest(TestCase):
    """Test for URLS"""

    def setUp(self):
        """Settings"""
        # Every test needs a client.
        self.client = Client()
        self.user = auth.models.User.objects.create_user('test', 
                                                         'test@test.ru', 
                                                         'nya')
        self.user.is_superuser = True
        self.user.save()

    def testBasic(self):
        """All tests"""
        database = DataBase()
        response = self.client.post('', {'login': 'test', 'pass': 'nya'})
        login = self.client.login(username='test', password='nya')
        self.assertEqual(login, True)
        self.assertContains(response, 'logout')

        doc1 = database.add_doc('jopa0.odt', 'JOPA0', 'odt', 0, True)
        doc2 = database.add_doc('jopa1.odt', 'JOPA1', 'odt', 0, True)
        database.add_doc('jopa2.odt', 'JOPA2', 'odt', 0, False)

        response = self.client.get('/documents/all/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div id="1">JOPA0</div>')
        self.assertContains(response, '<div id="2">JOPA1</div>')
        self.assertContains(response, '<div id="3">JOPA2</div>')

        response = self.client.get('/documents/parse/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/chains/addcheck/1/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'True')

        database.add_chain(doc1, doc1)
        database.add_chain(doc1, doc2)

        response = self.client.get('/chains/addcheck/1/1/')
        self.assertContains(response, 'False')

        response = self.client.get('/chains/addcheck/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/chains/addcheck/1/')
        self.assertEqual(response.status_code, 404)

        tag1 = database.add_tag('tag1', 'tag1')
        tag2 = database.add_tag('tag2', 'tag2')
        tag3 = database.add_tag('tag3', 'tag3')

        database.add_link(doc1, tag3)
        database.add_link(doc1, tag2)
        database.add_link(doc1, tag1)

        response = self.client.get('/documents/new/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<option value="1">JOPA0</option>')

        response = self.client.post('/documents/new/', {'id_doc': '1'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/documents/new/1/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'tag3')
        self.assertContains(response, 'tag2')
        self.assertContains(response, 'tag1')

        response = self.client.post('/documents/new/1/', 
                                    {tag1.id: 'nya1', 
                                     tag2.id: 'nya2', 
                                     tag3.id: 'nya3'})

        self.assertEqual(response.status_code, 302)

        response = self.client.get('/documents/show/1/')
        self.assertContains(response, 'nya1')
        self.assertContains(response, 'nya2')
        self.assertContains(response, 'nya3')

        response = self.client.get('/documents/edit/1/')
        self.assertContains(response, '<input type="submit" value="Change">')

        response = self.client.post('/documents/edit/1/',
                                   {'do': 'change',
                                    tag1.id: 'nya1_e',
                                    tag2.id: 'nya2_e',
                                    tag3.id: 'nya3_e'})

        self.assertEqual(response.status_code, 302)

        response = self.client.get('/documents/odf/1/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/documents/perm_error/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/documents/show/1/')
        self.assertContains(response, 'nya1_e')
        self.assertContains(response, 'nya2_e')
        self.assertContains(response, 'nya3_e')

        response = self.client.get('/documents/held/1/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/documents/show/1/')
        self.assertContains(response, '<b>Helded:')

        response = self.client.get('/chains/need/')
        self.assertContains(response, '<a href="/documents/new/1/1/">JOPA0 → JOPA0</a><br>')
        self.assertContains(response, '<a href="/documents/new/2/1/">JOPA0 → JOPA1</a><br>')

        response = self.client.get('/documents/new/1/1/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/documents/new/1/1/', 
                                    {'5': 'nya3_n',
                                     '4': 'nya2_n',
                                     '3': 'nya1_n'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/documents/show/2/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/documents/show/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/documents/edit/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/chains/add/')
        self.assertContains(response, '1 JOPA0 → 1 JOPA0')
        self.assertContains(response, '1 JOPA0 → 2 JOPA1')

        response = self.client.post('/chains/add/', {'chains': '2-1', 'save': ''})
        response = self.client.get('/chains/add/')
        self.assertContains(response, '1 JOPA0 → 1 JOPA0')
        self.assertContains(response, '1 JOPA0 → 2 JOPA1')
        self.assertContains(response, '2 JOPA1 → 1 JOPA0')

        response = self.client.get('/tags/links/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/tags/show/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/support/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/perms/user/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/perms/group/')
        self.assertEqual(response.status_code, 200)

        # logout
        response = self.client.post('', {'logout': 'logout'} )
        self.assertContains(response, 'Auth')

        response = self.client.get('/documents/all/')
        self.assertEqual(response.status_code, 302)

class DBTest(TestCase):
    """Test of database functions"""

    def setUp(self):
        """Default settings"""
        self.user = auth.models.User.objects.create_user('test', 'test@test.ru', 'nya')
        self.user.is_superuser = True
        self.user.save()

    def testBasic(self):
        database = DataBase()

        doc1 = database.add_doc('jopa.odt', 'JOPA', 'odt', 0, True)
        doc1 = database.add_doc('jopa.odt', 'JOPA1', 'odt', 0, True)
        self.assertEqual(doc1.id, 1)
        self.assertEqual(doc1.title, 'JOPA1')

        doc2 = database.add_doc('jopa2.odt', 'JOPA2', 'odt', 0, False)
        self.assertEqual(doc2.id, 2)

        doc3 = database.add_doc('jopa3.odt', 'JOPA3', 'odt', 0, False)
        self.assertEqual(doc3.id, 3)

        tag1 = database.add_tag('FIO', 'Name and Surname')
        tag1 = database.add_tag('FIO', 'Name and Surname 2')
        self.assertEqual(tag1.id, 1)
        self.assertEqual(tag1.description, 'Name and Surname 2')

        tag2 = database.add_tag('date', u'Date')
        self.assertEqual(tag2.id, 2)

        tag3 = database.add_tag('tag3', u'Tag3')
        self.assertEqual(database.del_tag(tag3), True)

        link1 = database.add_link(doc1, tag1)
        link1 = database.add_link(doc1, tag1)
        self.assertEqual(link1.id, 1)

        link2 = database.add_link(doc1, tag2)
        link3 = database.add_link(doc2, tag2)
        link4 = database.add_link(doc3, tag1)
        database.del_link_id(link4.id)

        self.assertEqual((link2.id, link3.id), (2, 3))

        chain1 = database.add_chain(doc1, doc2)
        self.assertEqual(chain1.id, 1)
        chain1 = database.add_chain(doc1, doc2)
        self.assertEqual(chain1.id, 1)

        chain2 = database.add_chain(doc3, doc1)
        self.assertEqual(chain2.id, 2)

        self.assertEqual(database.check_add_chain(doc1.id, doc2.id), False)
        self.assertEqual(database.check_add_chain(doc2.id, doc1.id), True)

        num1 = database.add_number(doc1, self.user)
        self.assertEqual(num1.id, 1)

        num2 = database.add_number(doc1, self.user, num1)
        self.assertEqual(num2.id, 2)

        num3 = database.add_number(doc3, self.user)
        self.assertEqual(database.del_number(num3), True)

        num3 = database.add_number(doc3, self.user)
        database.change_number(num3, True)
        self.assertEqual(database.del_number(num3), False)

        data1 = database.add_data(num1, tag1, 'gggg')
        self.assertEqual(data1, True)

        data2 = database.add_data(num1, tag1, 'hhhh')
        self.assertEqual(data2, False)

        data2 = database.add_data(num2, tag1, 'hhhh')
        self.assertEqual(data2, True)

        database.add_data(num2, tag1, 'tag1')
        self.assertEqual(database.del_tag_from_datadoc(num2, tag1), True)

        database.numbers_from_doc(doc1)

        data1 = database.change_data(num1, tag1, 'lololo')
        self.assertEqual(data1.tag_value, 'lololo')

        r = database.change_number(num1, False)
        self.assertEqual(r, True)

        r = database.change_number(num1, True)
        self.assertEqual(r, True)

        docs = database.get_slave_docs(num1)
        self.assertEqual(docs[0].id, 2)

        slaves = database.get_all_need_slave(self.user)
        self.assertEqual(slaves[0][0].id, 2)

        numbers = database.numbers_from_doc(doc1)
        self.assertEqual((numbers[0].id, numbers[1].id), (1, 2))

        # Test doc permissions
        self.user1 = auth.models.User.objects.create_user('user1', 'user1@example.com', 'user1')
        self.group1 = auth.models.Group.objects.create()
        self.group1.name = 'group1'
        self.group1.save()

        self.assertEqual(database.check_user_perm(self.user1, doc1, False), False)

        database.add_user_perm(self.user1, doc1, False)

        self.assertEqual(database.check_user_perm(self.user1, doc1, False), True)
        self.assertEqual(database.check_user_perm(self.user1, doc1, True), False)

        database.add_user_perm(self.user1, doc2, True)
        self.assertEqual(database.check_user_perm(self.user1, doc2, True), True)
        self.user1.groups.add(self.group1)

        database.add_group_perm(self.group1, doc1, True)
        self.assertEqual(database.check_group_perm(self.group1, doc1, True), True)

        docs = database.doc.all()
        database.add_group_perm(self.group1, doc3, False)
        self.user.groups.add(self.group1)

        docs_f = database.perm_doc_filter(self.user1, docs, False)
        self.assertEqual(docs_f, [doc1, doc2, doc3])

        docs_f = database.perm_doc_filter(self.user1, docs, True)
        self.assertEqual(docs_f, [doc2, doc1])

        self.assertEqual(database.check_doc_id('1'), True)
        self.assertEqual(database.check_doc_id('100'), False)

        # False - in number
        self.assertEqual(database.del_tag(tag1), False)

# vi: ts=4
