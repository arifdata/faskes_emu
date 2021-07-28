from django.db import models
from pendaftaran.models import DataPasien

# Create your models here.
class DataPeresep(models.Model):
    nama_peresep = models.CharField(max_length=30, help_text="Input nama peresep", blank=False, verbose_name="Nama Peresep")
    
    def __str__(self):
        return str(self.nama_peresep)
    class Meta:
        verbose_name_plural = "Data Peresep"

class Diagnosa(models.Model):
	diagnosa = models.CharField(max_length=50, help_text="Input nama diagnosa", blank=False, verbose_name="Diagnosa")

	def __str__(self):
		return str(self.diagnosa)
	class Meta:
		verbose_name_plural = "Diagnosa"

class DataKunjungan(models.Model):
	nama_pasien = models.ForeignKey(DataPasien, on_delete=models.CASCADE)
	tgl_kunjungan = models.DateField(verbose_name="Tanggal Kunjungan")
	no_resep = models.PositiveSmallIntegerField()
	penulis_resep = models.ForeignKey(DataPeresep, on_delete=models.CASCADE)
	diagnosa = models.ManyToManyField(Diagnosa)

	def __str__(self):
		return str(self.nama_pasien)
	class Meta:
		verbose_name_plural = "Data Kunjungan Pasien"