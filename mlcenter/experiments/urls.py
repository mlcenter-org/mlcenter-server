from django.urls import path
from . import views

app_name = 'experiments'

urlpatterns = [
    # Experiments
    path('<project_id>/',                 views.ExperimentListView.as_view(), name='list'),
    path('<project_id>/<pk>/detail',  views.ExperimentDetailView.as_view(), name='detail'),
    path('<project_id>/<pk>/delete/', views.ExperimentDeleteView.as_view(), name='delete'),
    path('<project_id>/<pk>/jstree/', views.jstree_experiment_artifacts, name='jstree_experiment_artifacts'),
]