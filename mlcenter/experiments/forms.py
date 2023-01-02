from django import forms
from mlcenter.projects import models as proj_models
from mlcenter.organisations.models import Organization, OrganizationMember
from mlcenter.mlregister import models as mlregister_models
from mlcenter.experiments import models as exp_models

class ReleaseModelForm(forms.ModelForm):
    
    description = forms.CharField(
        label='Release Description', 
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        help_text='Enter a description for the release',
        required=True
    )
    
    
    experiment = forms.ModelChoiceField(
        queryset=exp_models.Experiment.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Select Experiment',
        label='Experiment',
        help_text='Select the experiment to release as a model'

    )
    
    mlregister = forms.ModelChoiceField(
        queryset=mlregister_models.MLRegister.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Select Model',
        label='Register',
        help_text='Select the register to release the model to'
    )

    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.project_id = kwargs.pop('project_id', None)
        super(ReleaseModelForm, self).__init__(*args, **kwargs)
        
        print(self.project_id)

        project = proj_models.Project.objects.get(id=self.project_id)
        self.fields['experiment'].queryset = exp_models.Experiment.objects.filter(project=project)
        self.fields['mlregister'].queryset = mlregister_models.MLRegister.objects.filter(project=project)
        

    class Meta:
        model = mlregister_models.MLRelease
        fields = [ 'experiment','mlregister', 'description']