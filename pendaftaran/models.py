from django.db import models
import datetime

# Create your models here.
class DataPasien(models.Model):
    no_kartu = models.CharField(max_length=20, help_text="Masukkan no BPJS / KTP", verbose_name="Nomor Kartu")
    nama_pasien = models.CharField(max_length=30, help_text="Masukkan nama", verbose_name="Nama Pasien")
    alamat = models.CharField(max_length=50, help_text="Masukkan alamat", blank=True, verbose_name="Alamat")
    usia = models.DateField(help_text="dd-mm-yy", verbose_name="Tanggal Lahir", blank=True)
    no_hp = models.CharField(max_length=15, help_text="masukkan dengan format +628XXXXXXXXXX", verbose_name="No Telepon", blank=True)
    
    def __str__(self):
        u = self.umur()
        return  str(self.nama_pasien) + " (" + u + ") " + ", " + str(self.alamat[:30])
    def umur(self):
        now = datetime.datetime.now()
        usianya = datetime.date(now.year, now.month, now.day) - self.usia
        rendering = "{}Th {}Bln".format(int(usianya.days / 365), int((usianya.days % 365) / 30))
        return str(rendering)
    umur.short_description = 'Usia'
    
    def save(self, *args, **kwargs):
        self.nama_pasien = self.nama_pasien.upper()
        self.alamat = self.alamat.upper()
        return super(DataPasien, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Data Pasien"
