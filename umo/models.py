from django.db import models

# Create your models here.
class Person(models.Model):
    fullname=models.CharField(max_length=255, db_index=True, blank=False, null=False)