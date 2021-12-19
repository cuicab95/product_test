from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField
import os
from django.utils.text import slugify
# Create your models here.


class Customer(models.Model):

    TYPE_CHOICES = (
        ('NOR', _('Normal')),
        ('PLT', _('Plata')),
        ('ORO', _('Oro')),
        ('PTN', _('Platino')),
    )

    def image_path(self, filename):
        extension = os.path.splitext(filename)[1][1:]
        file_name = os.path.splitext(filename)[0]
        url = "customer/file/%s.%s" % (slugify(str(file_name)), extension)
        return url

    first_name = models.CharField(max_length=100, verbose_name=_("Nombre"))
    last_name = models.CharField(max_length=100, verbose_name=_("Apellido"))
    code = models.CharField(max_length=12, verbose_name=_("Código"), unique=True)
    photo = models.ImageField(upload_to=image_path, verbose_name=_("Foto"), null=True, blank=True)
    type = models.CharField(max_length=4, choices=TYPE_CHOICES, default='NOR', verbose_name=_("Tipo de cliente"))
    address = models.CharField(max_length=500, verbose_name=_("Dirección"), null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"))

    def __str__(self):
        return f"{self.first_name}-{self.last_name}"

    class Meta:
        verbose_name = _("Cliente")
        verbose_name_plural = _("Clientes")


class Provider(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nombre"))
    address = models.CharField(max_length=500, verbose_name=_("Dirección"), null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Proveedor")
        verbose_name_plural = _("Proveedores")


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nombre"))
    code = models.CharField(max_length=12, verbose_name=_("Código"))
    description = models.TextField(verbose_name=_("Descripción"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"))

    def __str__(self):
        return f"{self.code}-{self.name}"

    class Meta:
        verbose_name = _("Producto")
        verbose_name_plural = _("Productos")


class ProductProvider(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Producto"))
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name=_("Proveedor"))
    price = models.DecimalField(max_digits=7, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"))

    def __str__(self):
        return f"{self.product}-{self.provider}"

    class Meta:
        verbose_name = _("Producto con su proveedor")
        verbose_name_plural = _("Productos con sus proveedores")


class Order(models.Model):
    TYPE_CHOICES = (
        ('CD', _('Centro de distribución')),
        ('SU', _('Sucursal')),
        ('EA', _('Empresa asociada')),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("Cliente"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"))
    assortment_date = models.DateTimeField(verbose_name=_("Fecha de surtido"), null=True, blank=True)
    is_urgent = models.BooleanField(default=False, verbose_name=_("¿Urgente?"))
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='CD', verbose_name=_("Tipo de pedido"))
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    custom_data = JSONField(default={}, verbose_name=_("Información adicional"))

    def __str__(self):
        return f"{self.id}-{self.customer}"

    class Meta:
        verbose_name = _("Pedido")
        verbose_name_plural = _("Pedidos")


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("Pedido"))
    product_provider = models.ForeignKey(ProductProvider, on_delete=models.CASCADE, verbose_name=_("Producto"))
    quantity = models.IntegerField(verbose_name=_("Cantidad"), default=1)
    sale_price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.order}-{self.product_provider}"

    @property
    def total(self):
        total = self.sale_price * self.quantity
        return f'{total:,}'

    class Meta:
        verbose_name = _("Detalle de pedido")
        verbose_name_plural = _("Detalles de pedidos")







