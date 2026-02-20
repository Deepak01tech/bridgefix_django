from django.contrib import admin

# Register your models here.
from . import models  # Todo,User


admin.site.register(models.Todo)
# admin.site.register(models.User)
# @admin.register(User)\

