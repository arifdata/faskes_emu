from django.contrib import admin
from .models import DataPeresep, Diagnosa

# Register your models here.
@admin.register(DataPeresep)
class DataPeresepAdmin(admin.ModelAdmin):
	pass

@admin.register(Diagnosa)
class DiagnosaAdmin(admin.ModelAdmin):
	pass