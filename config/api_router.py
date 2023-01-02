from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from mlcenter.experiments.api import views as experiment_views
from mlcenter.mlregister.api import views as mlregister_views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# set regex for the uuid project_id
router.register(r"experiments/(?P<project_id>[0-9a-f-]+)", experiment_views.ExperimentViewSet, basename="log-experiments")

router.register(r"experiments/(?P<project_id>[0-9a-f-]+)/(?P<experiment_id>[0-9a-f-]+)/artifacts", experiment_views.ExperimentArtifactViewSet, basename="log-experiment-artifacts")

router.register(r"mlrelease/(?P<project_id>[0-9a-f-]+)/(?P<model_name>[a-zA-Z0-9_]+)/(?P<stage>[a-zA-Z0-9_]+)", mlregister_views.MLReleaseViewset, basename="get-ml-release")




app_name = "MLCenter API Endpoints"
urlpatterns = router.urls
