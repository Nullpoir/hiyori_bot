from django.shortcuts import render
from django.views.generic.base import TemplateView
from twitter.models import TalkSet

#ランディングページ
class IndexView(TemplateView):
    template_name = 'index.html'

    #コンテキスト挿入
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fixed_replies'] = TalkSet.objects.all()
        return context
