from django.db import models
#from pendaftaran.models import DataPasien
from apotek.models import Resep

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
	def save(self, *args, **kwargs):
	    self.diagnosa = self.diagnosa.upper()
	    super(Diagnosa, self).save(*args, **kwargs)
	class Meta:
		verbose_name_plural = "Diagnosa"

class DataKunjungan(models.Model):
	nama_pasien = models.ForeignKey('pendaftaran.DataPasien', on_delete=models.CASCADE)
	tgl_kunjungan = models.DateField(verbose_name="Tanggal Kunjungan")
	no_resep = models.PositiveSmallIntegerField(default=0, editable=False)
	penulis_resep = models.ForeignKey('poli.DataPeresep', on_delete=models.CASCADE)
	diagnosa = models.ManyToManyField('poli.Diagnosa')
	notes = models.TextField(blank=True)
	file_up = models.FileField(blank=True, upload_to='docs/%Y/%m/%d')

	def save(self, *args, **kwargs):
	    try:
	        q = DataKunjungan.objects.filter(tgl_kunjungan=self.tgl_kunjungan)
	        self.no_resep = len(q) + 1
	        super(DataKunjungan, self).save(*args, **kwargs)
	    except DataKunjungan.DoesNotExist:
	        self.no_resep = 1
	        super(DataKunjungan, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		query_obat = Resep.objects.filter(kunjungan_pasien_id=self.id)
		for data in query_obat:
			data.delete()
		super(DataKunjungan, self).delete(*args, **kwargs)

	def __str__(self):
		return str(self.nama_pasien)
	class Meta:
		verbose_name_plural = "Data Kunjungan Pasien"
