from django import forms
from .models import TalkSet

class TalkSetAdminForm(forms.ModelForm):
    trigger_body = forms.CharField(label="キーとなるツイート",widget=forms.Textarea)
    reply = forms.CharField(label="応答ツイート",widget=forms.Textarea)
    class Meta:
        model = TalkSet
        fields = '__all__'
