# Generated by Django 5.2.3 on 2025-06-23 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planilla', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plazas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20)),
                ('denominacion', models.CharField(max_length=255)),
                ('zona_economica', models.CharField(max_length=10)),
                ('nivel_salarial', models.CharField(max_length=10)),
                ('plazas', models.IntegerField()),
                ('horas', models.IntegerField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='adscripcion',
            options={},
        ),
        migrations.AlterField(
            model_name='planilla',
            name='no',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterModelTable(
            name='planilla',
            table='planilla',
        ),
    ]
