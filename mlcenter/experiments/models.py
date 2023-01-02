import uuid
from django.db import models
from mlcenter.projects.models import Project

class Experiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    version = models.CharField(max_length=100, blank=True, null=True, default='0.0.1')

    tags = models.TextField(blank=True, null=True)
    
    metrics = models.JSONField(blank=True, null=True, default=dict)
    hyperparameters = models.JSONField(blank=True, null=True, default=dict)
    requirements = models.JSONField(blank=True, null=True, default=dict)
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.DO_NOTHING, related_name='experiments')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}[{self.version}]'
    
    
    # increase version number by 1 until it reachs 100
    def increase_version(self):
        version = Experiment.objects.filter(project=self.project)
        if version.exists():
            version = version.order_by('-created_at').values_list('version', flat=True).first()
            version = version.split('.')
            version[-1] = str(int(version[-1]) + 1)
            if int(version[-1]) > 99:
                version[-1] = '0'
                version[-2] = str(int(version[-2]) + 1)
                
            self.version = '.'.join(version)
        else:
            self.version = '0.0.1'
    
    def save(self, *args, **kwargs):
        self.increase_version()
        super().save(*args, **kwargs)
    
    
    
def upload_to(instance, filename):
    return f'artifacts/{instance.experiment.id}/{filename}'
    
    
class ExperimentArtifact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    
    artifact = models.FileField(upload_to=upload_to)
    
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='artifacts')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    