from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create-superuser/", views.create_superuser_once),
    path("topic/add/", views.add_topic, name="add_topic"),
    path("topic/<int:topic_id>/edit/", views.update_topic, name="update_topic"),
    path("topic/<int:topic_id>/delete/", views.delete_topic, name="delete_topic"),
    path("topic/<int:topic_id>/progress/", views.add_progress, name="add_progress"),
]
