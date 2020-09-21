from django.db import models
import re
try:
    from app.helpers.text_sanitize import *
except ImportError:
    pass

class TalkSet(models.Model):
    name = models.CharField(verbose_name="パターン名",max_length=40,blank=True)
    trigger = models.CharField(max_length=140,blank=True,null=True)
    trigger_body = models.CharField(verbose_name="キーとなるツイート",max_length=140)
    reply = models.TextField(verbose_name="応答")

    def __str__(self):
        return self.name
    def save(self,*args, **kwargs):
        text = self.trigger_body
        text = text_sanitize(text)
        self.trigger = text
        super(TalkSet, self).save(*args, **kwargs)
