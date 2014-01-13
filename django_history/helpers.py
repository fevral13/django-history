# -*- coding:utf-8 -*-
from decimal import Decimal
from datetime import datetime, date, time
from types import NoneType

from django.utils.timezone import localtime
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from .settings import DATETIME_FORMAT, TIME_FORMAT, DATE_FORMAT


def serialize_field(obj, field_name, fail_silently=False):
    """Must serialize different fields differently
    - integers: integer
    - floats and decimals: float
    - string: string
    - foreign keys: integer
    - date: string "2012-01-03"
    - time: string "03:52 AM"
    - boolean: bool
    - datetime: string "2012-01-03 03:52 AM"
    - None value: null

    must be implemented per individual model class object
    - many-to-many: list of integers
    """
    if isinstance(field_name, (tuple, list)):
        return field_name

    try:
        value = getattr(obj, field_name)
    except ObjectDoesNotExist:
        if fail_silently:
            return field_name, None
        else:
            raise
    if isinstance(value, (int, bool, unicode, NoneType, float, str)):
        result = value
    elif isinstance(value, long):
        result = int(value)
    elif isinstance(value, Decimal):
        result = float(value)
    elif isinstance(value, datetime):
        result = unicode(localtime(value).strftime(DATETIME_FORMAT))
    elif isinstance(value, time):
        result = unicode(localtime(value).strftime(TIME_FORMAT))
    elif isinstance(value, date):
        result = unicode(localtime(value).strftime(DATE_FORMAT))
    elif isinstance(value, models.Model):
        result = value.id
    else:
        if fail_silently:
            result = str(value)
        else:
            raise Exception('Unknown type "%s" to convert' % type(value))

    return field_name, result
