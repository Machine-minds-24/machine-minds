# dream_app/forms.py

from django import forms

class DreamAppForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))
    audio_data = forms.CharField(widget=forms.HiddenInput(), required=False) 
