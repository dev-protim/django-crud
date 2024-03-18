from django.contrib import admin
from .models import Employees

# Register your models here.
models_list = [Employees]
admin.site.register(models_list)