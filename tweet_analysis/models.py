from django.db import models

# Create your models here.


class AnalysisResult(models.Model):
    tweet_usr = models.CharField(max_length=50)
    # id_str = models.CharField(max_length=200)
    fv_max_count = models.IntegerField(default=0)
    fv_max_text = models.CharField(max_length=300)
    fv_avg = models.IntegerField(default=0)
    rt_max_count = models.IntegerField(default=0)
    rt_max_text = models.CharField(max_length=300)
    rt_avg = models.IntegerField(default=0)
    create_date = models.DateTimeField()

    def __str__(self):
        return self.tweet_usr


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)