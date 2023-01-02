from django import forms
from crispy_forms.helper import FormHelper
from django_filters import FilterSet, CharFilter
from crispy_forms.layout import Layout, Row, Column
from mlcenter.projects import models 

class ProjectFilters(FilterSet):
    name = CharFilter(lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'placeholder': 'Search for a project'}))
    
    
    def __init__(self, *args, **kwargs):
        super(ProjectFilters, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-control'),
            )
        )

    class Meta:
        model = models.Project
        fields = ('name',)
        