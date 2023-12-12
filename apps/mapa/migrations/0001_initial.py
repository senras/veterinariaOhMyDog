# Generated by Django 4.2.2 on 2023-07-02 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paseador_cuidador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=50)),
                ('zona', models.CharField(max_length=50)),
                ('mail', models.CharField(max_length=50)),
                ('tipo_servicio', models.CharField(choices=[('Paseador', 'Paseador'), ('Cuidador', 'Cuidador')], max_length=20)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('descripcion', models.TextField()),
            ],
        ),
    ]