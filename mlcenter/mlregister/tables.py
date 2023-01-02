import django_tables2 as tables
from django.utils.html import format_html
import mlcenter.mlregister.models as mlregister_models

class MLRegisterTable(tables.Table):
    
    name = tables.LinkColumn('mlregister:detail', args=[tables.A('project.id'),tables.A('pk')])
    lifecycle = tables.Column()
    stages = tables.Column(verbose_name='Stages', accessor='pk')
    n_releases = tables.Column(verbose_name='Releases', accessor='pk')
    created_at = tables.DateTimeColumn()
    
    def render_stages(self, value):
        stages = mlregister_models.MLRegister.objects.get(id=value).lifecycle.stages.all().order_by('order_number')
            
        return format_html('<i class="fa-solid fa-arrow-right mx-1"></i>'.join([stage.name for stage in stages]))
    
    
    def render_n_releases(self, value):
        return mlregister_models.MLRelease.objects.filter(mlregister__id=value).count()
    
    class Meta:
        model = mlregister_models.MLRegister
        template_name = "django_tables2/bootstrap4.html"
        fields = ('name','lifecycle','n_releases','stages','created_at')
        order_by = ('-created_at')
        attrs = {
            'class': 'table table-hover experiments-table table-fixed text-nowrap table-sm',
            "th" : {
                "_ordering": {
                    "orderable": "sortable", # Instead of `orderable`
                    "ascending": "ascend",   # Instead of `asc`
                    "descending": "descend"  # Instead of `desc`
                }
            }
        }