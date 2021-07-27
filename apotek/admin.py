from django.contrib import admin
from .models import DataObat, StokObat, Resep

# Register your models here.
class StokObatAdmin(admin.ModelAdmin):
    search_fields = ['nama_obat__nama_obat']
    autocomplete_fields = ['nama_obat']
    list_display = ('nama_obat', 'jml')
    ordering = ['nama_obat']
    list_per_page = 50
    
class DataObatAdmin(admin.ModelAdmin):
    search_fields = ['nama_obat']
    def has_module_permission(self, request):
        return {}
    
class ResepAdmin(admin.ModelAdmin):
    search_fields = ['nama_obat']
    list_display = ('nama_obat', 'jumlah')
    ordering = ['id']
    list_per_page = 50
    actions = ['delete_selected']
    
    @admin.action(description='Hapus dan kembalikan jumlah stok')
    def delete_selected(modeladmin, request, queryset):
        for o in queryset.all():
            o.delete()
    
    
admin.site.register(DataObat, DataObatAdmin)
admin.site.register(StokObat, StokObatAdmin)
admin.site.register(Resep, ResepAdmin)