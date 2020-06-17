from django.utils.translation import ugettext_lazy as _

from ralph.access_cards.models import AccessCard, AccessZone
from ralph.admin import RalphAdmin, RalphMPTTAdmin, register
from ralph.lib.transitions.admin import TransitionAdminMixin


@register(AccessCard)
class AccessCardAdmin(TransitionAdminMixin, RalphAdmin):
    show_transition_history = True
    list_display = ['status', 'visual_number', 'system_number', 'user',
                    'owner', 'get_employee_id']
    list_select_related = ['user', 'owner']
    raw_id_fields = ['user', 'owner', 'region']
    list_filter = ['status', 'issue_date',]
    search_fields = ['visual_number', 'system_number', 'user__first_name',
                     'user__last_name', 'user__username']
    readonly_fields = ['get_employee_id']

    fieldsets = (
        (
            _('Access Card Info'),
            {
                'fields': ('visual_number', 'system_number',
                           'status', 'region', 'issue_date', 'notes')
            }
        ),
        (
            _('User Info'),
            {
                'fields': ('user', 'owner', 'get_employee_id')
            }
        ),
        (
            _('Access Zones'),
            {
                'fields': ('access_zones',)
            }
        ),

    )

    def get_employee_id(self, obj):
        if obj.user is not None:
            return obj.user.employee_id
        else:
            return '-'

    get_employee_id.short_description = _('Employee ID')


@register(AccessZone)
class AccessZoneAdmin(RalphMPTTAdmin):
    list_display = ['name', 'parent', 'description']
    search_fields = ['name', 'description']

    fieldsets = (
        (
            _('Access Zone'),
            {
                'fields': ('parent', 'name', 'description')
            }
        ),
    )
