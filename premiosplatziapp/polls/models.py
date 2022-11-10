import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date_published")

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    """ Avoid creating questions without choices"""
    # def save(self, *args, **kwargs):
    #     choices = kwargs.get('choices')
    #     if choices and len(choices) > 0:
    #         kwargs.pop('choices', None)
    #         super().save(*args, **kwargs)     
    #         for choice in choices:
    #             choice.question = self
    #             choice.save()
    #     else:
    #         raise ValueError("Should have choices")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)

    def __str__(self):
        return self.choice_text