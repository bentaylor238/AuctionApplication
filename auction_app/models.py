import datetime

from django.db import models

class Item(models.Model):
    class Meta:
        abstract = True
    title = models.CharField(max_length=200, default='')
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default='')
    date = models.DateTimeField(datetime.datetime.now(), default=datetime.datetime.now())

class SilentItem(Item):
    start = models.DateTimeField()
    end = models.DateTimeField()

class LiveItem(Item):
    orderinqueue = models.IntegerField()

class Rules(models.Model):
    title = models.CharField(max_length=200)
    lastModified = models.DateTimeField()
    rulesContent = models.TextField()
    announcementsContent = models.TextField()
    def __str__(self):
        return self.title

class User(models.Model):
    name = models.CharField(max_length=200, default='')
    username = models.CharField(max_length=200, default='')
    id = models.IntegerField(default=0)
    email = models.EmailField(max_length=200, default='')
    password = models.CharField(max_length=200, default='')
    silentItem = models.ForeignKey(SilentItem, on_delete=models.CASCADE)

class Bid(models.Model):
    amount = models.IntegerField(default=0)
    item = models.ForeignKey(SilentItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Auction(models.Model):
    items = models.ForeignKey(Item, on_delete=models.CASCADE)
    type = models.CharField(max_length=200, default='')


