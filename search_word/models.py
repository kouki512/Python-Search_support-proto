from django.db import models

TECHNIQUE = (('rails','Ruby on Rails'),('django','Django'))
# Create your models here.
class SearchWord(models.Model):
  technique = models.CharField(
    max_length = 30,
    choices = TECHNIQUE
  )
  error_message = models.TextField(max_length=1000)
  Feature = models.CharField(max_length=100)
