from django.db import models

CATEGORY = (('error','エラー解決'),('meaning','意味理解'))
# Create your models here.
class SearchWord(models.Model):
  category = models.CharField(
    max_length=100,
    choices = CATEGORY 
  )
  technique = models.CharField(max_length=50)
  error_message = models.CharField(max_length=100)
  error_detail = models.CharField(max_length=250)
  Feature = models.CharField(max_length=100)
