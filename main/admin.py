#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File name:    admin.py
# Author:       Viator (viator@via-net.org)
# License:      GPL (see http://www.gnu.org/licenses/gpl.txt)
# Created:      2011-08-15
# Description:
# TODO:

from django.contrib import admin
from openchain.main.models import Chain, Doc, Doc_attr, Doc_data, Doc_link, Doc_number

admin.site.register(Chain)
admin.site.register(Doc)
admin.site.register(Doc_attr)
admin.site.register(Doc_data)
admin.site.register(Doc_link)
admin.site.register(Doc_number)


# vi: ts=4
