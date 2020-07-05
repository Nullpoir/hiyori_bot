from django.db import models
from datetime import datetime

class Quiz(models.Model):
    # 基本データ
    created_at = models.DateTimeField(
        verbose_name='作成日',
        default=datetime.now
    )
    update_at = models.DateTimeField(
        verbose_name='更新日',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        verbose_name='有効',
        default=True
    )

    # クイズ
    question = models.CharField(verbose_name='問題文',max_length=131)
    answers = models.TextField(verbose_name="正解文")
    