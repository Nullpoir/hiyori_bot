from django import forms
from .models import TalkSet

class TalkSetAdminForm(forms.ModelForm):
    trigger = forms.CharField(widget=forms.Textarea)
    reply = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = TalkSet
        fields = '__all__'
