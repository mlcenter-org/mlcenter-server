from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from mlcenter.projects import models as project_models
from django_tables2 import SingleTableView, LazyPaginator
from mlcenter.experiments import forms as experiment_forms
from django.http import HttpResponse, HttpResponseRedirect
from mlcenter.lifecycles import models as lifecycle_models
from mlcenter.mlregister import models as mlregister_models
from mlcenter.mlregister import tables as mlregister_tables
from mlcenter.mlregister import filters as mlregister_filters
from django_tables2.views import SingleTableMixin, MultiTableMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class MLRegisterView(View):
    model = mlregister_models.MLRegister
    fields = [ 'name', 'lifecycle' ]
    
    def get_success_url(self):
        return reverse_lazy('mlregister:list', kwargs={'project_id': self.kwargs['project_id']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = project_models.Project.objects.get(id=self.kwargs['project_id'])
        return context
    
    
class MLRegisterListView(MLRegisterView, SingleTableMixin, FilterView):
    table_class = mlregister_tables.MLRegisterTable
    paginator_class = LazyPaginator
    filterset_class = mlregister_filters.MLRegisterFilter
    paginate_by = 10
    template_name = 'mlregister/mlregister_list.html'
    
    def get_queryset(self):
        return self.model.objects.filter(project__id=self.kwargs['project_id']).order_by('-created_at')

class MLRegisterCreateView(MLRegisterView, CreateView):
    
    # show only lifecyles available for the organization
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        project = project_models.Project.objects.get(id=self.kwargs['project_id'])
        
        form.fields['lifecycle'].queryset = form.fields['lifecycle'].queryset.filter(owner_id=project.owner_id)
        return form
    
    
    def form_valid(self, form):
        form.instance.project = project_models.Project.objects.get(id=self.kwargs['project_id'])
        messages.success(self.request, 'Model successfully created')
        return super().form_valid(form)
    
class MLRegisterUpdateView(MLRegisterView, UpdateView):
    
    def form_valid(self, form):
        messages.success(self.request, 'Model successfully updated')
        return super().form_valid(form)


class MLRegisterDetailView(MLRegisterView, DetailView):
    
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['releases'] =  mlregister_models.MLRelease.objects.filter(mlregister__id=self.kwargs['pk']).order_by('-created_at')[:20]
        context['stages'] = mlregister_models.MLRegister.objects.get(id=self.kwargs['pk']).lifecycle.stages.all().order_by('order_number')
        return context
    


class MLRegisterDeleteView(MLRegisterView, DeleteView):
    
    def get_success_url(self):
        messages.success(self.request, 'Model successfully deleted')
        return super().get_success_url()
    
    
class MLReleaseView(View):
    model = mlregister_models.MLRelease
    fields = '__all__'
    
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['project_id'] = self.kwargs['project_id']
        return kwargs
    
    
    def get_success_url(self):
        return reverse_lazy('mlregister:detail', kwargs={'project_id': self.kwargs['project_id'], 'mlregister_id': self.kwargs['mlregister_id']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = project_models.Project.objects.get(id=self.kwargs['project_id'])
        context['mlregister'] = mlregister_models.MLRegister.objects.get(id=self.kwargs['mlregister_id'])
        return context
    
    
class MLReleaseCreateView(MLReleaseView, CreateView):
    fields = None
    form_class = experiment_forms.ReleaseModelForm
        
    def form_valid(self, form):
        
        mlregister = mlregister_models.MLRegister.objects.get(id=form.data['mlregister'])
        
        #set mlregister id to kwargs
        self.kwargs['mlregister_id'] = mlregister.id
        
        messages.success(self.request, 'Release successfully created')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('mlregister:detail', kwargs={'project_id': self.kwargs['project_id'], 'pk': self.kwargs['mlregister_id'] })
    
    
class MLReleaseUpdateView(MLReleaseView, UpdateView):
        

    def get_success_url(self):
        return reverse_lazy('mlregister:detail', kwargs={'project_id': self.kwargs['project_id'], 'pk': self.kwargs['mlregister_id'] })
        
        
    # sending get request with all data inside the kwargs
    def get(self, request, *args, **kwargs):
        

        project = get_object_or_404(project_models.Project, id=self.kwargs['project_id'])
        mlregister = get_object_or_404(mlregister_models.MLRegister, id=self.kwargs['mlregister_id'])
        release = get_object_or_404(mlregister_models.MLRelease, id=self.kwargs['pk'])
        stage = get_object_or_404(lifecycle_models.LifecycleStage, id=self.kwargs['stage_id'])
        
        release.stage = str(stage.id)
        release.save()
        
        messages.success(self.request, 'Release successfully updated')
        return HttpResponseRedirect(reverse_lazy('mlregister:detail', kwargs={'project_id': self.kwargs['project_id'], 'pk': self.kwargs['mlregister_id'] }))
        
        
class MLReleaseDetailView(MLReleaseView, DetailView):
    pass