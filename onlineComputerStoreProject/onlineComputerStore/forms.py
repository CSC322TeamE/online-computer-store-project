from onlineComputerStore.models import *
from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext_lazy as _  # translatable
# Add CPU form
from django import forms


class AddCpuForm(ModelForm):
    class Meta:
        model = CPU
        fields = ['name', 'price', 'quantity', 'discount', 'rating', 'quantity_sold', 'img', 'description',
                  'category', 'core_name', 'num_cores', 'frequency']


# Add GPU form
class AddGpuForm(ModelForm):
    class Meta:
        model = GPU
        fields = ['name', 'price', 'quantity', 'discount', 'rating', 'quantity_sold', 'img', 'description',
                  'category', 'chipset', 'num_cuda_cores', 'core_clock']


# Add memory form
class AddMemoryForm(ModelForm):
    class Meta:
        model = Memory
        fields = ['name', 'price', 'quantity', 'discount', 'rating', 'quantity_sold', 'img', 'description',
                  'capacity']


# purchase form

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
        fields = ['description']
        widgets = {
            'description': Textarea(attrs={'cols': 60, 'rows': 10}),  # change text to textarea in form.
        }
        error_messages = {
            'description': {
                'max_length': _("You write too much."),
                'required': _("You have to provide some advice.")
            },
        }
