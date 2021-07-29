from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from .models import DataPeresep, Diagnosa, DataKunjungan
from apotek.models import Resep

# Register your models here.
@admin.register(DataPeresep)
class DataPeresepAdmin(admin.ModelAdmin):
	search_fields = ['penulis_resep']
	def has_module_permission(self, request):
		return {}
	def log_addition(self, *args):
		return

@admin.register(Diagnosa)
class DiagnosaAdmin(admin.ModelAdmin):
	search_fields = ['diagnosa']
	def has_module_permission(self, request):
		return {}
	def log_addition(self, *args):
		return

class ResepInline(admin.TabularInline):
	model = Resep
	autocomplete_fields = ['nama_obat']
	extra = 5

@admin.register(DataKunjungan)
class DataKunjunganAdmin(admin.ModelAdmin):
	inlines = [ResepInline,]
	autocomplete_fields = ['nama_pasien', 'diagnosa', 'penulis_resep']
	list_display = ('nama_pasien', 'tgl_kunjungan', 'no_resep')
	list_per_page = 20
	ordering = ['-tgl_kunjungan']
	list_filter = (
            ('tgl_kunjungan', DateRangeFilter),
            ('penulis_resep'),
            ('diagnosa'),
        )
	fieldsets = [
		('Data Kunjungan', {'fields': ['nama_pasien', 'tgl_kunjungan']}),
		('Data Resep', {'fields': ['penulis_resep', 'no_resep', 'diagnosa']}),
		('Data Tambahan', {'fields': ['notes', 'file_up'], 'classes': ('collapse',)}),
	]