# Generated by Django 3.2.5 on 2021-08-04 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apotek', '0004_auto_20210804_1130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bukupenerimaan',
            options={'verbose_name_plural': 'Buku Terima'},
        ),
        migrations.AlterModelOptions(
            name='sumberterima',
            options={'verbose_name_plural': 'Sumber Penerimaan'},
        ),
    ]