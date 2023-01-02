from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, mixins, views
import mlcenter.projects.models as projects_models
import mlcenter.mlregister.models as mlregister_models
from mlcenter.mlregister.api import serializers as mlregister_serializers

# build a get endpoint that returns the latest version of a model given project_id, model_name and stage

class MLReleaseViewset(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
    ):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = mlregister_serializers.MLRelease
    queryset = mlregister_models.MLRegister.objects.all()

    def get_queryset(self):
        super().get_queryset()
        
        
        project_id = self.kwargs['project_id']
        model_name = self.kwargs['model_name']
        stage = self.kwargs['stage']
        
        project = get_object_or_404(projects_models.Project, id=project_id)
        
        # permissions
        organization = project.owner
        user_owns_organization = organization.owner == self.request.user
        user_org_member = organization.organizationmember_set.filter(user=self.request.user)
        user_is_org_member = user_org_member.exists()
        
        
        if not user_owns_organization and not user_is_org_member:
            return []
        
        
        mlregister = get_object_or_404(mlregister_models.MLRegister, project=project, name=model_name)

        lifecycle = mlregister.lifecycle
        stage_instance = lifecycle.stages.get(name=stage)
        

        release = mlregister_models.MLRelease.objects.filter(mlregister=mlregister, stage=str(stage_instance.id), mlregister__name=model_name, mlregister__project=project).order_by('-created_at','-updated_at')
        if release.exists():
            release = release[:1]
        else:
            return []
        
        safe_to_access_release = False
        
        if not user_owns_organization and user_is_org_member:
            
            if user_org_member.role == 'owner':
                safe_to_access_release = True
            
            if user_org_member.role == 'admin' and stage_instance.roles in ['member', 'admin']:
                safe_to_access_release = True
            
            if user_org_member.role == 'member' and stage_instance.roles == 'member':
                safe_to_access_release = True
                
        if user_owns_organization:
            safe_to_access_release = True
            
        if not safe_to_access_release:
            return []
        
        return release