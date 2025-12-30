from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.history.models import History
import json
from django.http import JsonResponse
from apps.profiles.models import Profile
from collections import defaultdict
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import CleanHistoryForm, DeleteHistoryForm

@login_required(login_url='login')
def view_history(request):

    profile, _ = Profile.objects.get_or_create(user=request.user)

    sort_option = request.GET.get("sort", "newest")

    # Always fetch messages in chronological order
    messages = History.objects.filter(
        user=request.user
    ).order_by("created_at")

    # ==========================
    # GROUP BY CHAT ID
    # ==========================
    chat_groups = defaultdict(list)

    for msg in messages:
        chat_groups[msg.chat_id].append(msg)

    history_groups = []

    # ==========================
    # SPLIT EACH CHAT INTO 10-MESSAGE GROUPS
    # ==========================
    for chat_id, msgs in chat_groups.items():

        for i in range(0, len(msgs), 10):
            chunk = msgs[i:i + 10]

            history_groups.append({
                "chat_id": chat_id,
                "start_time": chunk[0].created_at,
                "preview": chunk[0].user_message[:60],
                "count": len(chunk),
                "from_time": chunk[0].created_at.isoformat(),
            })

    # ==========================
    # SORT GROUPS
    # ==========================
    history_groups.sort(
        key=lambda x: x["start_time"],
        reverse=(sort_option == "newest")
    )

    return render(request, "root/history.html", {
        "history_groups": history_groups,
        "profile": profile,
        "sort_option": sort_option,
    })


@login_required(login_url="login")
def clean_history(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form = CleanHistoryForm(request.user, data=data)
        if form.is_valid():
            form.clean_history()
            return JsonResponse({"status": "success"})
        return JsonResponse({"error": form.errors}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required(login_url='login')
def delete_history(request, chat_id):
    if request.method == "POST":
        form = DeleteHistoryForm(request.user, {"chat_id": chat_id})
        if form.is_valid():
            form.delete_history()
            return JsonResponse({"ok": True})
        return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)
