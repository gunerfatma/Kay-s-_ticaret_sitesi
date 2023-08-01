from django import forms
from .models import Siparis


class SiparisForm(forms.ModelForm):
    class Meta:
        model = Siparis
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note']