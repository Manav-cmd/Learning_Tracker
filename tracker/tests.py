from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Topic, TopicProgress


class PublicPageTests(TestCase):
    def test_home_page_is_accessible(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_about_page_is_accessible(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)


class DashboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="password123",
        )
        self.topic_no_progress = Topic.objects.create(
            user=self.user, subject="Math", title="Algebra"
        )
        self.topic_with_progress = Topic.objects.create(
            user=self.user, subject="Science", title="Biology"
        )
        TopicProgress.objects.create(
            topic=self.topic_with_progress,
            date=date.today(),
            effort_minutes=30,
            note="Studied cells",
        )

    def test_dashboard_counts_topics_and_statuses(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_topics"], 2)
        self.assertEqual(response.context["in_progress"], 1)
        self.assertEqual(response.context["not_started"], 1)

    def test_add_progress_template_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("add_progress", args=[self.topic_no_progress.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_progress.html")
