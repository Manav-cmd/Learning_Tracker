from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic
from .forms import TopicForm

# =========================
# HOME
# =========================
def home(request):
    return render(request, "home.html")


# =========================
# ABOUT
# =========================
def about(request):
    return render(request, "about.html")


# =========================
# ADD TOPIC
# =========================
def add_topic(request):
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("view_progress")
    else:
        form = TopicForm()

    return render(request, "add_topic.html", {"form": form})


def update_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method == "POST":
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect("view_progress")
    else:
        form = TopicForm(instance=topic)

    return render(request, "update_topic.html", {"form": form})

# =========================
# DELETE TOPIC
# =========================
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    topic.delete()
    return redirect("view_progress")


# =========================
# VIEW PROGRESS (CORE LOGIC)
# =========================
def view_progress(request):
    topics = Topic.objects.all()

    total_topics = topics.count()

    completed = topics.filter(progress=100).count()
    in_progress = topics.filter(progress__gt=0, progress__lt=100).count()
    not_started = topics.filter(progress=0).count()

    # HARD SANITY CHECK (for your brain, not code)
    # completed + in_progress + not_started == total_topics

    context = {
        "topics": topics,
        "total_topics": total_topics,
        "completed": completed,
        "in_progress": in_progress,
        "not_started": not_started,
    }

    return render(request, "view_progress.html", context)
