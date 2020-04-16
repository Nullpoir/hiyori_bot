from django.db import models
import re

# Create your models here.

class TalkSet(models.Model):
    name = models.CharField(verbose_name="パターン名",max_length=40,blank=True)
    trigger = models.CharField(verbose_name="キーとなるツイート",max_length=140)
    reply = models.CharField(verbose_name="応答ツイート",max_length=140)

    def __str__(self):
        return self.name
    def save():
        text = self.trigger

        text = re.sub(r'@mHiyori0324', "", text)
        text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
        text = re.sub('\n', "", text)
        text = re.sub(' ', "", text)
        text = re.sub('　', "", text)
        text = re.sub('\?', "", text)
        text = re.sub('\？', "", text)

        self.trigger = text
        super(TalkSet, self).save()
