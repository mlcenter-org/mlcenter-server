from django import forms
from crispy_forms.helper import FormHelper
from django_filters import FilterSet, CharFilter
from crispy_forms.layout import Layout, Row, Column
from mlcenter.organisations import models 

class OrganizationFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'placeholder': 'Search for an organization'}))
    
    
    def __init__(self, *args, **kwargs):
        super(OrganizationFilter, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-control'),
            )
        )

    class Meta:
        model = models.Organization
        fields = ('name',)
        
        
# search in user.email field
class OrganizationMemberFilter(FilterSet):
    email = CharFilter(lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'placeholder': 'Search for a member'}), field_name='user__email')
    
    
    def __init__(self, *args, **kwargs):
        super(OrganizationMemberFilter, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-control'),
            )
        )

    class Meta:
        model = models.OrganizationMember
        fields = ('email',)