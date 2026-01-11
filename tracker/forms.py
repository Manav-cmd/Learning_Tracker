from django import forms
from .models import Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["subject", "title", "progress"]

        widgets = {
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Subject"
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Topic name"
                }
            ),
            "progress": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "min": 0,
                    "max": 100
                }
            ),
        }
