import datetime
from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=200)
    telegram_id = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Shift(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        if self.status:
            return f'{self.start_time.strftime("%Y-%m-%d %H:%M")}, {self.end_time.strftime("%Y-%m-%d %H:%M")}'
        else:
            return f'{self.start_time.strftime("%Y-%m-%d %H:%M")}, смена не закончена'


class Break(models.Model):
    start_time = models.TimeField(auto_now_add=True)
    end_time = models.TimeField(auto_now=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        if self.status:
            return f'{self.start_time.strftime("%H:%M")}, {self.end_time.strftime("%H:%M")}'
        else:
            return f'{self.start_time.strftime("%H:%M")}, перерыв не закончен'


class Weekend(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date}'


class Ticket(models.Model):
    title = models.CharField(max_length=200, default=None)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=None, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.date}'