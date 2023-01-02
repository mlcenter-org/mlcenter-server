import json
from django.views.generic import TemplateView
from mlcenter.projects import models as project_models
from mlcenter.experiments import models as experiment_models
from mlcenter.organisations import models as organisation_models
from mlcenter.mlregister import models as mlregister_models
from django.db.models import Count, Q, Aggregate



class DashboardView(TemplateView):
    template_name = "dashboard/home.html"
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        owned_orgs = organisation_models.Organization.objects.filter(owner_id=self.request.user.id)
        part_of_orgs = organisation_models.OrganizationMember.objects.filter(user=self.request.user)
        org_ids = list(set([org.id for org in owned_orgs] + [org.organization.id for org in part_of_orgs]))
        
        projects = project_models.Project.objects.filter(owner_id__in=org_ids)
        experiments = experiment_models.Experiment.objects.filter(project__in=projects)
        releases = mlregister_models.MLRelease.objects.filter(experiment__in=experiments)

        context['number_of_projects'] = projects.count()
        context['number_of_releases'] = releases.count()
        context['number_of_organizations'] = len(org_ids)
        
        context['number_of_experiments_by_project'] = json.dumps(list(experiment_models.Experiment.objects.filter(project__in=projects).values('project').annotate(total=Count('id')).values('project__name', 'total')))
        context['number_of_releases_by_project'] = json.dumps(list(releases.values('experiment__project__name').annotate(total=Count('id')).values('experiment__project__name', 'total')))
        
        
        
        return context