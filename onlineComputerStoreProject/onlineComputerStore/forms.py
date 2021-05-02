from onlineComputerStore.models import *
from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext_lazy as _  # translatable
from django.db.models import Q
# Add CPU form
from django import forms


class AddCpuForm(ModelForm):
    class Meta:
        model = CPU
        fields = ['name', 'brand', 'price', 'quantity', 'discount', 'rating', 'quantity_sold', 'img', 'description',
                  'architecture', 'num_cores', 'frequency']


# Add GPU form
class AddGpuForm(ModelForm):
    class Meta:
        model = GPU
        fields = ['name', 'brand', 'price', 'quantity', 'discount', 'rating', 'quantity_sold', 'img', 'description',
                  'chipset', 'num_cuda_cores', 'core_clock']


# Add memory form
class AddMemoryForm(ModelForm):
    class Meta:
        model = Memory
        fields = ['name', 'brand', 'price', 'quantity', 'discount', 'rating', 'quantity_sold', 'img', 'description',
                  'capacity']


class DiscussionForm(ModelForm):
    class Meta:
        model = Discussion
        fields = ['discuss']
        widgets = {
            'discuss': Textarea(attrs={'class': 'login-input', 'cols': 60, 'rows': 10}),
            # change text to textarea in form.
        }
        error_messages = {
            'discuss': {
                'max_length': _("You write too much."),
            },
        }


class ForumReportForm(ModelForm):
    class Meta:
        model = ForumWarning
        fields = ['description']
        widgets = {
            'description': Textarea(attrs={'class': 'login-input', 'cols': 60, 'rows': 10}),
            # change text to textarea in form.
        }
        error_messages = {
            'description': {
                'max_length': _("You write too much."),
                'required': _("You have to provide some advice.")
            },
        }


# purchase form
class CreditCardForm(ModelForm):
    class Meta:
        model = CreditCard
        fields = ['name', 'card_number', 'csc', 'expired_date']

    def clean(self):
        clean_data = super().clean()
        if not CreditCard.objects.filter(Q(name=self.data['name']) & Q(card_number=self.data['card_number']) & Q(csc=self.data['csc'])).exists():
            raise forms.ValidationError(message="not valid credit card")

        return clean_data


# create transaction form
class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['address']
