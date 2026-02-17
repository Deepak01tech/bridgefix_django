from django.db import models

# Create your models here.
class Urldata(models.Model):
    url = models.URLField()
    slug = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"short url for: {self.url} is {self.slug}"
