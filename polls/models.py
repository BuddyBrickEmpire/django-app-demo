from django.db import models
from django.db.models import CASCADE


class Question(models.Model):
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class Choice(models.Model):
    question = models.ForeignKey(
        to=Question,
        on_delete=CASCADE
    )
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class Response(models.Model):
    created = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(
        to=Question,
        on_delete=CASCADE,
    )
    answer = models.ForeignKey(
        to=Choice,
        on_delete=CASCADE,
    )

