from django.contrib import admin
from mlcenter.lifecycles import models


admin.site.register(models.Lifecycle)
admin.site.register(models.LifecycleStage)