from django.db import models

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