from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django_tables2 import LazyPaginator
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.views.generic.detail import DetailView
from mlcenter.organisations import models as org_models
from mlcenter.organisations.tables import OrganizationMembersTable
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from mlcenter.organisations.filters import OrganizationFilter, OrganizationMemberFilter

class OrganizationView(View):
    model = org_models.Organization
    fields = ['name', 'description']
    success_url = reverse_lazy('organizations:list')
    
    
class OrganizationListView(OrganizationView, FilterView):
    context_object_name = "organizations_list"
    paginate_by = 9
    template_name = 'organisations/organization_list.html'
    filterset_class = OrganizationFilter
    
    def get_queryset(self):
        organizations_users_own = self.request.user.organization_set.all().values_list('id', flat=True)
        organizations_user_is_part_of = org_models.OrganizationMember.objects.all().filter(user=self.request.user).values_list('organization', flat=True)
        organizations = organizations_users_own.union(organizations_user_is_part_of)
        
        return self.model.objects.all().filter(id__in=organizations)

class OrganizationDetailView(OrganizationView, DetailView):
    pass

class OrganizationCreateView(OrganizationView, CreateView):
    def form_valid(self, form):
        
        if form.is_valid():
            form.instance.owner = self.request.user
            form.save()
        
        
        messages.success(self.request, 'Organization created successfully')
        return super().form_valid(form)
    

class OrganizationUpdateView(OrganizationView, UpdateView):
    
    def form_valid(self, form):
        messages.success(self.request, 'Organization updated successfully')
        return super().form_valid(form)

class OrganizationDeleteView(OrganizationView, DeleteView):
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Organization deleted successfully')
        return super().delete(request, *args, **kwargs)
    
    
    
class OrganizationMemberView(View):
    model = org_models.OrganizationMember
    fields = ['user', 'role']
    
    
    def get_success_url(self):
        return reverse_lazy('organizations:member_list', kwargs={'org_id': self.object.organization.id})
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = org_models.Organization.objects.get(id=self.kwargs['org_id'])
        
        return context
    
    
class OrganizationMemberDetailView(OrganizationMemberView, DetailView):
    context_object_name = "organization_member"
    
    
class OrganizationMemberListView(OrganizationMemberView, SingleTableMixin, FilterView):
    context_object_name = "organization_members_list"
    paginate_by = 10
    template_name = 'organisations/organizationmember_list.html'
    filterset_class = OrganizationMemberFilter
    table_class = OrganizationMembersTable
    paginator_class = LazyPaginator
    
    def get_queryset(self):
        return self.model.objects.filter(organization_id=self.kwargs['org_id'])
    
    
class OrganizationMemberCreateView(OrganizationMemberView, CreateView):
    def form_valid(self, form):
        
        if form.is_valid():
            form.instance.organization = org_models.Organization.objects.get(id=self.kwargs['org_id'])
            form.save()
        
        
        messages.success(self.request, 'Organization member added successfully')
        return super().form_valid(form)
    
class OrganizationMemberUpdateView(OrganizationMemberView, UpdateView):
    
    def form_valid(self, form):
        messages.success(self.request, 'Organization member updated successfully')
        return super().form_valid(form)
    
    
class OrganizationMemberDeleteView(OrganizationMemberView, DeleteView):
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Organization member deleted successfully')
        return super().delete(request, *args, **kwargs)