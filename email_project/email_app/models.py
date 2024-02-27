from django.db import models


class Student(models.Model):
    roll_no = models.IntegerField()
    name = models.CharField(max_length=30)
    marks = models.FloatField()
    city = models.CharField(max_length=20)
    