# -*- coding: utf-8 -*-

from django.db import models

class Chain(models.Model):
    # Chain of documents
    id_main_doc = models.BigIntegerField() # Main document ID → Doc.id
    id_slave_doc = models.BigIntegerField() # Slave document ID → Doc.id

    def __unicode__(self):
        return u'{0} → {1}'.format(self.id_main_doc, self.id_slave_doc)

class Doc(models.Model):
    # All Documents with path to Print Forms (ODT)
    print_form = models.CharField(max_length = 1024)
    title = models.CharField(max_length = 1024)
    main = models.BooleanField()

    def __unicode__(self):
        return u'{0} - {1} Main: {2}'.format(self.id, self.title, self.main)

class Doc_tag(models.Model): # All attributes (tags) for documents
    name = models.CharField(max_length = 1024) # name in Doc
    description = models.CharField(max_length = 1024) # description - for interface

    def __unicode__(self):
        return u'{0}'.format(self.description)

class Doc_data(models.Model): # Data 
    number = models.BigIntegerField() # Uniq number → Doc_number.id
    id_doc = models.BigIntegerField() # Doc ID → Doc.id
    id_tag = models.BigIntegerField() # Attr ID → Doc_tag.id
    tag_value = models.TextField() # Data :3

    def __unicode__(self):
        return u'{0}'.format(self.number)

class Doc_link(models.Model): # Attr ←→ Doc depends
    id_doc = models.BigIntegerField() # Doc.id
    id_tag = models.BigIntegerField() # Doc_tag.id

    def __unicode__(self):
        return u'{0} - {1}'.format(self.id_doc, self.id_tag)

class Doc_number(models.Model): # Real documents of system
    held_status = models.BooleanField() # Status of held
    date_held = models.DateTimeField(null = True) # Date of held
    date_create = models.DateTimeField() # Date of create
    date_change = models.DateTimeField() # Date of change
    main_number = models.BigIntegerField(null = True) # Main Doc Number (chain) Doc_number.id or NULL

    def __unicode__(self):
        return u'{0}: Held={1}'.format(self.id, self.held_status)

