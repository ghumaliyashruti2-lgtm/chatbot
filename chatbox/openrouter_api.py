from django.conf import settings
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class OpenRouterChatbot:
    def __init__(self):
        self.api_key = getattr(settings, "OPENROUTER_API_KEY", None)
        self.model = getattr(settings, "OPENROUTER_MODEL", "openai/gpt-4o-mini")

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is missing in settings or .env")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1"
        )

    def get_response(self, user_input, conversation_history):
        try:
            # Strong system instruction with explicit example
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are Elixire HelpDesk chatbot. ALWAYS reply in a clear, "
                        "point-wise format using numbered or bullet points. "
                        "Do NOT write paragraphs. Give short lines. "
                        "Example reply format:\n\n"
                        "1. First short point\n"
                        "2. Second short point\n"
                        "3. Third short point\n\n"
                        "If asked for lists, use numbered points. Keep each point <= 2 sentences."
                    )
                }
            ]

            # Add previous conversation (user/assistant pairs)
            messages += [
                {"role": msg["role"], "content": msg["content"]}
                for msg in conversation_history
            ]

            # Add the current user input
            messages.append({"role": "user", "content": user_input})

            # Call OpenRouter with deterministic settings
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.0,
                max_tokens=500,
            )

            # Defensive checks
            if (
                not response
                or not hasattr(response, "choices")
                or len(response.choices) == 0
                or not response.choices[0].message
            ):
                return "Error: AI did not return any response."

            bot_text = response.choices[0].message.content

            # LOG for debugging (inspect what the model actually returned)
            logger.debug("OpenRouter reply: %s", repr(bot_text))

            return bot_text

        except Exception as e:
            logger.exception("Error communicating with AI")
            return f"Error communicating with AI: {str(e)}"
