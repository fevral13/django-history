# -*- coding:utf-8 -*-
import logging

from django.contrib.auth.models import User
from django.db import models
from django.utils.simplejson import dumps
try:
    from django.utils.timezone import now
except ImportError:  # Django < 1.4
    from datetime import datetime
    now = datetime.now

from .. import ACTION_TYPE_CHOICES, ACTION_CHANGE, ACTION_CREATE, ACTION_DELETE
from ..middleware import thread_namespace
from ..helpers import serialize_field
from ..settings import SKIP_APPS, SKIP_TABLES, INCLUDE_APPS, INCLUDE_TABLES, HISTORY_ENABLED

logger = logging.getLogger(__name__)


class HistoryRecord(models.Model):
    datetime_created = models.DateTimeField(db_index=True)
    model = models.CharField(max_length=100, db_index=True)
    instance_pk = models.IntegerField()
    action_type = models.IntegerField(choices=ACTION_TYPE_CHOICES)
    data = models.TextField(blank=True, null=True)
    user = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        if self.id is None:
            self.datetime_created = now()
        super(HistoryRecord, self).save(*args, **kwargs)

    class Meta:
        app_label = 'history'


def log_record(sender, instance, *args, **kwargs):
    app = sender._meta.app_label
    model = sender._meta.object_name
    model_path = '.'.join([app, model])

    if (app in INCLUDE_APPS or model_path in INCLUDE_TABLES) and not (app in SKIP_APPS or model_path in SKIP_TABLES):
        logger.debug(u'Model %s' % model_path)
        if 'created' in kwargs:
            action_types = {True: ACTION_CREATE, False: ACTION_CHANGE}
            action_type = action_types[kwargs['created']]
            data = dumps([serialize_field(instance, f.name, fail_silently=True) for f in instance._meta.fields])
        else:
            action_type = ACTION_DELETE
            data = ''

        create_parameters = {'model': model_path, 'action_type': action_type, 'instance_pk': instance.pk, 'data': data}

        user = getattr(thread_namespace, 'user', 'None')
        if hasattr(user, '_wrapped') and hasattr(user, '_setup'):
            if user._wrapped.__class__ == object:
                user._setup()
            user = user._wrapped
            if isinstance(user, User):
                create_parameters['user'] = user

        HistoryRecord.objects.create(**create_parameters)


def anonymize_history_records(sender, instance, *args, **kwargs):
    HistoryRecord.objects.filter(user=instance).update(user=None)

if HISTORY_ENABLED:
    models.signals.post_save.connect(log_record, dispatch_uid='history_record_update')
    models.signals.post_delete.connect(log_record, dispatch_uid='history_record_delete')
    models.signals.pre_delete.connect(anonymize_history_records, sender=User, dispatch_uid='clean')