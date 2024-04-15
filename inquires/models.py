from django.db import models


class inquires(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField(blank=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.email
