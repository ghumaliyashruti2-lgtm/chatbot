from django import forms
from apps.history.models import History

class ChatbotMessageForm(forms.Form):
    message = forms.CharField(max_length=5000, required=True)

    def __init__(self, user, chat_id, conversation=None, *args, **kwargs):
        """
        user: current request.user
        chat_id: current chat session ID
        conversation: list of previous messages for context
        """
        super().__init__(*args, **kwargs)
        self.user = user
        self.chat_id = chat_id
        self.conversation = conversation or []

    def clean_message(self):
        msg = self.cleaned_data.get("message", "").strip()
        if not msg:
            raise forms.ValidationError("Message cannot be empty.")
        return msg

    def save(self, bot_engine):
        """
        Saves the user message and AI response to History
        bot_engine: instance of chatbot engine (OpenRouterChatbot)
        """
        user_message = self.cleaned_data["message"]

        # Get AI reply
        ai_reply = bot_engine.get_response(user_message, self.conversation)

        # Save to History
        History.objects.create(
            user=self.user,
            chat_id=self.chat_id,
            user_message=user_message,
            ai_message=ai_reply
        )

        return ai_reply
