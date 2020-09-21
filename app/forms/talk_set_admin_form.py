from django import forms
from app.models import TalkSet

class TalkSetAdminForm(forms.ModelForm):
    trigger_body = forms.CharField(label="キーとなるツイート",widget=forms.Textarea)
    class Meta:
        model = TalkSet
        fields = '__all__'
    def clean_reply(self):
        replies = self.cleaned_data.get('reply').split(',')
        for r in replies:
            if len(r) > 140:
                raise forms.ValidationError('ツイートは140文字以内でどうぞ')

        return self.cleaned_data.get('reply')
