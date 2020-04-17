from django.db import models
import re
from .TextSanitize import TextSanitize

# Create your models here.

class TalkSet(models.Model):
    name = models.CharField(verbose_name="パターン名",max_length=40,blank=True)
    trigger = models.CharField(max_length=140,blank=True,null=True)
    trigger_body = models.CharField(verbose_name="キーとなるツイート",max_length=140)
    reply = models.CharField(verbose_name="応答",max_length=140)

    def __str__(self):
        return self.name
    def save(self,*args, **kwargs):
        text = self.trigger_body
        text = TextSanitize(text)
        self.trigger = text
        super(TalkSet, self).save(*args, **kwargs)
