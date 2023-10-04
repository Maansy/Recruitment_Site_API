from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company/images/')
    description = models.TextField()
    employee_count = models.IntegerField()
    Linkedin = models.URLField()
    website = models.URLField()
    facebook = models.URLField()
    twitter = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['name']

