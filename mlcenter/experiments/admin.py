from django.contrib import admin
from mlcenter.experiments import models as experiment_models


admin.site.register(experiment_models.Experiment)
admin.site.register(experiment_models.ExperimentArtifact)