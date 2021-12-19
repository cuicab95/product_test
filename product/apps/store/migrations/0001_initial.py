# Generated by Django 4.0 on 2021-12-18 02:23

from django.db import migrations, models
import django.db.models.deletion
import product.apps.global_functions
import product.apps.store.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=100, verbose_name='Apellido')),
                ('code', models.CharField(max_length=12, unique=True, verbose_name='Código')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=product.apps.store.models.Customer.image_path, verbose_name='Foto')),
                ('type', models.CharField(default='NOR', max_length=4, verbose_name='Tipo de cliente')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Dirección')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('assortment_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de surtido')),
                ('is_urgent', models.BooleanField(default=False, verbose_name='¿Urgente?')),
                ('type', models.CharField(default='CD', max_length=2, verbose_name='Tipo de pedido')),
                ('total', models.DecimalField(decimal_places=2, max_digits=7)),
                ('custom_data', models.JSONField(default={}, verbose_name='Información adicional')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.customer', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('code', models.CharField(max_length=12, verbose_name='Código')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=100, verbose_name='Apellido')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Dirección')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
            },
        ),
        migrations.CreateModel(
            name='ProductProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Producto')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.provider', verbose_name='Proveedor')),
            ],
            options={
                'verbose_name': 'Producto con su proveedor',
                'verbose_name_plural': 'Productos con sus proveedores',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='Cantidad')),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order', verbose_name='Pedido')),
                ('product_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productprovider', verbose_name='Producto')),
            ],
            options={
                'verbose_name': 'Detalle de pedido',
                'verbose_name_plural': 'Detalles de pedidos',
            },
        ),
    ]
