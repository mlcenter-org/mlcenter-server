from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, mixins
import mlcenter.projects.models as projects_models
import mlcenter.experiments.models as experiments_models
from .serializers import ExperimentSerializer, ExperimentArtifactSerializer
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser


class ExperimentViewSet(
        mixins.CreateModelMixin,
        viewsets.GenericViewSet
    ):
    serializer_class = ExperimentSerializer
    lookup_field='id'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        
        return experiments_models.Experiment.objects.filter(
            user=self.request.user, 
            project__id=self.kwargs['project_id']
        )
        
        
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
 
 
    def perform_create(self, serializer):

        return serializer.save(
            user=self.request.user,
            project=get_object_or_404(projects_models.Project, id=self.kwargs['project_id'])
        )
       
        
class ExperimentArtifactViewSet(
        mixins.CreateModelMixin,
        viewsets.GenericViewSet
    ):
    serializer_class = ExperimentArtifactSerializer
    lookup_field='id'
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def get_queryset(self):
        
        return experiments_models.ExperimentArtifact.objects.filter(
            experiement__project_id=self.kwargs['project_id'],
            experiment_id=self.kwargs['experiment_id'],
            id=self.kwargs['id']
        )
        
    def perform_create(self, serializer):
        artifact = self.request.FILES.get('artifact')

        if artifact is None:
            return Response({'error': 'No artifact uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        return serializer.save(
            experiment=get_object_or_404(experiments_models.Experiment, id=self.kwargs['experiment_id']),
            artifact=artifact
        )
       
        
