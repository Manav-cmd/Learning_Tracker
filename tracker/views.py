from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import Sum
from .models import Topic, TopicProgress


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
# DASHBOARD (core view)
# =========================

@login_required
def dashboard(request):
    topics = Topic.objects.filter(user=request.user)

    total_topics = topics.count()
    active_topics = topics.filter(progress_entries__isnull=False).distinct().count()

    total_minutes = (
        TopicProgress.objects
        .filter(topic__user=request.user)
        .aggregate(total=Sum("effort_minutes"))["total"] or 0
    )

    context = {
        "topics": topics,
        "total_topics": total_topics,
        "active_topics": active_topics,
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
