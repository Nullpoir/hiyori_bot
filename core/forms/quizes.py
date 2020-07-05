from django import forms
from core.models import Quiz

class QuizAdminForm(forms.ModelForm):
    question = forms.CharField(label="問題文",widget=forms.Textarea)
    class Meta:
        model = Quiz
        fields = '__all__'
    def clean_answer(self):
        answers = self.cleaned_data.get('answers').split(',')
        for a in answers:
            if len(a) > 140:
                raise forms.ValidationError('ツイートは140文字以内です')

        return self.cleaned_data.get('answers')
