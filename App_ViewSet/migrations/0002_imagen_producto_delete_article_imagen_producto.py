# Generated by Django 4.1 on 2022-08-04 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App_ViewSet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=150, null=True, verbose_name='Url de la imagen')),
            ],
            options={
                'verbose_name': 'Imagen',
                'verbose_name_plural': 'Imágenes',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre del producto')),
                ('descripcion', models.TextField(max_length=150, verbose_name='Descripción del producto')),
                ('precio', models.IntegerField(verbose_name='Precio')),
                ('iva', models.IntegerField(verbose_name='Iva')),
                ('marca', models.CharField(blank=True, max_length=25, verbose_name='Marca')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.AddField(
            model_name='imagen',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_ViewSet.producto', verbose_name='Producto'),
        ),
    ]
