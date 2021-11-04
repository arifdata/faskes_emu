# Generated by Django 3.2.5 on 2021-11-04 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apotek', '0008_auto_20211104_0922'),
    ]

    operations = [
        migrations.CreateModel(
            name='StokObatApotek',
            fields=[
                ('stokobatgudang_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apotek.stokobatgudang')),
            ],
            options={
                'verbose_name_plural': 'Stok Obat Apotek',
            },
            bases=('apotek.stokobatgudang',),
        ),
        migrations.AddField(
            model_name='stokobatgudang',
            name='after_pengurangan_saldo',
            field=models.PositiveSmallIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='stokobatgudang',
            name='prev_saldo',
            field=models.PositiveSmallIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='dataobat',
            name='is_okt',
            field=models.BooleanField(help_text='Check jika termasuk narko/psiko', verbose_name='Narkotik / Psikotropik?'),
        ),
    ]
