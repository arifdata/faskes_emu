from django.contrib import admin
from .models import DataObat, StokObatGudang, Resep, Penerimaan, BukuPenerimaan, SumberTerima, StokObatApotek, Pengeluaran, BukuPengeluaran, TujuanKeluar
from rangefilter.filters import DateRangeFilter

# Register your models here.
@admin.register(StokObatGudang)
class StokObatGudangAdmin(admin.ModelAdmin):
    def log_addition(self, *args):
        return
    def log_change(self, *args):
        return
    def log_deletion(self, *args):
        return
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    search_fields = ['nama_obat__nama_obat']
    list_filter = (
            ('tgl_kadaluarsa', DateRangeFilter),
        )
    autocomplete_fields = ['nama_obat']
    list_display = ('nama_obat', 'jml', 'tgl_kadaluarsa')
    ordering = ['nama_obat__nama_obat']
    list_per_page = 50

@admin.register(StokObatApotek)
class StokObatApotekAdmin(admin.ModelAdmin):
    def log_addition(self, *args):
        return
    def log_change(self, *args):
        return
    def log_deletion(self, *args):
        return
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request):
        return False
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
    ordering = ['nama_obat']
    list_display = ('nama_obat', 'satuan', 'is_non_generik', 'is_ab', 'is_okt', 'is_alkes', 'is_jkn')
    list_filter = ('satuan', 'is_non_generik', 'is_ab', 'is_okt', 'is_alkes', 'is_jkn',)
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
    actions = ['delete_selected', 'download_csv']
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

    @admin.action(description='Download CSV')
    def download_csv(modeladmin, request, queryset):
        import csv
        from django.http import HttpResponse
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="nganu.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['Nama', 'Jumlah'])
        for o in queryset.all():
            writer.writerow([o.nama_obat, o.jumlah])
        return response

@admin.register(SumberTerima)
class SumberTerimaAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return {}
    def log_addition(self, *args):
        return
    def log_change(self, *args):
        return
    def log_deletion(self, *args):
        return


class PenerimaanInline(admin.TabularInline):
    model = Penerimaan
    autocomplete_fields = ['nama_barang']
    extra = 5

class PengeluaranInline(admin.TabularInline):
    model = Pengeluaran
    autocomplete_fields = ['nama_barang']
    extra = 5

@admin.register(Penerimaan)
class PenerimaanAdmin(admin.ModelAdmin):
    search_fields = ['nama_barang__nama_obat']
    list_display = ('nama_barang', 'terima_barang', 'jumlah', 'tgl_kadaluarsa')
    def has_module_permission(self, request):
        return {}
    def log_addition(self, *args):
        return
    def log_change(self, *args):
        return
    def log_deletion(self, *args):
        return

@admin.register(BukuPenerimaan)
class BukuPenerimaanAdmin(admin.ModelAdmin):
    list_filter = (
            ('tgl_terima', DateRangeFilter),
        )
    inlines = [PenerimaanInline,]
    list_display = ('tgl_terima', 'sumber', 'notes')
    search_fields = ['sumber__nama', 'notes']
    def log_addition(self, *args):
        return
    def log_change(self, *args):
        return
    def log_deletion(self, *args):
        return
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(TujuanKeluar)
class TujuanKeluarAdmin(admin.ModelAdmin):
    search_fields = ['nama']
    def has_module_permission(self, request):
        return {}
    def log_addition(self, *args):
        return
    def log_change(self, *args):
        return
    def log_deletion(self, *args):
        return

@admin.register(BukuPengeluaran)
class BukuPengeluaranAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tujuan']
    list_display = ('tgl_keluar', 'tujuan', 'notes')
    inlines = [PengeluaranInline,]
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Pengeluaran)
class PengeluaranAdmin(admin.ModelAdmin):
    def log_addition(self, *args):
        return
    def log_change(self, *args):
        return
    def log_deletion(self, *args):
        return
    def has_module_permission(self, request):
        return {}
    def has_change_permission(self, request, obj=None):
        return False
