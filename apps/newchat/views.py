from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import uuid, base64

from apps.newchat.forms import ChatbotMessageForm
from apps.history.models import History
from apps.profiles.models import Profile
from chatbox.openrouter_api import OpenRouterChatbot

chatbot_engine = OpenRouterChatbot()

# =====================
# CHAT LIMIT CONFIG
# =====================
MAX_MESSAGES = 10
CHAT_LIMIT_HOURS = 24


@login_required(login_url="login")
def new_chatbot(request):

    # =====================
    # CHAT ID HANDLING
    # =====================
    if request.GET.get("action") == "new":
        chat_id = str(uuid.uuid4())
    else:
        chat_id = (
            request.POST.get("chat_id")
            or request.GET.get("chat_id")
            or request.session.get("chat_id")
        )

    if not chat_id:
        chat_id = str(uuid.uuid4())

    request.session["chat_id"] = chat_id

    profile = Profile.objects.get(user=request.user)

    # =====================
    # FETCH CHAT HISTORY
    # =====================
    db_history = History.objects.filter(
        user=request.user,
        chat_id=chat_id
    ).order_by("created_at")

    conversation = []
    for item in db_history:
        conversation.append({"role": "user", "content": item.user_message})
        conversation.append({"role": "assistant", "content": item.ai_message})

    # =====================
    # CHAT LIMIT (PAGE LOAD)
    # =====================
    limit_reached = False
    remaining_seconds = None
    now = timezone.now()

    window_start = now - timedelta(hours=CHAT_LIMIT_HOURS)

    recent_messages = History.objects.filter(
        user=request.user,
        chat_id=chat_id,
        created_at__gte=window_start
    ).order_by("created_at")

    user_message_count = recent_messages.count()

    if user_message_count >= MAX_MESSAGES:
        first_msg = recent_messages.first()
        expiry_time = first_msg.created_at + timedelta(hours=CHAT_LIMIT_HOURS)
        limit_reached = True
        remaining_seconds = int((expiry_time - now).total_seconds())

    # =====================
    # AJAX POST (MESSAGE SEND)
    # =====================
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":

        now = timezone.now()
        window_start = now - timedelta(hours=CHAT_LIMIT_HOURS)

        recent_messages = History.objects.filter(
            user=request.user,
            chat_id=chat_id,
            created_at__gte=window_start
        ).order_by("created_at")

        user_message_count = recent_messages.count()

        if user_message_count >= MAX_MESSAGES:
            first_msg = recent_messages.first()
            expiry_time = first_msg.created_at + timedelta(hours=CHAT_LIMIT_HOURS)
            remaining_seconds = int((expiry_time - now).total_seconds())

            return JsonResponse(
                {
                    "error": "Chat limit reached",
                    "remaining_seconds": remaining_seconds
                },
                status=403
            )

        # =====================
        # RECEIVE MESSAGE + FILE
        # =====================
        message = request.POST.get("message", "").strip()
        uploaded_file = request.FILES.get("file")

        image_base64 = None
        ai_message = message

        if uploaded_file:

            if uploaded_file.content_type.startswith("image"):
                image_base64 = base64.b64encode(uploaded_file.read()).decode("utf-8")

            elif uploaded_file.content_type.startswith("text"):
                decoded_text = uploaded_file.read().decode("utf-8", errors="ignore")[:1000]
                ai_message = (
                    f"{message}\n\n"
                    f"[Uploaded Text File]\n"
                    f"File name: {uploaded_file.name}\n"
                    f"Content preview:\n{decoded_text}"
                )

            else:
                ai_message = (
                    f"{message}\n\n"
                    f"[Uploaded File]\n"
                    f"File name: {uploaded_file.name}\n"
                    f"File type: {uploaded_file.content_type}"
                )

        # =====================
        # FORM PROCESS
        # =====================
        form = ChatbotMessageForm(
            user=request.user,
            chat_id=chat_id,
            conversation=conversation,
            data={"message": ai_message}
        )

        if form.is_valid():
            reply = form.save(
                bot_engine=chatbot_engine,
                uploaded_file=uploaded_file,
                image_base64=image_base64
            )

            return JsonResponse({
                "reply": reply,
                "file": uploaded_file.name if uploaded_file else None
            })

        return JsonResponse({"error": form.errors}, status=400)

    # =====================
    # PAGE LOAD
    # =====================
    return render(request, "root/chatbot.html", {
        "conversation": conversation,
        "profile": profile,
        "chat_id": chat_id,
        "limit_reached": limit_reached,
        "remaining_seconds": remaining_seconds,
    })
