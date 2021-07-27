# Generated by Django 3.2.5 on 2021-07-27 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pendaftaran', '0003_auto_20210727_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataDokter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_dokter', models.CharField(help_text='Input nama dokter', max_length=30, verbose_name='Nama Dokter')),
            ],
            options={
                'verbose_name_plural': 'Data Dokter',
            },
        ),
        migrations.AlterField(
            model_name='datapasien',
            name='alamat',
            field=models.CharField(blank=True, help_text='Masukkan alamat', max_length=50, verbose_name='Alamat'),
        ),
    ]
