from django.db import models
from django.db.models import F
#from poli.models import DataKunjungan

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
    is_alkes = models.BooleanField(help_text="Check jika bukan obat konsumsi / alkes", verbose_name="Alkes?")

    def __str__(self):
        return str(self.nama_obat)
    class Meta:
        verbose_name_plural = "Data Obat"
        
class StokObat(models.Model):
    nama_obat = models.ForeignKey('apotek.DataObat', on_delete=models.CASCADE)
    jml = models.SmallIntegerField(verbose_name="Jumlah")
    tgl_kadaluarsa = models.DateField(verbose_name="Tanggal Kadaluarsa")
    
    def __str__(self):
        return self.nama_obat.nama_obat
    class Meta:
        verbose_name_plural = "Stok Obat"
        
class Resep(models.Model):
    kunjungan_pasien = models.ForeignKey('poli.DataKunjungan', on_delete=models.CASCADE)
    nama_obat = models.ForeignKey('apotek.StokObat', on_delete=models.CASCADE)
    jumlah = models.PositiveSmallIntegerField(blank=False, verbose_name="Jumlah")
    ATURAN_PK = (
        (0, '3x1'),
        (1, '2x1'),
        (2, '1x1'),
        (3, 'sue'),
        (4, 'sprn'),
        (5, 'suc'),
        )
    aturan_pakai = models.PositiveSmallIntegerField(choices=ATURAN_PK, verbose_name="Aturan Pakai")
    lama_pengobatan = models.PositiveSmallIntegerField(verbose_name="Lama Pengobatan (hari)")
    prev_saldo = models.PositiveSmallIntegerField(default=0, editable=False)
    after_pengurangan_saldo = models.PositiveSmallIntegerField(default=0, editable=False)
    
    def __str__(self):
        return str(self.nama_obat.nama_obat.nama_obat)
        
    def save(self, *args, **kwargs):
        reference = self.nama_obat.id
        stock = StokObat.objects.get(pk=reference)
        self.prev_saldo = stock.jml
        self.after_pengurangan_saldo = stock.jml - self.jumlah
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

class Penerimaan(models.Model):
    terima_barang = models.ForeignKey('apotek.BukuPenerimaan', on_delete=models.CASCADE)
    nama_barang = models.ForeignKey('apotek.DataObat', on_delete=models.CASCADE)
    jumlah = models.PositiveSmallIntegerField(blank=False, verbose_name="Jumlah")
    tgl_kadaluarsa = models.DateField(null=True, blank=True)
    prev_saldo = models.PositiveSmallIntegerField(default=0, editable=False)
    after_pengurangan_saldo = models.SmallIntegerField(default=0, editable=False)

class SumberTerima(models.Model):
    nama = models.CharField(max_length=20)
    def __str__(self):
        return self.nama
    class Meta:
        verbose_name_plural = "Sumber Penerimaan"

class BukuPenerimaan(models.Model):
    tgl_terima = models.DateField(verbose_name="Tanggal Terima")
    sumber = models.ForeignKey('apotek.SumberTerima', on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    file_up = models.FileField(blank=True, upload_to='docs/%Y/%m/%d')

    class Meta:
        verbose_name_plural = "Buku Terima"