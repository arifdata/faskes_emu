# Generated by Django 3.2.5 on 2024-02-22 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataPasien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_kartu', models.CharField(help_text='Masukkan no BPJS / KTP', max_length=20, verbose_name='Nomor Kartu')),
                ('nama_pasien', models.CharField(help_text='Masukkan nama', max_length=30, verbose_name='Nama Pasien')),
                ('alamat', models.CharField(blank=True, help_text='Masukkan alamat', max_length=50, verbose_name='Alamat')),
                ('usia', models.DateField(blank=True, help_text='dd-mm-yy', verbose_name='Tanggal Lahir')),
                ('no_hp', models.CharField(blank=True, help_text='masukkan dengan format +628XXXXXXXXXX', max_length=15, verbose_name='No Telepon')),
            ],
            options={
                'verbose_name_plural': 'Data Pasien',
            },
        ),
    ]
