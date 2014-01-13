# -*- coding:utf-8 -*-
from django.conf import settings


try:
    HISTORY_ENABLED = settings.HISTORY_ENABLED
except AttributeError:
    HISTORY_ENABLED = True

try:
    SKIP_LIST = settings.HISTORY_SKIP_TABLES
except AttributeError:
    SKIP_LIST = ()

if not 'history' in SKIP_LIST:
    SKIP_LIST += ('history', )

try:
    INCLUDE_LIST = settings.HISTORY_INCLUDE_TABLES
except AttributeError:
    INCLUDE_LIST = ()

SKIP_APPS = set([i for i in SKIP_LIST if not '.' in i])
SKIP_TABLES = set([i for i in SKIP_LIST if '.' in i])

INCLUDE_APPS = set([i for i in INCLUDE_LIST if not '.' in i])
INCLUDE_TABLES = set([i for i in INCLUDE_LIST if '.' in i])

DATE_FORMAT = u'%Y-%m-%d'
DATETIME_FORMAT = u'%Y-%m-%d %I:%M %p'
TIME_FORMAT = u'%I:%M %p'
