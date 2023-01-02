from rest_framework import serializers
import mlcenter.mlregister.models as mlregister_models
from mlcenter.experiments import models as experiment_models

class MLRelease(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True, source='mlregister.name')
    organization = serializers.CharField(read_only=True, source='mlregister.project.owner.name')
    project = serializers.CharField(read_only=True, source='mlregister.project.name')
    version = serializers.CharField(read_only=True, source='experiment.version')
    tags = serializers.CharField(read_only=True, source='experiment.tags')
    stage = serializers.CharField(read_only=True, source='stage_name')
    artifacts = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='experiment.artifacts')
    
    
    # split tags by , and return as list
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = [x.strip() for x in representation['tags'].split(',')]
        representation['artifacts'] = [
            {
                'id': artifact_instance.id,
                'name': artifact_instance.name,
                'url': artifact_instance.artifact.url,
            }
            for artifact_instance in experiment_models.ExperimentArtifact.objects.filter(id__in=representation['artifacts'])
        ]
        
        
        
        return representation
    
    
    
    class Meta:
        model = mlregister_models.MLRelease
        fields = [
            'id',
            'name',
            'version',
            'tags',
            'project',
            'organization',
            
            'stage',
            'artifacts',
        ]

 