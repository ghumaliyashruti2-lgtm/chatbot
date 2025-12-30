from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
import uuid
import json
from apps.history.models import History
from apps.newchat.models import NewChat
from chatbox.openrouter_api import OpenRouterChatbot
from apps.profiles.models import Profile
from django.contrib.auth.models import User



# ----------------------------
# CHATBOT VIEW
# ---------------------------
chatbot_engine = OpenRouterChatbot()
DAILY_CHAT_LIMIT = 10


chatbot_engine = OpenRouterChatbot()  # ✅ renamed

DAILY_CHAT_LIMIT = 10

@login_required(login_url='login')
def new_chatbot(request):

    # ✅ FIXED: New Chat
    if request.GET.get("action") == "new":
        request.session.pop("chat_id", None)

    chat_id = request.GET.get("chat_id")

    if not chat_id:
        chat_id = request.session.get("chat_id")

    if not chat_id:
        chat_id = str(uuid.uuid4())

    request.session["chat_id"] = chat_id

    profile = Profile.objects.get(user=request.user)

    db_history = History.objects.filter(
        user=request.user,
        chat_id=chat_id
    ).order_by("created_at")

    conversation = []
    for item in db_history:
        conversation.append({"role": "user", "content": item.user_message})
        conversation.append({"role": "assistant", "content": item.ai_message})

    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        data = json.loads(request.body)
        user_input = data.get("message", "").strip()

        if not user_input:
            return JsonResponse({"error": "Empty message"}, status=400)

        bot_reply = chatbot_engine.get_response(user_input, conversation)

        History.objects.create(
            user=request.user,
            chat_id=chat_id,
            user_message=user_input,
            ai_message=bot_reply
        )

        return JsonResponse({"reply": bot_reply})

    return render(request, "root/chatbot.html", {
        "conversation": conversation,
        "profile": profile,
        "chat_id": chat_id
    })  