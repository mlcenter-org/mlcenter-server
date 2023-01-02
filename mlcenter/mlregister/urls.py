from django.urls import path
from . import views

app_name = 'mlregister'

urlpatterns = [
    # MLRegister
    path('<project_id>/',             views.MLRegisterListView.as_view(),   name='list'),
    path('<project_id>/create',       views.MLRegisterCreateView.as_view(), name='create'),
    path('<project_id>/<pk>/update',  views.MLRegisterUpdateView.as_view(), name='update'),
    path('<project_id>/<pk>/detail',  views.MLRegisterDetailView.as_view(), name='detail'),
    path('<project_id>/<pk>/delete',  views.MLRegisterDeleteView.as_view(), name='delete'),
    
    
    # MLRelease
    path('<project_id>/release/create',       views.MLReleaseCreateView.as_view(), name='mlrelease_create'),
    path('<project_id>/release/<mlregister_id>/<pk>/update/<stage_id>',  views.MLReleaseUpdateView.as_view(), name='mlrelease_update'),
    
    
]