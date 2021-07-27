from django.db import models
from django.db.models import F

# Create your models here.
class DataObat(models.Model):
    nama_obat = models.CharField(max_length=100, help_text="Tulis nama obat dan dosisnya", blank=False)
    SAT = (
        ('TAB', 'Tablet'),
        ('SYR', 'Sirup'),
        ('CAP', 'Kapsul'),
        ('BKS', 'Bungkus'),
        ('SAL', 'Salep'),
        ('CRM', 'Krim'),
        ('PCS', 'Pcs'),
        ('BTL', 'Botol'),
        ('SET', 'Set'),
        ('KTK', 'Kotak'),
        )
    satuan = models.CharField(max_length=3, choices=SAT, help_text="Bentuk sediaan", verbose_name="Bentuk sediaan")
    ab = models.BooleanField(help_text="Check jika termasuk antibiotik", verbose_name="Antibiotik?")
    okt = models.BooleanField(help_text="Check jika termasuk narko/psiko", verbose_name="Narkotik / Psikotropik")

    def __str__(self):
        return str(self.nama_obat)
    class Meta:
        verbose_name_plural = "Data Obat"
        
class StokObat(models.Model):
    nama_obat = models.ForeignKey('DataObat', on_delete=models.CASCADE)
    jml = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return self.nama_obat.nama_obat
    class Meta:
        verbose_name_plural = "Stok Obat"
        
class Resep(models.Model):
    nama_obat = models.ForeignKey('StokObat', on_delete=models.CASCADE)
    jumlah = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return str(self.nama_obat.nama_obat.nama_obat)
        
    def save(self, *args, **kwargs):
        reference = self.nama_obat.id
        stock = StokObat.objects.get(pk=reference)
        stock.jml = F('jml') - self.jumlah
        stock.save()
        return super(Resep, self).save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        reference = str(self.nama_obat.id)
        stock = StokObat.objects.get(pk=reference)
        stock.jml = F('jml') + self.jumlah
        stock.save()
        super(Resep, self).delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Resep"