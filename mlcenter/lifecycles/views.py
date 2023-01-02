from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django_tables2 import LazyPaginator
from django_filters.views import FilterView
from django.views.generic.list import ListView
from django_tables2.views import SingleTableMixin
from django.views.generic.detail import DetailView
from mlcenter.lifecycles.tables import LifecyclesTable
from mlcenter.organisations import models as org_models
from mlcenter.lifecycles.filters import LifecyclesFilter
from django.contrib.auth.decorators import login_required
from mlcenter.lifecycles import models as lifecycle_models
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class LifecycleView(View):
    model = lifecycle_models.Lifecycle
    fields = ['name', 'description']
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organization"] =  org_models.Organization.objects.get(id=self.kwargs['org_id'])
        return context
    
    
    def get_success_url(self):
        return reverse_lazy('lifecycles:list', kwargs={'org_id': self.kwargs['org_id']})
    
    
class LifecycleListView(LifecycleView, SingleTableMixin, FilterView):
    context_object_name = "lifecycles_list"
    paginate_by = 9
    filterset_class = LifecyclesFilter
    template_name = 'lifecycles/lifecycle_list.html'
    table_class = LifecyclesTable
    paginator_class = LazyPaginator

    
    def get_queryset(self):
        return lifecycle_models.Lifecycle.objects.filter(owner__id=self.kwargs['org_id']).order_by('-created_at')
    
    
class LifecycleDetailView(LifecycleView, DetailView):
    pass


class LifecycleCreateView(LifecycleView, CreateView):
    def form_valid(self, form):
        messages.success(self.request, 'Lifecycle created successfully')
        
        if form.is_valid():
            form.instance.owner = org_models.Organization.objects.get(id=self.kwargs['org_id'])
            form.save()
        
        
        return super().form_valid(form)
    
class LifecycleUpdateView(LifecycleView, UpdateView):
    
    def form_valid(self, form):
        messages.success(self.request, 'Lifecycle updated successfully')
        
        return super().form_valid(form)
    
class LifecycleDeleteView(LifecycleView, DeleteView):
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Lifecycle deleted successfully')
        return super().delete(request, *args, **kwargs)
    
    
class LifecycleStageView(View):
    model = lifecycle_models.LifecycleStage
    fields = ['name', 'description', 'roles']
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organization"] =  org_models.Organization.objects.get(id=self.kwargs['org_id'])
        context['lifecycle'] = lifecycle_models.Lifecycle.objects.get(id=self.kwargs['lifecycle_id'])
        return context
    
     
    def get_success_url(self):
        return reverse_lazy('lifecycles:stage_list', kwargs={'org_id': self.kwargs['org_id'], 'lifecycle_id': self.kwargs['lifecycle_id']})
    
    
    
class LifecycleStageListView(LifecycleStageView, ListView):
    context_object_name = "lifecycle_stages_list"
    
    def get_queryset(self):
        return lifecycle_models.LifecycleStage.objects.filter(lifecycle=self.kwargs['lifecycle_id']).order_by('order_number')
    
class LifecycleStageDetailView(LifecycleStageView, DetailView):
    pass


class LifecycleStageCreateView(LifecycleStageView, CreateView):
    def form_valid(self, form):
        messages.success(self.request, 'Lifecycle Stage created successfully')
        
        if form.is_valid():
            form.instance.lifecycle = lifecycle_models.Lifecycle.objects.get(id=self.kwargs['lifecycle_id'])
            form.save()
        
        
        return super().form_valid(form)
    

class LifecycleStageUpdateView(LifecycleStageView, UpdateView):
    
    def form_valid(self, form):
        messages.success(self.request, 'Lifecycle Stage updated successfully')
        
        return super().form_valid(form)
    
    
class LifecycleStageDeleteView(LifecycleStageView, DeleteView):
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Lifecycle Stage deleted successfully')
        return super().delete(request, *args, **kwargs)
    
@login_required 
def update_lifecycle_stage_order(request, org_id, lifecycle_id, stage_id, direction):
    
    if request.method == 'GET':
        oranization = org_models.Organization.objects.get(id=org_id)
        
        user_not_in_org = True
        
        if request.user == oranization.owner:
            user_not_in_org = False
            
        if org_models.OrganizationMember.objects.filter(organization=oranization, user=request.user).exists():
            if org_models.OrganizationMember.objects.get(organization=oranization, user=request.user).role != 'member':
                user_not_in_org = False
                
        if user_not_in_org:
            messages.error(request, 'You are not authorized to perform this action')
            return HttpResponseRedirect(reverse_lazy('lifecycle:stage_list', kwargs={'org_id': org_id, 'lifecycle_id': lifecycle_id}))
        
        
        
        stages = lifecycle_models.LifecycleStage.objects.filter(lifecycle=lifecycle_id).order_by('order_number')
        stage = lifecycle_models.LifecycleStage.objects.get(id=stage_id)
        current_stage_order = stage.order_number
        
        # revers order !!!!
        if direction == 'up':
            # increase order number by one and decrease order number of stage above by one
            stages.filter(order_number=current_stage_order-1).update(order_number=current_stage_order)
            stage.order_number = current_stage_order-1
            stage.save()

        if direction == 'down':
            # decrease order number by one and increase order number of stage below by one
            stages.filter(order_number=current_stage_order+1).update(order_number=current_stage_order)
            stage.order_number = current_stage_order+1
            stage.save()

        messages.success(request, 'Lifecycle Stage order updated successfully')
        
        return HttpResponseRedirect(reverse_lazy('lifecycles:stage_list', kwargs={'org_id': org_id, 'lifecycle_id': lifecycle_id}))