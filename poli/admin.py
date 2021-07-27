from django.contrib import admin
from .models import DataPeresep

# Register your models here.
@admin.register(DataPeresep)
class DataPeresepAdmin(admin.ModelAdmin):
	pass