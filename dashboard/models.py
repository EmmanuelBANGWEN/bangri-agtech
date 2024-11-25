from django.db import models

class Earnings(models.Model):
    monthly = models.DecimalField(max_digits=10, decimal_places=2)
    annual = models.DecimalField(max_digits=10, decimal_places=2)

class Task(models.Model):
    name = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

class Request(models.Model):
    description = models.TextField()
    status = models.CharField(max_length=20)  # e.g. 'pending', 'completed'



from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    office = models.CharField(max_length=100)
    age = models.IntegerField()
    start_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
