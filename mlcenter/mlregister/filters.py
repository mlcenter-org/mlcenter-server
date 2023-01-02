from django import forms
from crispy_forms.helper import FormHelper
from django_filters import FilterSet, CharFilter
from crispy_forms.layout import Layout, Row, Column
from mlcenter.mlregister import models as mlregister_models

class MLRegisterFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'placeholder': 'Search for a model'}))
    
    
    def __init__(self, *args, **kwargs):
        super(MLRegisterFilter, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-control'),
            )
        )

    class Meta:
        model = mlregister_models.MLRegister
        fields = ('name',)
        