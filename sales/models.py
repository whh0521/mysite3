from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.TextField()
    pname = models.TextField()
    releasedate = models.DateField()
    runningtime = models.IntegerField(default=0)
    pprice = models.IntegerField(default=0)
    imgfile = models.ImageField(null=True, blank=True)
    modify_date = models.DateTimeField(null=True, blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.type + " " + self.pname + " " + str(self.releasedate) + " " + str(self.runningtime) + "분" + " " + str(self.pprice) + "원"

class SalesInfo(models.Model):
    type = models.TextField()
    pname = models.TextField()
    pprice = models.IntegerField(default=0)
    p_date = models.DateTimeField()

    def publish(self):
        self.p_date = timezone.now()
        self.save()