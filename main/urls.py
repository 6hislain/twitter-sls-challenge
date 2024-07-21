from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("heartbeat", views.heartbeat, name="heartbeat"),
    path("q2", views.user_recommendation, name="user_recommendation"),
    path("statistics", views.data_statistics, name="data_statistics"),
    path("hashtag_histogram", views.hashtag_histogram, name="hashtag_histogram"),
]
