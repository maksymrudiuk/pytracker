from django import forms
from ..models import TimeJournal


class TimeJournalForm(forms.ModelForm):
    """TimeJournalForm definition."""

    class Meta:
        """Meta definition for TimeJournalForm."""

        model = TimeJournal
        fields = ['spent_time', 'notes', ]
