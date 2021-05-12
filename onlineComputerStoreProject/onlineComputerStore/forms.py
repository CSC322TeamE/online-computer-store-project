from onlineComputerStore.models import *
from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext_lazy as _  # translatable
from django.db.models import Q
from django import forms


# Add CPU Form
class AddCpuForm(ModelForm):
    class Meta:
        model = CPU
        fields = ['name', 'brand', 'price', 'quantity', 'discount', 'img', 'description',
                  'architecture', 'num_cores', 'frequency']


# Add GPU form
class AddGpuForm(ModelForm):
    class Meta:
        model = GPU
        fields = ['name', 'brand', 'price', 'quantity', 'discount', 'img', 'description',
                  'chipset', 'num_cuda_cores', 'core_clock', 'memory_size']


# Add memory form
class AddMemoryForm(ModelForm):
    class Meta:
        model = Memory
        fields = ['name', 'brand', 'price', 'quantity', 'discount', 'img', 'description',
                  'capacity', 'type', 'frequency']


class AddHddForm(ModelForm):
    class Meta:
        model = HDD
        fields = ['name', 'brand', 'price', 'quantity', 'discount', 'img', 'description',
                  'capacity', 'rpm']


class AddMonitorForm(ModelForm):
    class Meta:
        model = Monitor
        fields = ['name', 'brand', 'price', 'quantity', 'discount', 'img', 'description',
                  'screen_size', 'resolution', 'refresh_rate']


class AddBatteryForm(ModelForm):
    class Meta:
        model = Battery
        fields = ['name', 'brand', 'price', 'quantity', 'discount', 'img', 'description',
                  'capacity']


class AddComputerForm(ModelForm):
    class Meta:
        model = Computer
        fields = ['name', 'brand', 'price', 'quantity', 'discount', 'img', 'description',
                  'os', 'computer_cpu', 'computer_gpu', 'computer_memory', 'computer_hdd', 'computer_monitor', 'computer_battery']

    def __init__(self, *args, **kwargs):
        super(AddComputerForm, self).__init__(*args, **kwargs)
        self.fields['computer_cpu'].label_from_instance = lambda obj: "%s" % obj.name
        self.fields['computer_gpu'].label_from_instance = lambda obj: "%s" % obj.name
        self.fields['computer_memory'].label_from_instance = lambda obj: "%s" % obj.name
        self.fields['computer_hdd'].label_from_instance = lambda obj: "%s" % obj.name
        self.fields['computer_monitor'].label_from_instance = lambda obj: "%s" % obj.name
        self.fields['computer_battery'].label_from_instance = lambda obj: "%s" % obj.name


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


# component chosen form for filter computer
class FilterComputerForm(forms.Form):
    os = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    purpose = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    architecture = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    cpu = forms.ModelChoiceField(queryset=None, required=False)
    gpu = forms.ModelChoiceField(queryset=None, required=False)
    memory = forms.ModelChoiceField(queryset=None, required=False)
    hdd = forms.ModelChoiceField(queryset=None, required=False)
    monitor = forms.ModelChoiceField(queryset=None, required=False)
    battery = forms.ModelChoiceField(queryset=None, required=False)
    items = Computer.objects.all()

    def __init__(self, *args, **kwargs):
        super(FilterComputerForm, self).__init__(*args, **kwargs)

        # filter computer by input
        # filter os
        if self.has_data("os"):
            self.items = self.items.filter(os=self.data["os"])

        # filter by purpose
        # A gaming computer's cpu frequency >= 3.0, gpu core clock >= 1500, memory capacity >= 8
        # ...
        if self.has_data("purpose"):
            if self.data["purpose"] == "gaming":
                self.items = self.items.filter(Q(computer_cpu__frequency__gte=3.0) &
                                               Q(computer_gpu__core_clock__gte=1500) &
                                               Q(computer_memory__capacity__gte=8))

            if self.data["purpose"] == 'business':
                self.items = self.items.filter(Q(computer_cpu__frequency__gte=2.0) &
                                               Q(price__lte=1000))

            if self.data["purpose"] == "computing":
                self.items = self.items.filter(Q(computer_cpu__frequency__gte=3.0) &
                                               Q(computer_cpu__num_cores__gte=8) &
                                               Q(computer_memory__capacity__gte=8))

        if self.has_data("architecture"):
            self.items = self.items.filter(computer_cpu__architecture=self.data["architecture"])

        # A better gpu should have a better battery or have no battery
        if self.has_data("gpu"):
            if self.data["gpu"].power > 200:
                self.items = self.items.filter(Q(computer_battery__capacity__gte=4000) | Q(computer_battery__capacity=None))

        # get filtered computer's cpu to options
        id_list = self.items.distinct().order_by('computer_cpu').values_list('computer_cpu')
        self.fields["cpu"].queryset = CPU.objects.filter(id__in=id_list)
        self.fields["cpu"].label_from_instance = lambda obj: "%s" % obj.name

        id_list = self.items.distinct().order_by('computer_gpu').values_list('computer_gpu')
        self.fields["gpu"].queryset = GPU.objects.filter(id__in=id_list)
        self.fields["gpu"].label_from_instance = lambda obj: "%s" % obj.name

        id_list = self.items.distinct().order_by('computer_memory').values_list('computer_memory')
        self.fields["memory"].queryset = Memory.objects.filter(id__in=id_list)
        self.fields["memory"].label_from_instance = lambda obj: "%s" % obj.name

        id_list = self.items.distinct().order_by('computer_hdd').values_list('computer_hdd')
        self.fields["hdd"].queryset = HDD.objects.filter(id__in=id_list)
        self.fields["hdd"].label_from_instance = lambda obj: "%s" % obj.name

        id_list = self.items.distinct().order_by('battery').values_list('battery')
        self.fields["battery"].queryset = Battery.objects.filter(id__in=id_list)
        self.fields["battery"].label_from_instance = lambda obj: "%s" % obj.name

        id_list = self.items.distinct().order_by('monitor').values_list('monitor')
        self.fields["monitor"].queryset = Monitor.objects.filter(id__in=id_list)
        self.fields["monitor"].label_from_instance = lambda obj: "%s" % obj.name

    def has_data(self, s):
        if s not in self.data:
            return False

        if not self.data[s]:
            return False

        return True

    # get items queryset
    def get_items(self):
        if self.has_data('cpu'):
            self.items = self.items.filter(computer_cpu=self.data["cpu"])

        if self.has_data('gpu'):
            self.items = self.items.filter(computer_gpu=self.data["gpu"])

        if self.has_data('memory'):
            self.items = self.items.filter(computer_memory=self.data["memory"])

        if self.has_data('hdd'):
            self.items = self.items.filter(computer_memory=self.data["hdd"])

        if self.has_data('monitor'):
            self.items = self.items.filter(computer_memory=self.data["monitor"])

        if self.has_data('battery'):
            self.items = self.items.filter(computer_memory=self.data["battery"])

        return self.items


class SuggestedItemForm(ModelForm):
    class Meta:
        model = SuggestedItem
        fields = ['item1', 'item2', 'item3']

    def __init__(self, *args, **kwargs):
        super(SuggestedItemForm, self).__init__(*args, **kwargs)

        self.fields['item1'].queryset = Item.objects.all()
        self.fields['item2'].queryset = Item.objects.all()
        self.fields['item3'].queryset = Item.objects.all()

        self.fields['item1'].label_from_instance = lambda obj: "%s" % obj.name
        self.fields['item2'].label_from_instance = lambda obj: "%s" % obj.name
        self.fields['item3'].label_from_instance = lambda obj: "%s" % obj.name






