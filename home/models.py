from django.db import models


class Person(models.Model):
    emp_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name
