from django.db import models
from django.contrib.auth.hashers import check_password

class Admin(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email
