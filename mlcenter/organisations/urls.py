from django.urls import path
from . import views

app_name = 'organizations'

urlpatterns = [
    
    # organizations
    path('',                 views.OrganizationListView.as_view(), name='list'),
    path('<pk>/detail',  views.OrganizationDetailView.as_view(), name='detail'),
    path('create/',          views.OrganizationCreateView.as_view(), name='create'),
    path('<pk>/update/', views.OrganizationUpdateView.as_view(), name='update'),
    path('<pk>/delete/', views.OrganizationDeleteView.as_view(), name='delete'),
    
 
    # organization members 
    path('<org_id>/members/', views.OrganizationMemberListView.as_view(), name='member_list'),
    path('<org_id>/members/<pk>/detail', views.OrganizationMemberDetailView.as_view(), name='member_detail'),
    path('<org_id>/members/create/', views.OrganizationMemberCreateView.as_view(), name='member_create'),
    path('<org_id>/members/<pk>/update/', views.OrganizationMemberUpdateView.as_view(), name='member_update'),
    path('<org_id>/members/<pk>/delete/', views.OrganizationMemberDeleteView.as_view(), name='member_delete'),
    
    
]