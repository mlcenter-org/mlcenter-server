import uuid
from django.db import models
from mlcenter.projects.models import Project



class MLRegister(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    lifecycle = models.ForeignKey('lifecycles.Lifecycle', on_delete=models.CASCADE, related_name='mlregister')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class MLRelease(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True, null=True)
    
    mlregister = models.ForeignKey(MLRegister, on_delete=models.CASCADE, related_name='releases')
    experiment = models.ForeignKey('experiments.Experiment', on_delete=models.CASCADE, related_name='experiments')
    stage = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.experiment.name}[{self.mlregister.lifecycle.stages.get(id=self.stage).name}]'
    
    @property
    def stage_name(self):
        return self.mlregister.lifecycle.stages.get(id=self.stage).name
    
    @property
    def stage_id(self):
        return self.mlregister.lifecycle.stages.get(id=self.stage).id
    
    @property
    def stage_order_number(self):
        return self.mlregister.lifecycle.stages.get(id=self.stage).order_number
