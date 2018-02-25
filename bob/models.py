from django.db import models


class Tasks(models.Model):
    name = models.CharField(max_length=32)
    cdate = models.DateTimeField('date create')
    fields = models.CharField(max_length=2048)


class BobTasks(models.Model):
    name = models.CharField(max_length=32)
    cdate = models.DateTimeField('date create')
    udate = models.DateTimeField('date create')
    para = models.CharField(max_length=2048, default="")
    input_file = models.CharField(max_length=256, default="")
    output_file = models.CharField(max_length=256, default="")
    output = models.CharField(max_length=2048, default="")
    status = models.IntegerField(default=0)  # 0: unfinished 1: finished
