from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.views.generic.list import ListView
from mlcenter.projects.forms import ProjectForm
from django.views.generic.detail import DetailView
from mlcenter.projects import models as proj_models
from mlcenter.projects.filters import ProjectFilters
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from mlcenter.organisations.models import Organization, OrganizationMember


class ProjectView(View):
    model = proj_models.Project
    
    def get_success_url(self):
        return reverse_lazy('projects:list')
    
    
class ProjectListView(ProjectView, FilterView):
    context_object_name = "projects_list"
    paginate_by = 9
    filterset_class = ProjectFilters
    template_name = 'projects/project_list.html'
    # user's projects
    def get_queryset(self):
        
        organizations_user_is_part_of = OrganizationMember.objects.filter(user=self.request.user).values_list('organization_id', flat=True)
        organizations_user_owns = Organization.objects.filter(owner=self.request.user).values_list('id', flat=True)
        organizations_ids = list(set(list(organizations_user_is_part_of) + list(organizations_user_owns)))
        
        return self.model.objects.all().filter(owner__in=organizations_ids)
    
    

class ProjectDetailView(ProjectView, DetailView):
    pass

class ProjectCreateView(ProjectView, CreateView):
    form_class = ProjectForm
    
    def get_form_kwargs(self):
        kw = super(ProjectCreateView, self).get_form_kwargs()
        kw['request'] = self.request 
    
        return kw
    

    def form_valid(self, form):
        
        messages.success(self.request, 'Project created successfully')
        return super().form_valid(form)


class ProjectUpdateView(ProjectView, UpdateView):
    form_class = ProjectForm
    
    def get_form_kwargs(self):
        kw = super(ProjectUpdateView, self).get_form_kwargs()
        kw['request'] = self.request 
        return kw
    
    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully')
        return super().form_valid(form)

class ProjectDeleteView(ProjectView, DeleteView):

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Project deleted successfully')
        return super().delete(request, *args, **kwargs)