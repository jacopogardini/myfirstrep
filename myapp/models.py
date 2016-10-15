from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.urlresolvers import reverse
import datetime

class Node(MPTTModel):

    TUMOR = (
        ('S', 'Solid'),
        ('A', 'Ascites'),
    )
    SITE = (
        ('S', 'Subcute'),
        ('I', 'IpSlice'),
        ('C', 'IpCells'),
    )
    POSITION = (
        ('L', 'Left'),
        ('R', 'Right'),
    )
    TREATMENT = (
        ('N', 'No'),
        ('S', 'StartingDate'),
        ('T', 'Type'),
        ('D', 'Dose'),
        ('A', 'AdministratorRoute'),
    )
    
    name = models.CharField(default='0000000',max_length=20,unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    date = models.DateField(null=True,blank=True)
    tumor = models.CharField(max_length=1, choices=TUMOR,null=True,blank=True)
    anatomic_pathology = models.CharField(max_length=60,null=True,blank=True)
    tumor_markers = models.CharField(max_length=60,null=True,blank=True)
    site = models.CharField(max_length=1, choices=SITE,null=True,blank=True)
    position = models.CharField(max_length=1, choices=POSITION,null=True,blank=True)
    treatment = models.CharField(max_length=1, choices=TREATMENT,null=True,blank=True)
    
    age = models.IntegerField(null=True,blank=True)
    actual_state = models.CharField(max_length=60,null=True,blank=True)

    def __unicode__(self):
        return self.name

class TimeVolume(models.Model):

    time = models.IntegerField()
    volume = models.IntegerField()
    datins = models.DateTimeField(auto_now_add=True)

    node = models.ForeignKey(Node, on_delete=models.CASCADE) #1 a n

    def __unicode__(self):
        return str(self.node)
    
