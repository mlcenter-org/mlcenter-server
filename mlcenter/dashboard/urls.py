from django.urls import path
from mlcenter.dashboard import views


app_name = "dashboard"


urlpatterns = [
    path("", views.DashboardView.as_view(), name="home"),
]
