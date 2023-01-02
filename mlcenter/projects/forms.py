from django import forms
from mlcenter.projects import models as proj_models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Button, HTML, Div, Field
from django.contrib.contenttypes.models import ContentType
from mlcenter.organisations.models import Organization, OrganizationMember


class ProjectForm(forms.ModelForm):
    
    name = forms.CharField(label='Project Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Project Description', widget=forms.Textarea(attrs={'class': 'form-control'}))
    

    owner = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Select Owner',
        label='Owner',
        help_text='Select the type of owner for this project'
    )
    
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        organizations_user_is_part_of = OrganizationMember.objects.filter(user=self.request.user).values_list('organization_id', flat=True)
        organizations_user_owns = Organization.objects.filter(owner=self.request.user).values_list('id', flat=True)
        organizations_ids = list(set(list(organizations_user_is_part_of) + list(organizations_user_owns)))
        
        
        self.fields['owner'].queryset = Organization.objects.filter(id__in=organizations_ids)
        
        
        self.helper.layout = Layout(
            Field('name', css_class='form-control'),
            Field('description', css_class='form-control'),
            Field('owner', css_class='form-control'),
            
            Div(
                Submit('save', 'Save', css_class='btn btn-primary'),
                HTML('<a href="{% url "projects:list" %}" class="btn btn-danger float-end">Cancel</a>'),
                css_class='col-12'
            )
        )
        

    class Meta:
        model = proj_models.Project
        fields = ['name', 'description', 'owner']