import django_tables2 as tables
from django.utils.html import format_html
from mlcenter.lifecycles import models as lifecycle_models

class LifecyclesTable(tables.Table):
    
    name = tables.Column(accessor='name', verbose_name='Name', orderable=False)
    organization = tables.Column(accessor='owner.name', verbose_name='Organization', orderable=False)
    n_stages = tables.Column(accessor='stages', verbose_name='Number of Stages')
    stages = tables.Column(accessor='stages', verbose_name='Stages', orderable=False)
    created_at = tables.DateTimeColumn()
    actions = tables.TemplateColumn(template_name='lifecycles/lifecycle_list_actions.html', verbose_name='Actions', orderable=False)
    
    def render_stages(self, value):
        stages = value.all().order_by('order_number')
            
        return format_html('<i class="fa-solid fa-arrow-right mx-1"></i>'.join([stage.name for stage in stages]))
    
    def render_n_stages(self, value):
        return value.count()
    
 
    class Meta:
        model = lifecycle_models.Lifecycle
        template_name = "django_tables2/bootstrap4.html"
        order_by = ('-created_at')
        fields = ('name','organization','n_stages','stages','created_at','actions')
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