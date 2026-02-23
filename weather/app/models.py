from django.db import models

# Create your models here.
class Searchistory(models.Model):
    city_name = models.CharField(max_length=100)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True) 
    pressure = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)   
    searched_at = models.DateTimeField(auto_now_add=True)

    # country = models.CharField(max_length=100)
    # date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city_name} at {self.searched_at.strftime('%Y-%m-%d %H:%M:%S')}"