import django_tables2 as tables
from django.utils.html import format_html
import mlcenter.organisations.models as org_models

class OrganizationMembersTable(tables.Table):
    
    email = tables.Column(accessor='user.email', verbose_name='Email')
    organization = tables.Column(accessor='organization.name', verbose_name='Organization', orderable=False)
    role = tables.Column(accessor='role', verbose_name='Role')
    created_at = tables.DateTimeColumn()
    actions = tables.TemplateColumn(template_name='organisations/organizationmember_list_actions.html', verbose_name='Actions', orderable=False)
    
    class Meta:
        model = org_models.OrganizationMember
        template_name = "django_tables2/bootstrap4.html"
        order_by = ('-created_at')
        fields = ('email', 'organization', 'role', 'created_at', 'actions')
        attrs = {
            'class': 'table table-hover table-fixed text-nowrap table-sm',
            "th" : {
                "_ordering": {
                    "orderable": "sortable", # Instead of `orderable`
                    "ascending": "ascend",   # Instead of `asc`
                    "descending": "descend"  # Instead of `desc`
                }
            }
        }