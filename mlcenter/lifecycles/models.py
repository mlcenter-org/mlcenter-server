import uuid
from django.db import models
from mlcenter.organisations.models import Organization, MEMBER_ROLE_CHOICES


class Lifecycle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    owner = models.ForeignKey('organisations.Organization', on_delete=models.CASCADE, related_name='lifecycles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lifecycle'
        verbose_name_plural = 'Lifecycles'
        
        
class LifecycleStage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lifecycle = models.ForeignKey(Lifecycle, on_delete=models.CASCADE, related_name='stages')
    name = models.CharField(max_length=255)
    order_number = models.IntegerField(default=0)
    roles = models.CharField(max_length=255, choices=MEMBER_ROLE_CHOICES, default='owner')    
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.lifecycle.stages.count() + 1
        super(LifecycleStage, self).save(*args, **kwargs)
    
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lifecycle Stage'
        verbose_name_plural = 'Lifecycle Stages'