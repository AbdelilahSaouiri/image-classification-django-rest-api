from django.db import models

class Image(models.Model):
    image=models.ImageField(upload_to="images/")
    upload_at=models.DateField(auto_now_add=True)
    title=models.CharField(max_length=80,default='')
    class Meta:
        db_table='images'
