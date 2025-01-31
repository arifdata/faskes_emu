# Generated by Django 3.2.5 on 2024-02-22 23:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('poli', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BukuPenerimaan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tgl_terima', models.DateField(verbose_name='Tanggal Terima')),
                ('notes', models.TextField(blank=True)),
                ('file_up', models.FileField(blank=True, upload_to='docs/%Y/%m/%d')),
            ],
            options={
                'verbose_name_plural': 'Buku Penerimaan Gudang',
            },
        ),
        migrations.CreateModel(
            name='BukuPengeluaran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tgl_keluar', models.DateField(verbose_name='Tanggal Keluar')),
                ('notes', models.TextField(blank=True)),
                ('file_up', models.FileField(blank=True, upload_to='docs/%Y/%m/%d')),
            ],
            options={
                'verbose_name_plural': 'Buku Pengeluaran Gudang',
            },
        ),
        migrations.CreateModel(
            name='DataObat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_obat', models.CharField(help_text='Tulis nama obat dan dosisnya', max_length=200)),
                ('satuan', models.CharField(choices=[('TAB', 'Tablet'), ('SYR', 'Sirup'), ('CAP', 'Kapsul'), ('BKS', 'Bungkus'), ('TUB', 'Tube'), ('CRM', 'Krim'), ('PCS', 'Pcs'), ('BTL', 'Botol'), ('AMP', 'Ampul'), ('SET', 'Set'), ('KTK', 'Kotak')], help_text='Bentuk sediaan', max_length=3, verbose_name='Bentuk sediaan')),
                ('is_ab', models.BooleanField(help_text='Check jika termasuk antibiotik', verbose_name='Antibiotik?')),
                ('is_okt', models.BooleanField(help_text='Check jika termasuk narko/psiko', verbose_name='Narkotik / Psikotropik?')),
                ('is_non_generik', models.BooleanField(help_text='Check jika termasuk obat non generik', verbose_name='Non Generik?')),
                ('is_alkes', models.BooleanField(help_text='Check jika bukan obat konsumsi / alkes', verbose_name='Alkes?')),
                ('is_jkn', models.BooleanField(help_text='Check jika obat beli dari dana JKN', verbose_name='Dari dana JKN?')),
            ],
            options={
                'verbose_name_plural': 'Data Obat',
            },
        ),
        migrations.CreateModel(
            name='SumberTerima',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Sumber Penerimaan',
            },
        ),
        migrations.CreateModel(
            name='TujuanKeluar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Tujuan Keluar',
            },
        ),
        migrations.CreateModel(
            name='StokObatGudang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jml', models.SmallIntegerField(verbose_name='Jumlah')),
                ('tgl_kadaluarsa', models.DateField(blank=True, null=True, verbose_name='Tanggal Kadaluarsa')),
                ('nama_obat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apotek.dataobat')),
            ],
            options={
                'verbose_name_plural': 'Stok Obat Gudang',
            },
        ),
        migrations.CreateModel(
            name='StokObatApotek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jml', models.SmallIntegerField(verbose_name='Jumlah')),
                ('nama_obat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apotek.dataobat')),
            ],
            options={
                'verbose_name_plural': 'Stok Obat Apotek',
            },
        ),
        migrations.CreateModel(
            name='Resep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jumlah', models.PositiveSmallIntegerField(verbose_name='Jumlah')),
                ('aturan_pakai', models.CharField(blank=True, help_text='Aturan pakai obat', max_length=10, null=True)),
                ('lama_pengobatan', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Lama Pengobatan (hari)')),
                ('kunjungan_pasien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poli.datakunjungan')),
                ('nama_obat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apotek.stokobatapotek')),
            ],
            options={
                'verbose_name_plural': 'Resep',
            },
        ),
        migrations.CreateModel(
            name='Pengeluaran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jumlah', models.PositiveSmallIntegerField(verbose_name='Jumlah')),
                ('keluar_barang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apotek.bukupengeluaran')),
                ('nama_barang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apotek.stokobatgudang')),
            ],
            options={
                'verbose_name_plural': 'Item Keluar',
            },
        ),
        migrations.CreateModel(
            name='Penerimaan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jumlah', models.PositiveSmallIntegerField(verbose_name='Jumlah')),
                ('tgl_kadaluarsa', models.DateField(blank=True, help_text='Isi tgl kadaluarsa, jika tdk ada kosongkan', null=True, verbose_name='Tanggal Kadaluarsa')),
                ('no_batch', models.CharField(blank=True, help_text='Isi no batch, jika tdk ada kosongkan', max_length=30, null=True, verbose_name='Nomor Batch')),
                ('nama_barang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apotek.dataobat')),
                ('terima_barang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apotek.bukupenerimaan')),
            ],
            options={
                'verbose_name_plural': 'Item Penerimaan',
            },
        ),
        migrations.CreateModel(
            name='KartuStokGudang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tgl', models.DateField(default=datetime.date.today)),
                ('unit', models.CharField(default='', max_length=20)),
                ('stok_terima', models.PositiveSmallIntegerField(default=0)),
                ('stok_keluar', models.PositiveSmallIntegerField(default=0)),
                ('sisa_stok', models.SmallIntegerField(default=0)),
                ('ket', models.CharField(default='-', max_length=20)),
                ('nama_obat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apotek.dataobat')),
            ],
            options={
                'verbose_name_plural': 'Kartu Stok Gudang',
            },
        ),
        migrations.CreateModel(
            name='KartuStokApotek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tgl', models.DateField(default=datetime.date.today)),
                ('unit', models.CharField(default='', max_length=20)),
                ('stok_terima', models.PositiveSmallIntegerField(default=0)),
                ('stok_keluar', models.PositiveSmallIntegerField(default=0)),
                ('sisa_stok', models.SmallIntegerField(default=0)),
                ('ket', models.CharField(default='-', max_length=20)),
                ('ref', models.PositiveIntegerField(blank=True, null=True)),
                ('nama_obat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apotek.dataobat')),
            ],
            options={
                'verbose_name_plural': 'Kartu Stok Apotek',
            },
        ),
        migrations.AddField(
            model_name='bukupengeluaran',
            name='tujuan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apotek.tujuankeluar'),
        ),
        migrations.AddField(
            model_name='bukupenerimaan',
            name='sumber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apotek.sumberterima'),
        ),
    ]
