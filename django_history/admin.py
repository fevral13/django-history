# -*- coding:utf-8 -*-
from django.contrib import admin

from .models.history_record import HistoryRecord


class HistoryRecordAdmin(admin.ModelAdmin):
    list_display = ['model', 'instance_pk', 'action_type', 'datetime_created', 'user', 'select_similar_objects_link']
    list_filter = ['action_type', 'model']
    date_hierarchy = 'datetime_created'
    raw_id_fields = ['user']

    def select_similar_objects_link(self, obj):
        return u'<a href="?model=%s&instance_pk=%s">Select similar objects</a>' % (obj.model, obj.instance_pk)
    select_similar_objects_link.allow_tags = True
    select_similar_objects_link.short_description = 'Links'


admin.site.register(HistoryRecord, HistoryRecordAdmin)
