from rest_framework import serializers
import mlcenter.experiments.models as experiments_models

class ExperimentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    version = serializers.CharField(read_only=True)
    
    class Meta:
        model = experiments_models.Experiment
        fields = [
            'id',
            'name',
            'description',
            'version',
            'tags',
            'metrics',
            'hyperparameters',
            'requirements',
        ]

 

class ExperimentArtifactSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    artifact = serializers.FileField()
    
    class Meta:
        model = experiments_models.ExperimentArtifact
        fields = [
            'id',
            'name',
            'artifact'
        ]
