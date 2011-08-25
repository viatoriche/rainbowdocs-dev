# -*- coding: utf-8 -*-

from django.db import models

class Chain(models.Model):
    # Chain of documents
    id_main_doc = models.BigIntegerField() # Main document ID → Doc.id
    id_slave_doc = models.BigIntegerField() # Slave document ID → Doc.id

    class Meta:
        permissions = (
            ("can_view", "Can see all chains"),
            ("can_change", "Can change all chains"),
            ("can_add", "Can add chains"),
            ("can_delete", "Can delete all chains"),
        )

    def __unicode__(self):
        return u'{0} → {1}'.format(self.id_main_doc, self.id_slave_doc)

class Doc(models.Model):
    # All Documents with path to Print Forms (ODT)
    print_form = models.CharField(max_length = 1024)
    title = models.CharField(max_length = 1024)
    main = models.BooleanField()

    class Meta:
        permissions = (
            ("can_view", "Can see all docs (template forms)"),
            ("can_change", "Can change all docs (template forms)"),
            ("can_add", "Can add docs (template forms)"),
            ("can_delete", "Can delete all docs (template forms)"),
        )

    def __unicode__(self):
        return u'{0} - {1} Main: {2}'.format(self.id, self.title, self.main)

class Doc_tag(models.Model): # All attributes (tags) for documents
    name = models.CharField(max_length = 1024) # name in Doc
    description = models.CharField(max_length = 1024) # description - for interface

    class Meta:
        permissions = (
            ("can_view", "Can see all tags"),
            ("can_change", "Can change all tags"),
            ("can_add", "Can add tags"),
            ("can_delete", "Can delete tags"),
        )

    def __unicode__(self):
        return u'{0}'.format(self.description)

class Doc_data(models.Model): # Data 
    number = models.BigIntegerField() # Uniq number → Doc_number.id
    id_tag = models.BigIntegerField() # Attr ID → Doc_tag.id
    tag_value = models.TextField() # Data :3

    class Meta:
        permissions = (
            ("can_view", "Can see all data docs"),
            ("can_change", "Can change all data docs"),
            ("can_add", "Can add all data docs"),
            ("can_delete", "Can delete all data docs"),
        )

    def __unicode__(self):
        return u'{0}'.format(self.number)

class Doc_link(models.Model): # Attr ←→ Doc depends
    id_doc = models.BigIntegerField() # Doc.id
    id_tag = models.BigIntegerField() # Doc_tag.id

    class Meta:
        permissions = (
            ("can_view", "Can see all doc/tag links"),
            ("can_add", "Can add all doc/tag links"),
            ("can_delete", "Can delete all doc/tag links"),
        )

    def __unicode__(self):
        doc = Doc.objects.get(id = self.id_doc)
        tag = Doc_tag.objects.get(id = self.id_tag)
        return u'{0} - {1}'.format(doc.title, tag.description)

class Doc_number(models.Model): # Real documents of system
    held_status = models.BooleanField() # Status of held
    date_held = models.DateTimeField(blank = True) # Date of held
    date_create = models.DateTimeField() # Date of create
    date_change = models.DateTimeField() # Date of change
    main_number = models.BigIntegerField(blank = True) # Main Doc Number (chain) Doc_number.id or NULL
    id_doc = models.BigIntegerField() # Doc ID → Doc.id
    id_user = models.BigIntegerField() # User ID author

    class Meta:
        permissions = (
            ("can_view", "Can see all numbers"),
            ("can_add", "Can add number"),
            ("can_change", "Can change number"),
        )

    def __unicode__(self):
        return u'{0}: Held={1}'.format(self.id, self.held_status)


