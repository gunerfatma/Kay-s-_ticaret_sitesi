from django import forms 
from .models import Puanlama


class PuanlamaForm(forms.ModelForm):
    class Meta:
        model = Puanlama
        fields = ['subject', 'puanlama', 'degerlendirme']
