from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
    text = models.CharField(max_length = 500)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    priority = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.text
