import uuid
from django.db import models


MEMBER_ROLE_CHOICES = (
     ('owner', 'Owner'),
     ('admin', 'Admin'),
     ('member', 'Member'),
 )

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey('users.User', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
    
    
class OrganizationMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.DO_NOTHING)
    role = models.CharField(max_length=255, choices=MEMBER_ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email

    class Meta:
        unique_together = ('organization', 'user')
        ordering = ['-created_at']
        verbose_name = 'Organization Member'
        verbose_name_plural = 'Organization Members'

        
