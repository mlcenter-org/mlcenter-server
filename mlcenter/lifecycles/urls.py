from django.urls import path
from . import views

app_name = 'lifecycles'

urlpatterns = [
    
    
    # Lifecycle
    path('<org_id>/',                 views.LifecycleListView.as_view(), name='list'),
    path('<org_id>/<pk>/detail',  views.LifecycleDetailView.as_view(), name='detail'),
    path('<org_id>/create/',          views.LifecycleCreateView.as_view(), name='create'),
    path('<org_id>/<pk>/update/', views.LifecycleUpdateView.as_view(), name='update'),
    path('<org_id>/<pk>/delete/', views.LifecycleDeleteView.as_view(), name='delete'),
    
    # Lifecycle Stage
    path('<org_id>/<lifecycle_id>/stage/', views.LifecycleStageListView.as_view(), name='stage_list'),
    path('<org_id>/<lifecycle_id>/stage/<pk>/detail', views.LifecycleStageDetailView.as_view(), name='stage_detail'),
    path('<org_id>/<lifecycle_id>/stage/create/', views.LifecycleStageCreateView.as_view(), name='stage_create'),
    path('<org_id>/<lifecycle_id>/stage/<pk>/update/', views.LifecycleStageUpdateView.as_view(), name='stage_update'),
    path('<org_id>/<lifecycle_id>/stage/<pk>/delete/', views.LifecycleStageDeleteView.as_view(), name='stage_delete'),
    path('<org_id>/<lifecycle_id>/stage/<stage_id>/<direction>/', views.update_lifecycle_stage_order, name='stage_move'),
    
]