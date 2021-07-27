# Generated by Django 3.2.5 on 2021-07-27 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poli', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnosa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosa', models.CharField(help_text='Input nama diagnosa', max_length=50, verbose_name='Diagnosa')),
            ],
            options={
                'verbose_name_plural': 'Diagnosa',
            },
        ),
        migrations.AlterModelOptions(
            name='dataperesep',
            options={'verbose_name_plural': 'Data Peresep'},
        ),
    ]
