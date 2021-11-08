# Generated by Django 3.2.5 on 2021-11-08 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('poli', '0003_alter_datakunjungan_no_resep'),
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
                'verbose_name_plural': 'Buku Terima Gudang',
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
                ('nama_obat', models.CharField(help_text='Tulis nama obat dan dosisnya', max_length=100)),
                ('satuan', models.CharField(choices=[('TAB', 'Tablet'), ('SYR', 'Sirup'), ('CAP', 'Kapsul'), ('BKS', 'Bungkus'), ('SAL', 'Salep'), ('CRM', 'Krim'), ('PCS', 'Pcs'), ('BTL', 'Botol'), ('SET', 'Set'), ('KTK', 'Kotak')], help_text='Bentuk sediaan', max_length=3, verbose_name='Bentuk sediaan')),
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
                ('tgl_kadaluarsa', models.DateField(verbose_name='Tanggal Kadaluarsa')),
                ('prev_saldo', models.PositiveSmallIntegerField(default=0, editable=False)),
                ('after_pengurangan_saldo', models.PositiveSmallIntegerField(default=0, editable=False)),
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
                ('prev_saldo', models.PositiveSmallIntegerField(default=0, editable=False)),
                ('after_pengurangan_saldo', models.PositiveSmallIntegerField(default=0, editable=False)),
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
                ('aturan_pakai', models.PositiveSmallIntegerField(choices=[(0, '3x1'), (1, '2x1'), (2, '1x1'), (3, 'sue'), (4, 'sprn'), (5, 'suc')], verbose_name='Aturan Pakai')),
                ('lama_pengobatan', models.PositiveSmallIntegerField(verbose_name='Lama Pengobatan (hari)')),
                ('prev_saldo', models.PositiveSmallIntegerField(default=0, editable=False)),
                ('after_pengurangan_saldo', models.PositiveSmallIntegerField(default=0, editable=False)),
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
                ('prev_saldo', models.PositiveSmallIntegerField(default=0, editable=False)),
                ('after_pengurangan_saldo', models.SmallIntegerField(default=0, editable=False)),
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
                ('tgl_kadaluarsa', models.DateField(blank=True, null=True)),
                ('prev_saldo', models.PositiveSmallIntegerField(default=0, editable=False)),
                ('after_pengurangan_saldo', models.SmallIntegerField(default=0, editable=False)),
                ('nama_barang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apotek.dataobat')),
                ('terima_barang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apotek.bukupenerimaan')),
            ],
            options={
                'verbose_name_plural': 'Item Penerimaan',
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
