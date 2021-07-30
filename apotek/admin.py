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
    list_display = ('nama_obat', 'jumlah', 'get_nama', 'get_alamat')
    ordering = ['id']
    list_per_page = 50
    actions = ['delete_selected']
    list_filter = (
            ('kunjungan_pasien__tgl_kunjungan', DateRangeFilter),
        )

    def get_nama(self, obj):
        return "{} ({} tahun)".format(obj.kunjungan_pasien.nama_pasien.nama_pasien, obj.kunjungan_pasien.nama_pasien.umur())
    get_nama.short_description = "Penerima Obat"

    def get_alamat(self, obj):
        return "{}".format(obj.kunjungan_pasien.nama_pasien.alamat)
    get_nama.short_description = "Alamat"

    def log_addition(self, *args):
        return
    def log_change(self, *args):
        return
    def log_deletion(self, *args):
        return
    def has_module_permission(self, request):
        return {}
    
    @admin.action(description='Hapus & kembalikan stok')
    def delete_selected(modeladmin, request, queryset):
        for o in queryset.all():
            o.delete()