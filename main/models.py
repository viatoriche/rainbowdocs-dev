# -*- coding: utf-8 -*-
#

from django.db import models

class Chain(models.Model):
    # Chain of documents
    id_main_doc = models.BigIntegerField() # Main document ID → Doc.id
    id_slave_doc = models.BigIntegerField() # Slave document ID → Doc.id

class Doc(models.Model):
    # All Documents with path to Print Forms (ODT)
    print_form = models.CharField(max_length = 1024)

class Doc_attr(models.Model): # All attributes (tags) for documents
    name = models.CharField(max_length = 1024)

class Doc_data(models.Model): # Data 
    number = models.BigIntegerField() # Uniq number → Doc_number.id
    id_doc = models.BigIntegerField() # Doc ID → Doc.id
    id_attr = models.BigIntegerField() # Attr ID → Doc_attr.id
    attr_value = models.TextField() # Data :3

class Doc_link(models.Model): # Attr ←→ Doc depends
    id_doc = models.BigIntegerField() # Doc.id
    id_attr = models.BigIntegerField() # Doc_attr.id

class Doc_number(models.Model): # Real documents of system
    held_status = models.BooleanField() # Status of held
    date_held = models.DateTimeField(null = True) # Date of held
    date_create = models.DateTimeField() # Date of create
    date_change = models.DateTimeField() # Date of change
    main_number = models.BigIntegerField(null = True) # Main Doc Number (chain) Doc_number.id or NULL

