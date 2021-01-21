from django.db import models

# Create your models here.
from django.db.models import SET_NULL


class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_count(self):
        return Student.objects.filter(course=self).count()


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    course = models.ForeignKey(Course,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='students')

    def __str__(self):
        return self.name
