from django.contrib.gis.db import models


class FileInfo(models.Model):
    name = models.CharField(max_length=30, unique=True)
    date = models.DateTimeField()
    
    class Meta:
        ordering = ['id']

class Node(models.Model):
    dateTimeLabel = models.DateTimeField()
    g1 = models.IntegerField()
    L = models.IntegerField()
    T = models.CharField(max_length=200)
    BAT = models.IntegerField()
    ACC = models.CharField(max_length=200)
    G4 = models.CharField(max_length=200)
    # GPS = models.GeometryField(geography=True)
    GPS = models.GeometryField()
    dist = models.FloatField(null=True)
    TEMP = models.FloatField()
    CO = models.FloatField()
    NO2 = models.FloatField()
    fileInfo = models.ForeignKey(FileInfo, on_delete=models.CASCADE)
    