from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Topic(models.Model):
    """
    A learning goal / topic owned by a specific user.
    Example: Subject = DSA, Title = Binary Search
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Defensive validation
        if not self.subject.strip():
            raise ValidationError({"subject": "Subject cannot be empty."})

        if not self.title.strip():
            raise ValidationError({"title": "Topic title cannot be empty."})

    def save(self, *args, **kwargs):
        # Always validate, even outside forms
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def total_days_tracked(self):
        return self.progress_entries.count()

    @property
    def total_effort_minutes(self):
        return sum(entry.effort_minutes for entry in self.progress_entries.all())

    @property
    def status(self):
        """
        Derived status (no stored progress field)
        """
        if self.progress_entries.count() == 0:
            return "Not Started"
        return "In Progress"

    def __str__(self):
        return f"{self.subject} - {self.title}"


class TopicProgress(models.Model):
    """
    A daily progress entry for a topic.
    One topic → many daily entries.
    """

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="progress_entries"
    )

    date = models.DateField(default=timezone.now)
    effort_minutes = models.PositiveIntegerField()
    note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("topic", "date")
        ordering = ["-date"]

    def clean(self):
        if self.effort_minutes <= 0:
            raise ValidationError(
                {"effort_minutes": "Effort must be greater than zero."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.topic.title} - {self.date}"
