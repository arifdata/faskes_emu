# Generated by Django 3.2.5 on 2021-07-27 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apotek', '0002_out_stock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='out',
            old_name='nama',
            new_name='nama_obat',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='nama',
        ),
        migrations.AddField(
            model_name='stock',
            name='nama_obat',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='apotek.dataobat'),
            preserve_default=False,
        ),
    ]
