from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    precio_base = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=50, help_text="Cantidad disponible en inventario")
    disponible = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre


class Variante(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='variantes')
    nombre = models.CharField(max_length=80)
    precio_extra = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Variante'
        verbose_name_plural = 'Variantes'

    def __str__(self):
        return f'{self.producto.nombre} - {self.nombre}'


class Personalizacion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='personalizaciones')
    nombre = models.CharField(max_length=100)
    precio_extra = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Personalización'
        verbose_name_plural = 'Personalizaciones'

    def __str__(self):
        return f'{self.producto.nombre} - {self.nombre}'


class Pedido(models.Model):
    ESTADOS = [
        ('RECIBIDO', 'Recibido'),
        ('PREPARANDO', 'En preparación'),
        ('LISTO', 'Listo'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]

    folio = models.CharField(max_length=20, unique=True, editable=False)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='RECIBIDO')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creado_en']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def save(self, *args, **kwargs):
        if not self.folio:
            ultimo_pedido = Pedido.objects.all().order_by('id').last()
            nuevo_id = 1 if not ultimo_pedido else ultimo_pedido.id + 1
            self.folio = f'PED-{nuevo_id:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.folio} - {self.estado} (${self.total})"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    variante = models.ForeignKey(Variante, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} (Pedido {self.pedido.folio})"