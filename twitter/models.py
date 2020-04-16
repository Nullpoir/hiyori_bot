from django.db import models

# Create your models here.

class TalkSet(models.Model):
    name = models.CharField(verbose_name="パターン名",max_length=40,blank=True)
    trigger = models.CharField(verbose_name="キーとなるツイート",max_length=140)
    reply = models.CharField(verbose_name="応答ツイート",max_length=140)

    def __str__(self):
        return self.name
