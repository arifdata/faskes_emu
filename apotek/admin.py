from django.contrib import admin
from .models import DataObat, StokObat, Resep
from rangefilter.filters import DateRangeFilter

# Register your models here.
@admin.register(StokObat)
class StokObatAdmin(admin.ModelAdmin):
    def log_addition(self, *args):
        return
    def log_change(self, *args):
        return
    def log_deletion(self, *args):
        return
    search_fields = ['nama_obat__nama_obat']
    list_filter = (
            ('tgl_kadaluarsa', DateRangeFilter),
        )
    autocomplete_fields = ['nama_obat']
    list_display = ('nama_obat', 'jml', 'tgl_kadaluarsa')
    ordering = ['nama_obat__nama_obat']
    list_per_page = 50
    
@admin.register(DataObat)
class DataObatAdmin(admin.ModelAdmin):
    search_fields = ['nama_obat']
    def log_addition(self, *args):
        return
    def log_change(self, *args):
        return
    def log_deletion(self, *args):
        return
    def has_module_permission(self, request):
        return {}

@admin.register(Resep)    
class ResepAdmin(admin.ModelAdmin):
    search_fields = ['nama_obat']
    autocomplete_fields = ['nama_obat']
    list_display = ('nama_obat', 'jumlah', 'aturan_pakai', 'lama_pengobatan')
    ordering = ['id']
    list_per_page = 50
    actions = ['delete_selected']
    def log_addition(self, *args):
        return
    def log_change(self, *args):
        return
    def log_deletion(self, *args):
        return
    def has_module_permission(self, request):
        return {}
    
    @admin.action(description='Hapus dan kembalikan jumlah stok')
    def delete_selected(modeladmin, request, queryset):
        for o in queryset.all():
            o.delete()