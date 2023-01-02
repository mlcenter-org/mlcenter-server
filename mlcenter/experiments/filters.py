from django import forms
from crispy_forms.helper import FormHelper
from django_filters import FilterSet, CharFilter
from crispy_forms.layout import Layout, Row, Column
from mlcenter.experiments import models as experiment_models

class ExperimentFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'placeholder': 'Search for an experiment'}))
    
    
    def __init__(self, *args, **kwargs):
        super(ExperimentFilter, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-control'),
            )
        )

    class Meta:
        model = experiment_models.Experiment
        fields = ('name',)