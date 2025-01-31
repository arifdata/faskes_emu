# Generated by Django 3.2.5 on 2024-02-22 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pendaftaran', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataPeresep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_peresep', models.CharField(help_text='Input nama peresep', max_length=50, verbose_name='Nama Peresep')),
            ],
            options={
                'verbose_name_plural': 'Data Peresep',
            },
        ),
        migrations.CreateModel(
            name='Diagnosa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosa', models.CharField(help_text='Input nama diagnosa', max_length=200, verbose_name='Diagnosa')),
            ],
            options={
                'verbose_name_plural': 'Diagnosa',
            },
        ),
        migrations.CreateModel(
            name='DataKunjungan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tgl_kunjungan', models.DateField(verbose_name='Tanggal Kunjungan')),
                ('no_resep', models.PositiveSmallIntegerField(default=0, editable=False)),
                ('notes', models.TextField(blank=True)),
                ('file_up', models.FileField(blank=True, upload_to='docs/%Y/%m/%d')),
                ('diagnosa', models.ManyToManyField(to='poli.Diagnosa')),
                ('nama_pasien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pendaftaran.datapasien')),
                ('penulis_resep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poli.dataperesep')),
            ],
            options={
                'verbose_name_plural': 'Data Kunjungan Pasien',
            },
        ),
    ]
