from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Topic(models.Model):
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=200)

    progress = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Defensive programming: never trust input
        if self.progress < 0 or self.progress > 100:
            raise ValidationError(
                {"progress": "Progress must be between 0 and 100."}
            )

        if not self.title.strip():
            raise ValidationError(
                {"title": "Topic title cannot be empty."}
            )

        if not self.subject.strip():
            raise ValidationError(
                {"subject": "Subject cannot be empty."}
            )

    def save(self, *args, **kwargs):
        # Enforce validation EVERY time, even outside forms
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def status(self):
        if self.progress == 100:
            return "Completed"
        elif self.progress > 0:
            return "In Progress"
        return "Not Started"

    def __str__(self):
        return f"{self.subject} - {self.title}"
