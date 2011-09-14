# -*- coding: utf-8 -*-
"""All main models"""

from django.db import models
from django.contrib.auth.models import User, Group

ODF_CHOICES = (
    ('ods', 'ods'),
    ('odt', 'odt'),
)

class Doc(models.Model):
    """All Documents with path to Print Forms (ODT)"""
    print_form = models.CharField('Print Form', max_length = 1024)
    title = models.CharField('Title', max_length = 1024)
    main = models.BooleanField('Main')
    # ods, odf
    type_odf = models.CharField('Type of ODF', max_length = 3, choices = ODF_CHOICES)
    ods_list = models.IntegerField('ODS List')

    class Meta:
        verbose_name = "Doc"
        permissions = (
            ("can_view_doc", "View"),
        )

    def __unicode__(self):
        return u'{0} - {1} Main: {2}'.format(self.id, self.title, self.main)

class Tag(models.Model):
    """All attributes (tags) for documents"""

    # name in printform
    name = models.CharField('Name', max_length = 1024)
    # description - for interface
    description = models.CharField('Desc', max_length = 1024)

    class Meta:
        verbose_name = "Tag"
        permissions = (
            ("can_view_tag", "View"),
        )

    def __unicode__(self):
        return u'{0} : {1} Cycle: {2}'.format(self.name, self.description, self.cycle)

class Link(models.Model):
    """Links = Doc - Tag"""

    doc = models.ForeignKey(Doc, verbose_name = 'Doc')
    tag = models.ForeignKey(Tag, verbose_name = 'Tag')

    class Meta:
        verbose_name = "Link"
        permissions = (
            ("can_view_link", "View"),
        )

    def __unicode__(self):
        return u'{0} - {1} [{2}]'.format(self.doc.title, self.tag.description, self.tag.name)

class Number(models.Model):
    """Real documents of system"""

    # Status of held
    held_status = models.BooleanField('Held', default = False)
    # Date of held
    date_held = models.DateTimeField('Helded', null = True, blank = True)
    # Date of create
    date_create = models.DateTimeField('Created', auto_now_add=True, auto_now=False)
    # Date of change
    date_change = models.DateTimeField('Changed', auto_now_add=True, auto_now=True)
    # Self is slave of main_number
    main_number = models.ForeignKey('self', blank = True, null = True, verbose_name = 'NumberMain')
    # Printform and type of doc
    doc = models.ForeignKey(Doc, verbose_name = 'Doc')
    # Author of document
    user = models.ForeignKey(User, verbose_name = 'Author')

    class Meta:
        verbose_name = "RealDoc"
        permissions = (
            ("can_view_number", "View"),
        )

    def __unicode__(self):
        return u'{0}: Held={1} Author: {2}'.format(self.id, self.held_status, self.user.username)

class Data(models.Model):
    """Data for numbers"""

    number = models.ForeignKey(Number, verbose_name = 'Number')
    tag_name = models.CharField('Name', max_length = 1024)
    tag_value = models.TextField('Value')

    class Meta:
        verbose_name = "Data"
        permissions = (
            ("can_view_data", "View"),
        )

    def __unicode__(self):
        return u'{0}: {1} = {2}'.format(self.number.id, self.tag.description, self.tag_value)



class Chain(models.Model):
    """Chain of documents"""

    # Main document
    main_doc = models.ForeignKey(Doc, related_name="main_doc", verbose_name = 'Main')
    # Slave document
    slave_doc = models.ForeignKey(Doc, related_name="slave_doc", verbose_name = 'Slave')

    class Meta:
        verbose_name = "Chain"
        permissions = (
            ("can_view_chain", "View"),
        )

    def __unicode__(self):
        return u'{0} → {1}'.format(self.main_doc.title, self.slave_doc.title)

class User_perms(models.Model):
    """User permissions for Doc"""

    doc = models.ForeignKey(Doc, verbose_name = 'Doc')
    user = models.ForeignKey(User, verbose_name = 'User')
    # if write - can write, else read only
    write = models.BooleanField('Write', default = False)

    class Meta:
        verbose_name = "PermsUser"

    def __unicode__(self):
        return u'{0} = {1} Write: {2}'.format(self.user.username, self.doc.title, self.write)

class Group_perms(models.Model):
    """Group permissions for Doc"""

    doc = models.ForeignKey(Doc, verbose_name = 'Doc')
    group = models.ForeignKey(Group, verbose_name = 'Group') # User ID author
    # if write - can write, else read only
    write = models.BooleanField('Write', default = False)

    class Meta:
        verbose_name = "PermsGroup"

    def __unicode__(self):
        return u'{0} = {1} Write: {2}'.format(self.group.name, self.doc.title, self.write)

