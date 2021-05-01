from django import forms
from django.forms import ModelForm
from onlineComputerStore.models import CPU, GPU, Memory


# Add CPU form
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