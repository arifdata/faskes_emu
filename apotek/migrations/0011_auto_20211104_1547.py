# Generated by Django 3.2.5 on 2021-11-04 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apotek', '0010_auto_20211104_1504'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bukupengeluaran',
            options={'verbose_name_plural': 'Buku Pengeluaran Gudang'},
        ),
        migrations.RenameField(
            model_name='bukupengeluaran',
            old_name='sumber',
            new_name='tujuan',
        ),
        migrations.AlterField(
            model_name='resep',
            name='nama_obat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apotek.stokobatapotek'),
        ),
    ]
