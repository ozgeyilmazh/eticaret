from django.db import models

# Create your models here.

# About
class About(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

# Contact    
class Contact(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=30)
    cover_image = models.ImageField(null=True, blank=True, upload_to='about')
    def __str__(self):
        return self.title
