from django.db import models

# Create your models here.
class Crypto(models.Model):
  name = models.CharField(max_length=10)
  price = models.FloatField()
  time_lastupdate = models.DateTimeField(auto_now=True)
  slug = models.SlugField(unique=True)
  def __str__(self):
    return self.name