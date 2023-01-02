from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django_tables2 import SingleTableView, LazyPaginator
from mlcenter.experiments import models as experiment_models
from mlcenter.projects import models as project_models
from mlcenter.experiments import tables as experiment_tables
from mlcenter.experiments import filters as experiment_filters
from mlcenter.experiments import forms as experiment_forms
from django_tables2.views import SingleTableMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http.response import JsonResponse

FILES_MAPPING={
    'image': ['jpg','jpeg','png'],
    'archive': ['zip','tar','gz','bz2','rar'],
    'code': ['py', 'json', 'js', 'html', 'css', 'txt', 'md', 'csv', 'tsv', 'xml', 'yml', 'yaml'],
}


def get_file_type(f_type, mapping_list):
    for key, value in mapping_list.items():
        if f_type in value:
            return key
    return 'file'


class ExperimentView(View):
    model = experiment_models.Experiment
    fields = '__all__'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['project_id'] = self.kwargs['project_id']
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('experiments:list', kwargs={'project_id': self.kwargs['project_id']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = project_models.Project.objects.get(id=self.kwargs['project_id'])
        return context
    
    
class ExperimentListView(ExperimentView, SingleTableMixin, FilterView):
    table_class = experiment_tables.ExperimentTable
    paginator_class = LazyPaginator
    filterset_class = experiment_filters.ExperimentFilter
    paginate_by = 9
    template_name = 'experiments/experiment_list.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['release_model_form'] = experiment_forms.ReleaseModelForm(request=self.request, project_id=self.kwargs['project_id'])
        return context
    
    
    def get_queryset(self):
        return self.model.objects.filter(project__id=self.kwargs['project_id']).order_by('-created_at')
    

class ExperimentDetailView(ExperimentView, DetailView):
    pass


class ExperimentDeleteView(ExperimentView, DeleteView):
    model = experiment_models.Experiment
    fields = '__all__'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('request')
        kwargs.pop('project_id')
        # kwargs['request'] = self.request
        # kwargs['project_id'] = self.kwargs['project_id']
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('experiments:list', kwargs={'project_id': self.kwargs['project_id']})
    
    def get_context_data(self, **kwargs):
        context = dict()
        context['project'] = project_models.Project.objects.get(id=self.kwargs['project_id'])
        context['experiment'] = experiment_models.Experiment.objects.get(id=self.kwargs['pk'])
        return context
    
    
    def form_valid(self, form):
        messages.success(self.request, 'Experiment deleted successfully')
        return super().form_valid(form)
    


def jstree_experiment_artifacts(request, project_id, pk):
    experiment_artifacts = experiment_models.ExperimentArtifact.objects.filter(experiment__id=pk, experiment__project_id=project_id).order_by('name')
    
    files = []
    for experiment_artifact in experiment_artifacts:
        try:
            file_type = experiment_artifact.artifact.url.split('.')[-1].split('?')[0]
            file_type = get_file_type(file_type, FILES_MAPPING)

        except:
            file_type = 'file'
            
            
        files.append({
            'id': experiment_artifact.id,
            'text': experiment_artifact.name,
            'url': experiment_artifact.artifact.url,
            'type': file_type
        })
    
    
    return JsonResponse(files, safe=False, status=200)
    
    