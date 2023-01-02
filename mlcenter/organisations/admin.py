from django.contrib import admin
from mlcenter.organisations import models

admin.site.register(models.Organization)
admin.site.register(models.OrganizationMember)