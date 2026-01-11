from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),

    path("add/", views.add_topic, name="add_topic"),
    path("progress/", views.view_progress, name="view_progress"),

    path("update/<int:topic_id>/", views.update_topic, name="update_topic"),
    path("delete/<int:topic_id>/", views.delete_topic, name="delete_topic"),
]
