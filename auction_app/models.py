from django.db import models

class Rules(models.Model):
    title = models.CharField(max_length=50)
    lastModified = models.DateTimeField()
    rulesContent = models.TextField()
    announcementsContent = models.TextField()

    def __str__(self):
        return self.title