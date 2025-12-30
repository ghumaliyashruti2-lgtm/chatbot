from django import forms
from apps.history.models import History
from django.utils.timezone import localdate
from datetime import timedelta
from django.utils import timezone

RANGE_CHOICES = (
    ('day', 'Day'),
    ('week', 'Week'),
    ('month', 'Month'),
    ('all', 'All'),
)
class CleanHistoryForm(forms.Form):
    range_type = forms.ChoiceField(choices=RANGE_CHOICES)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_history(self):
        range_type = self.cleaned_data["range_type"]
        today = localdate()

        qs = History.objects.filter(user=self.user)

        if range_type == "day":
            qs = qs.filter(created_at__date=today)

        elif range_type == "week":
            week_start = today - timedelta(days=today.weekday())
            qs = qs.filter(created_at__date__gte=week_start)

        elif range_type == "month":
            qs = qs.filter(
                created_at__year=today.year,
                created_at__month=today.month
            )

        elif range_type == "all":
            pass

        qs.delete()

class DeleteHistoryForm(forms.Form):
    chat_id = forms.CharField()

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_chat_id(self):
        chat_id = self.cleaned_data.get("chat_id")
        if not History.objects.filter(user=self.user, chat_id=chat_id).exists():
            raise forms.ValidationError("Chat ID does not exist for this user!")
        return chat_id

    def delete_history(self):
        chat_id = self.cleaned_data.get("chat_id")
        History.objects.filter(user=self.user, chat_id=chat_id).delete()
        return True
