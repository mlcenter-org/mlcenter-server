# create table using django tables for the experiment model
import django_tables2 as tables
import mlcenter.experiments.models as experiment_models
from django.utils.html import format_html



class DecimalColumn(tables.Column):
    
    def render(self, value):
        if isinstance(value, float):
            return round(value, 4)
        return value




class ExperimentTable(tables.Table):
    
    version = tables.LinkColumn('experiments:detail', args=[tables.A('project.id'),tables.A('pk')])
    name = tables.Column()
    tags = tables.Column()
    created_at = tables.DateTimeColumn()
    
    
    def __init__(self, *args, **kwargs):
        
        metrics_unique_keys = set()
        hyperparameters_unique_keys = set()
        for row in kwargs['data']:
            for key in row.metrics.keys():
                metrics_unique_keys.add(key)
            for key in row.hyperparameters.keys():
                hyperparameters_unique_keys.add(key)
                
        self.base_columns['metrics'] = tables.Column(verbose_name='Metrics:', accessor='none')
        for key in metrics_unique_keys:
            # round the values to 4 decimal places
            self.base_columns[f'metrics__{key}'] = DecimalColumn(verbose_name=key)
            
        self.base_columns['hyperparameters'] = tables.Column(verbose_name='Hyperparameters:', accessor='none')
            
        for key in hyperparameters_unique_keys:
            self.base_columns[f'hyperparameters__{key}'] = DecimalColumn(verbose_name=key)
        
        
        super(ExperimentTable, self).__init__(*args, **kwargs)
        
        
    def render_tags(self, value):
        tags = value.split(',')
        return format_html(''.join([f'<span class="badge badge-primary bg-primary mx-1">{tag}</span>' for tag in tags]))
        
        
    
    
    class Meta:
        model = experiment_models.Experiment
        template_name = "django_tables2/bootstrap4.html"
        fields = ('version', 'name', 'tags')
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