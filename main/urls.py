from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("q2", views.user_recommendation, name="user_recommendation"),
    path("statistics", views.data_statistics, name="data_statistics"),
]
