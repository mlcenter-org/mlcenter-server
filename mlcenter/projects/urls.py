from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    
    path('',                 views.ProjectListView.as_view(), name='list'),
    path('<pk>/detail',  views.ProjectDetailView.as_view(), name='detail'),
    path('create/',          views.ProjectCreateView.as_view(), name='create'),
    path('<pk>/update/', views.ProjectUpdateView.as_view(), name='update'),
    path('<pk>/delete/', views.ProjectDeleteView.as_view(), name='delete'),
    
]