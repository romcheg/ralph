# -*- coding: utf-8 -*-
from django.core.paginator import Paginator
from django.http import StreamingHttpResponse
from django.utils.translation import ugettext_lazy as _
from import_export.forms import ExportForm
from import_export.formats import base_formats as export_formats

from ralph.admin import RalphAdmin, RalphMPTTAdmin, register
from ralph.admin.mixins import RalphAdminForm
from ralph.admin.views.main import RalphChangeList
from ralph.attachments.admin import AttachmentsMixin
from ralph.data_importer import resources
from ralph.operations.filters import StatusFilter
from ralph.operations.models import (
    Change,
    Failure,
    Incident,
    Operation,
    OperationStatus,
    OperationType,
    Problem
)


class OperationChangeList(RalphChangeList):

    def get_filters(self, request):
        """Avoid using DISTINCT clause when base object filter is not used."""

        filter_specs, filter_specs_exist, lookup_params, use_distinct = \
            super(RalphChangeList, self).get_filters(request)

        filter_params = self.get_filters_params()

        return (
            filter_specs,
            filter_specs_exist,
            lookup_params,
            use_distinct if filter_params.get('base_objects') else False
        )


@register(OperationType)
class OperationTypeAdmin(RalphMPTTAdmin):
    list_display = ('name', 'parent')
    list_select_related = ('parent',)
    search_fields = ['name']

    def has_delete_permission(self, request, obj=None):
        # disable delete
        return False


@register(OperationStatus)
class OperationStatusAdmin(RalphAdmin):
    list_display = ('name',)
    search_fields = ['name']


class OperationAdminForm(RalphAdminForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _operation_type_subtree = self.instance._operation_type_subtree
        if _operation_type_subtree:
            root = OperationType.objects.get(pk=_operation_type_subtree)
            self.fields['type'].queryset = self.fields['type'].queryset.filter(
                pk__in=root.get_descendants(include_self=True)
            )


@register(Operation)
class OperationAdmin(AttachmentsMixin, RalphAdmin):
    search_fields = ['title', 'description', 'ticket_id']
    list_filter = ['type', ('status', StatusFilter), 'reporter',
                   'assignee', 'ticket_id', 'created_date',
                   'update_date', 'resolved_date', 'base_objects']
    list_display = ['title', 'type', 'created_date', 'status', 'reporter',
                    'get_ticket_url']
    list_select_related = ('reporter', 'type', 'status')
    raw_id_fields = ['assignee', 'reporter', 'base_objects']
    resource_class = resources.OperationResource
    form = OperationAdminForm

    fieldsets = (
        (_('Basic info'), {
            'fields': (
                'type', 'title', 'status', 'reporter', 'assignee',
                'description', 'ticket_id', 'created_date', 'update_date',
                'resolved_date',
            )
        }),
        (_('Objects'), {
            'fields': (
                'base_objects',
            )
        }),
    )

    def get_ticket_url(self, obj):
        return '<a href="{ticket_url}" target="_blank">{ticket_id}</a>'.format(
            ticket_url=obj.ticket_url,
            ticket_id=obj.ticket_id
        )
    get_ticket_url.allow_tags = True
    get_ticket_url.short_description = _('ticket ID')

    def get_changelist(self, request, **kwargs):
        return OperationChangeList

    def get_export_data_whole(self, file_format, request):
        yield 'BOO'
        queryset = self.get_export_queryset(request)
        resource_class = self.get_export_resource_class()

        data = resource_class().export(queryset)
        yield file_format.export_data(data)

    def get_export_data_in_chunks(self, file_format, request):
        """
        Returns file_format representation for given queryset.
        """
        yield 'BOO'
        queryset = self.get_export_queryset(
            request,
            iterated=False,
            prefetch=False
        )
        start = 0
        step = 100

        resource_class = self.get_export_resource_class()

        while True:
            to_export = queryset[start:start+step].prefetch_related(
                *resource_class._meta.prefetch_related
            )

            import ipdb; ipdb.set_trace()
            to_export = to_export.values_list()

            data = resource_class().export(to_export)

            if len(data) == 0:
                break

            if start != 0:
                data.headers = None

            export_data = file_format.export_data(data)
            yield export_data
            start += step

    def export_action(self, request, *args, **kwargs):
        chunkable_formats = {export_formats.CSV, export_formats.TSV}

        formats = self.get_export_formats()
        form = ExportForm(formats, request.POST or None)
        if form.is_valid():
            file_format = formats[
                int(form.cleaned_data['file_format'])
            ]()

            content_type = file_format.get_content_type()

            if type(file_format) in chunkable_formats:
                export_data = self.get_export_data_in_chunks(
                    file_format,
                    request
                )
            else:
                export_data = self.get_export_data_whole(file_format, request)

            response = StreamingHttpResponse(
                export_data,
                content_type=content_type
            )

            response['Content-Disposition'] = 'attachment; filename=%s' % (
                self.get_export_filename(file_format),
            )
            return response

        return super().export_action(request, *args, **kwargs)


@register(Change)
class ChangeAdmin(OperationAdmin):
    pass


@register(Incident)
class IncidentAdmin(OperationAdmin):
    pass


@register(Problem)
class ProblemAdmin(OperationAdmin):
    pass


@register(Failure)
class FailureAdmin(OperationAdmin):
    list_filter = OperationAdmin.list_filter + [
        'base_objects__asset__model__manufacturer'
    ]
