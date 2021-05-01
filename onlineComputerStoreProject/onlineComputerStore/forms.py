from onlineComputerStore.models import *
from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext_lazy as _  # translatable


# Add CPU form


# Add GPU form


# Add memory form


# ...


class DiscusstionForm(ModelForm):
    class Meta:
        model = Discussion
        fields = ['discuss']
        widgets = {
            'discuss': Textarea(attrs={'cols': 60, 'rows': 10}),  # change text to textarea in form.
        }
        error_messages = {
            'discuss': {
                'max_length': _("You write too much."),
            },
        }


class FroumReportForm(ModelForm):
    class Meta:
        model = ForumWarning
        exclude = ['finalized']
        widgets = {
            'description': Textarea(attrs={'cols': 60, 'rows': 10}),  # change text to textarea in form.
        }
        error_messages = {
            'discuss': {
                'max_length': _("You write too much."),
            },
        }