from django.db import models
from django.db.models import F
from django.core.exceptions import ValidationError
import datetime
#from poli.models import DataKunjungan

# Create your models here.

class KartuStokGudang(models.Model):
    nama_obat = models.ForeignKey('apotek.DataObat', on_delete=models.CASCADE)
    tgl = models.DateField(default=datetime.date.today)
    unit = models.CharField(max_length=20, default="")
    stok_terima = models.PositiveSmallIntegerField(default=0)
    stok_keluar = models.PositiveSmallIntegerField(default=0)
    sisa_stok = models.PositiveSmallIntegerField(default=0)
    ket = models.CharField(max_length=20, default='-')

    def __str__(self):
        return self.nama_obat.nama_obat
    class Meta:
        verbose_name_plural = "Kartu Stok Gudang"

class KartuStokApotek(models.Model):
    nama_obat = models.ForeignKey('apotek.DataObat', on_delete=models.CASCADE)
    tgl = models.DateField(default=datetime.date.today)
    unit = models.CharField(max_length=20, default="")
    stok_terima = models.PositiveSmallIntegerField(default=0)
    stok_keluar = models.PositiveSmallIntegerField(default=0)
    sisa_stok = models.PositiveSmallIntegerField(default=0)
    ket = models.CharField(max_length=20, default='-')

    def __str__(self):
        return self.nama_obat.nama_obat
    class Meta:
        verbose_name_plural = "Kartu Stok Apotek"
    
class DataObat(models.Model):
    nama_obat = models.CharField(max_length=200, help_text="Tulis nama obat dan dosisnya", blank=False)
    SAT = (
        ('TAB', 'Tablet'),
        ('SYR', 'Sirup'),
        ('CAP', 'Kapsul'),
        ('BKS', 'Bungkus'),
        ('TUB', 'Tube'),
        ('CRM', 'Krim'),
        ('PCS', 'Pcs'),
        ('BTL', 'Botol'),
        ('AMP', 'Ampul'),
        ('SET', 'Set'),
        ('KTK', 'Kotak'),
        )
    satuan = models.CharField(max_length=3, choices=SAT, help_text="Bentuk sediaan", verbose_name="Bentuk sediaan")
    is_ab = models.BooleanField(help_text="Check jika termasuk antibiotik", verbose_name="Antibiotik?")
    is_okt = models.BooleanField(help_text="Check jika termasuk narko/psiko", verbose_name="Narkotik / Psikotropik?")
    is_non_generik = models.BooleanField(help_text="Check jika termasuk obat non generik", verbose_name="Non Generik?")
    is_alkes = models.BooleanField(help_text="Check jika bukan obat konsumsi / alkes", verbose_name="Alkes?")
    is_jkn = models.BooleanField(help_text="Check jika obat beli dari dana JKN", verbose_name="Dari dana JKN?")

    def __str__(self):
        return str(self.nama_obat)

    def clean(self):
        if DataObat.objects.filter(nama_obat=self.nama_obat).exists():
            raise ValidationError({'nama_obat': "Sudah ada item dengan nama yg sama"})
            
    def save(self, *args, **kwargs):
        # self.nama_obat = self.nama_obat.upper()
        return super(DataObat, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "Data Obat"

class StokObatGudang(models.Model):
    nama_obat = models.ForeignKey('apotek.DataObat', on_delete=models.CASCADE)
    jml = models.SmallIntegerField(verbose_name="Jumlah")
    tgl_kadaluarsa = models.DateField(verbose_name="Tanggal Kadaluarsa")
    
    def __str__(self):
        return self.nama_obat.nama_obat
    def get_satuan(self):
        return self.nama_obat.satuan
    get_satuan.short_description = "satuan"

    class Meta:
        verbose_name_plural = "Stok Obat Gudang"

class StokObatApotek(models.Model):
    nama_obat = models.ForeignKey('apotek.DataObat', on_delete=models.CASCADE)
    jml = models.SmallIntegerField(verbose_name="Jumlah")
    
    def __str__(self):
        return self.nama_obat.nama_obat
    class Meta:
        verbose_name_plural = "Stok Obat Apotek"

class Resep(models.Model):
    kunjungan_pasien = models.ForeignKey('poli.DataKunjungan', on_delete=models.CASCADE)
    nama_obat = models.ForeignKey('apotek.StokObatApotek', on_delete=models.CASCADE)
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
    
    def __str__(self):
        return str(self.nama_obat.nama_obat.nama_obat)

    def clean(self):
        reference = self.nama_obat.id
        stock = StokObatApotek.objects.get(pk=reference)
        if self.jumlah > stock.jml:
            raise ValidationError({'jumlah': 'Stok di apotek tidak mencukupi.'})

    def save(self, *args, **kwargs):
        reference = self.nama_obat.id
        stock = StokObatApotek.objects.get(pk=reference)
        stock.jml = F('jml') - self.jumlah
        stock.save()

        query_kartu_apt = KartuStokApotek.objects.filter(nama_obat=self.nama_obat.nama_obat)
        stok_apt_sebelum = query_kartu_apt[len(query_kartu_apt)-1]
        sisa_stok_apt = stok_apt_sebelum.sisa_stok - self.jumlah
        kartu_stok_apt_input = KartuStokApotek(nama_obat=self.nama_obat.nama_obat, tgl=self.kunjungan_pasien.tgl_kunjungan, unit=self.kunjungan_pasien.nama_pasien.nama_pasien[0:20], stok_keluar=self.jumlah, sisa_stok=sisa_stok_apt, ket=self.kunjungan_pasien.notes[0:20])
        kartu_stok_apt_input.save()
        
        super(Resep, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        reference = str(self.nama_obat.id)
        stock = StokObatApotek.objects.get(pk=reference)
        krt = KartuStokApotek.objects.filter(nama_obat=self.nama_obat.nama_obat)
        krt = krt[len(krt)-1]
        krt.delete()
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
    
    def __str__(self):
        return self.nama_barang.nama_obat

    #def clean(self):
    #    if self.jumlah < 10:
    #        raise ValidationError({'jumlah': 'jumlah dibawah 10'})

    def save(self, *args, **kwargs):
        reference = str(self.nama_barang_id)
        try:
            stock = StokObatGudang.objects.get(nama_obat_id=reference)
            query_stock_sebelum = KartuStokGudang.objects.filter(nama_obat=self.nama_barang)
            stock_sebelum = query_stock_sebelum[len(query_stock_sebelum)-1]
            sisa = stock_sebelum.sisa_stok + self.jumlah
            kartu_stok_input = KartuStokGudang(nama_obat=self.nama_barang, tgl=self.terima_barang.tgl_terima, unit=self.terima_barang.sumber.nama, stok_terima=self.jumlah, sisa_stok=sisa, ket=self.terima_barang.notes[0:20])
            kartu_stok_input.save()
            stock.jml = F('jml') + self.jumlah
            if self.tgl_kadaluarsa == None:
                self.tgl_kadaluarsa = stock.tgl_kadaluarsa
            elif self.tgl_kadaluarsa < stock.tgl_kadaluarsa:
                stock.tgl_kadaluarsa = self.tgl_kadaluarsa
            stock.save()
            super(Penerimaan, self).save(*args, **kwargs)
        except StokObatGudang.DoesNotExist:
            new_item = StokObatGudang(nama_obat=self.nama_barang, jml=self.jumlah, tgl_kadaluarsa=self.tgl_kadaluarsa)
            new_item.save()
            kartu_stok_input = KartuStokGudang(nama_obat=self.nama_barang, tgl=self.terima_barang.tgl_terima, unit=self.terima_barang.sumber, stok_terima=self.jumlah, sisa_stok=self.jumlah, ket=self.terima_barang.notes[0:20])
            kartu_stok_input.save()
            super(Penerimaan, self).save(*args, **kwargs)
       # except KartuStokGudang.DoesNotExist:
       #     kartu_stok_input = KartuStokGudang(nama_obat=self.nama_barang, tgl=self.terima_barang.tgl_terima, unit=self.terima_barang.sumber, stok_terima=self.jumlah, sisa_stok=self.jumlah, ket=self.terima_barang.notes[0:20])
       #     kartu_stok_input.save()
       #     super(Penerimaan, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        reference = str(self.nama_barang_id)
        stock = StokObatGudang.objects.get(nama_obat_id=reference)
        stock.jml = F('jml') - self.jumlah
        stock.save()
        super(Penerimaan, self).delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Item Penerimaan"

class SumberTerima(models.Model):
    nama = models.CharField(max_length=20)
    def __str__(self):
        return self.nama
        
    def save(self, *args, **kwargs):
        self.nama = self.nama.upper()
        return super(SumberTerima, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Sumber Penerimaan"

class BukuPenerimaan(models.Model):
    tgl_terima = models.DateField(verbose_name="Tanggal Terima")
    sumber = models.ForeignKey('apotek.SumberTerima', on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    file_up = models.FileField(blank=True, upload_to='docs/%Y/%m/%d')

    def __str__(self):
        return str(self.tgl_terima.strftime('%d %B %Y'))

    class Meta:
        verbose_name_plural = "Buku Penerimaan Gudang"

class TujuanKeluar(models.Model):
    nama = models.CharField(max_length=30)
    def __str__(self):
        return self.nama
    def save(self, *args, **kwargs):
        self.nama = self.nama.upper()
        return super(TujuanKeluar, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Tujuan Keluar"

class BukuPengeluaran(models.Model):
    tgl_keluar = models.DateField(verbose_name="Tanggal Keluar")
    tujuan = models.ForeignKey('apotek.TujuanKeluar', on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    file_up = models.FileField(blank=True, upload_to='docs/%Y/%m/%d')

    def __str__(self):
        return str(self.tgl_keluar.strftime('%d %B %Y'))

    class Meta:
        verbose_name_plural = "Buku Pengeluaran Gudang"

    def delete(self, *args, **kwargs):
        query_obat = Pengeluaran.objects.filter(keluar_barang_id=self.id)
        for data in query_obat:
            data.delete()
        super(BukuPengeluaran, self).delete(*args, **kwargs)

class Pengeluaran(models.Model):
    keluar_barang = models.ForeignKey('apotek.BukuPengeluaran', on_delete=models.CASCADE)
    nama_barang = models.ForeignKey('apotek.StokObatGudang', on_delete=models.CASCADE)
    jumlah = models.PositiveSmallIntegerField(blank=False, verbose_name="Jumlah")
    
    def __str__(self):
        return self.nama_barang.nama_obat.nama_obat

    def clean(self):
        reference = str(self.nama_barang.nama_obat.nama_obat)
        stock = StokObatGudang.objects.get(nama_obat__nama_obat=reference)
        if self.jumlah > stock.jml:
            raise ValidationError({'jumlah': 'Stok di gudang tidak mencukupi.'})
            
    def save(self, *args, **kwargs):
        reference = str(self.nama_barang.nama_obat.nama_obat)
        stock = StokObatGudang.objects.get(nama_obat__nama_obat=reference)
        stock.jml = F('jml') - self.jumlah
        stock.save()
        if self.keluar_barang.tujuan.nama == "APOTEK":
            ref_obat = self.nama_barang.nama_obat
            try:
                stok_apt = StokObatApotek.objects.get(nama_obat=ref_obat)

                # Query Kartu Stok Gudang
                query_stock_sebelum = KartuStokGudang.objects.filter(nama_obat=self.nama_barang.nama_obat)
                stock_sebelum = query_stock_sebelum[len(query_stock_sebelum)-1]
                sisa = stock_sebelum.sisa_stok - self.jumlah
                kartu_stok_input = KartuStokGudang(nama_obat=self.nama_barang.nama_obat, tgl=self.keluar_barang.tgl_keluar, unit=self.keluar_barang.tujuan.nama, stok_keluar=self.jumlah, sisa_stok=sisa, ket=self.keluar_barang.notes[0:20])
                kartu_stok_input.save()

                # Query Kartu Stok Apotek
                query_kartu_apt = KartuStokApotek.objects.filter(nama_obat=self.nama_barang.nama_obat)
                stok_apt_sebelum = query_kartu_apt[len(query_kartu_apt)-1]
                sisa_stok_apt = stok_apt_sebelum.sisa_stok + self.jumlah
                kartu_stok_apt_input = KartuStokApotek(nama_obat=self.nama_barang.nama_obat, tgl=self.keluar_barang.tgl_keluar, unit=self.keluar_barang.tujuan.nama, stok_terima=self.jumlah, sisa_stok=sisa_stok_apt, ket=self.keluar_barang.notes[0:20])
                kartu_stok_apt_input.save()
                
                stok_apt.jml = F('jml') + self.jumlah
                stok_apt.save()
                super(Pengeluaran, self).save(*args, **kwargs)
            except StokObatApotek.DoesNotExist:
                new_item = StokObatApotek(nama_obat=ref_obat, jml=self.jumlah)
                new_item.save()
                query_stock_sebelum = KartuStokGudang.objects.filter(nama_obat=self.nama_barang.nama_obat)
                stock_sebelum = query_stock_sebelum[len(query_stock_sebelum)-1]
                sisa = stock_sebelum.sisa_stok -self.jumlah
                kartu_stok_input = KartuStokGudang(nama_obat=self.nama_barang.nama_obat, tgl=self.keluar_barang.tgl_keluar, unit=self.keluar_barang.tujuan.nama, stok_keluar=self.jumlah, sisa_stok=sisa, ket=self.keluar_barang.notes[0:20])
                kartu_stok_input.save()

                # Query Kartu Stok Apotek
                kartu_stok_apt_input = KartuStokApotek(nama_obat=self.nama_barang.nama_obat, tgl=self.keluar_barang.tgl_keluar, unit=self.keluar_barang.tujuan.nama, stok_terima=self.jumlah, sisa_stok=self.jumlah, ket=self.keluar_barang.notes[0:20])
                kartu_stok_apt_input.save()
                super(Pengeluaran, self).save(*args, **kwargs)
        else:
            query_stock_sebelum = KartuStokGudang.objects.filter(nama_obat=self.nama_barang.nama_obat)
            stock_sebelum = query_stock_sebelum[len(query_stock_sebelum)-1]
            sisa = stock_sebelum.sisa_stok -self.jumlah
            kartu_stok_input = KartuStokGudang(nama_obat=self.nama_barang.nama_obat, tgl=self.keluar_barang.tgl_keluar, unit=self.keluar_barang.tujuan.nama, stok_keluar=self.jumlah, sisa_stok=sisa, ket=self.keluar_barang.notes[0:20])
            kartu_stok_input.save()
        super(Pengeluaran, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        reference = str(self.nama_barang_id)
        stock = StokObatGudang.objects.get(nama_obat_id=reference)
        stock.jml = F('jml') + self.jumlah
        stock.save()
        super(Pengeluaran, self).delete(*args, **kwargs)
        #print(self.keluar_barang.id)
    class Meta:
        verbose_name_plural = "Item Keluar"
