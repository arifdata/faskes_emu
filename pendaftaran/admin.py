from django.contrib import admin
from .models import DataPasien
from django.contrib.auth.models import User, Group

# Register your models here.
@admin.register(DataPasien)
class DataPasienAdmin(admin.ModelAdmin):
    search_fields = ['nama_pasien', 'no_hp', 'no_kartu', 'alamat']
    list_display = ('nama_pasien', 'umur', 'alamat', 'no_hp')
    ordering = ['nama_pasien']
    list_per_page = 50
    
    def log_addition(self, *args):
        return
    def log_change(self, *args):
        return
    def log_deletion(self, *args):
        return


admin.site.unregister(User)
admin.site.unregister(Group)