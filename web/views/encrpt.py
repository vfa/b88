#!/usr/bin/env python
# -*- coding:utf-8 -*-
# by lanfc
import hashlib
from django.conf import settings


def md5(string):
    """MD5加密"""
    vhash = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    vhash.update(string.encode('utf-8'))
    return vhash.hexdigest()

