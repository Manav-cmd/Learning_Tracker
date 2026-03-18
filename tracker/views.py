from datetime import date

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SignUpForm
from .models import Topic, TopicProgress

def create_superuser_once(request):
    if User.objects.filter(is_superuser=True).exists():
        return HttpResponse("Superuser already exists")

    User.objects.create_superuser(
        username="admin",
        password="admin12345",
        email="admin@example.com"
    )

    return HttpResponse("Superuser created")

# =========================
# HOME (public)
# =========================
def home(request):
    return render(request, "home.html")


# =========================
# ABOUT (public)
# =========================
def about(request):
    return render(request, "about.html")


# =========================
# SIGNUP (public)
# =========================
def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})


# =========================
# DASHBOARD (core view)
# =========================

@login_required
def dashboard(request):
    topics = Topic.objects.filter(user=request.user).prefetch_related("progress_entries")

    total_topics = topics.count()
    in_progress = topics.filter(progress_entries__isnull=False).distinct().count()
    not_started = topics.filter(progress_entries__isnull=True).count()

    total_minutes = (
        TopicProgress.objects
        .filter(topic__user=request.user)
        .aggregate(total=Sum("effort_minutes"))["total"] or 0
    )

    context = {
        "topics": topics,
        "total_topics": total_topics,
        "in_progress": in_progress,
        "not_started": not_started,
        "total_minutes": total_minutes,
    }

    return render(request, "dashboard.html", context)

# =========================
# ADD TOPIC
# =========================
@login_required
def add_topic(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        title = request.POST.get("title")

        Topic.objects.create(
            user=request.user,
            subject=subject,
            title=title
        )
        return redirect("dashboard")

    return render(request, "add_topic.html")


# =========================
# UPDATE TOPIC
# =========================
@login_required
def update_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, user=request.user)

    if request.method == "POST":
        topic.subject = request.POST.get("subject")
        topic.title = request.POST.get("title")
        topic.save()
        return redirect("dashboard")

    return render(request, "update_topic.html", {"topic": topic})


# =========================
# DELETE TOPIC
# =========================
@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, user=request.user)
    topic.delete()
    return redirect("dashboard")


# =========================
# ADD DAILY PROGRESS
# =========================
@login_required
def add_progress(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, user=request.user)

    if request.method == "POST":
        effort = int(request.POST.get("effort"))
        note = request.POST.get("note", "")

        TopicProgress.objects.update_or_create(
            topic=topic,
            date=date.today(),
            defaults={
                "effort_minutes": effort,
                "note": note
            }
        )
        return redirect("dashboard")

    return render(request, "add_progress.html", {"topic": topic})
