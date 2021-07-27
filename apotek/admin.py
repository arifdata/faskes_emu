from django.contrib import admin
from .models import DataObat, StokObat, Resep

# Register your models here.
@admin.register(StokObat)
class StokObatAdmin(admin.ModelAdmin):
    search_fields = ['nama_obat__nama_obat']
    autocomplete_fields = ['nama_obat']
    list_display = ('nama_obat', 'jml', 'tgl_kadaluarsa')
    ordering = ['nama_obat']
    list_per_page = 50
    
@admin.register(DataObat)
class DataObatAdmin(admin.ModelAdmin):
    search_fields = ['nama_obat']
    def has_module_permission(self, request):
        return {}

@admin.register(Resep)    
class ResepAdmin(admin.ModelAdmin):
    search_fields = ['nama_obat']
    autocomplete_fields = ['nama_obat']
    list_display = ('nama_obat', 'jumlah')
    ordering = ['id']
    list_per_page = 50
    actions = ['delete_selected']
    
    @admin.action(description='Hapus dan kembalikan jumlah stok')
    def delete_selected(modeladmin, request, queryset):
        for o in queryset.all():
            o.delete()