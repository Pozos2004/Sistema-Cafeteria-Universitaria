from django.contrib import admin
from django.utils import timezone
from django.db.models import Sum, Count
from .models import Categoria, Producto, Variante, Personalizacion, Pedido, DetallePedido


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa', 'orden')
    list_filter = ('activa',)
    search_fields = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_base', 'stock', 'disponible', 'activo')
    list_filter = ('categoria', 'disponible', 'activo')
    search_fields = ('nombre', 'descripcion')


@admin.register(Variante)
class VarianteAdmin(admin.ModelAdmin):
    list_display = ('producto', 'nombre', 'precio_extra', 'disponible')
    list_filter = ('disponible',)


@admin.register(Personalizacion)
class PersonalizacionAdmin(admin.ModelAdmin):
    list_display = ('producto', 'nombre', 'precio_extra', 'disponible')
    list_filter = ('disponible',)


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ('producto', 'variante', 'cantidad', 'precio_unitario')


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('folio', 'estado', 'total', 'creado_en')
    list_filter = ('estado', 'creado_en')
    search_fields = ('folio',)
    inlines = [DetallePedidoInline]
    
    # Conectar la plantilla del reporte
    change_list_template = "admin/productos/pedido/change_list.html"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        hoy = timezone.now().date()
        
        # Calcular ventas del día (excluyendo cancelados)
        ventas = Pedido.objects.filter(creado_en__date=hoy).exclude(estado='CANCELADO').aggregate(total=Sum('total'))
        extra_context['ventas_hoy'] = ventas['total'] or 0.00

        # Calcular top 5 de productos
        top = DetallePedido.objects.filter(pedido__creado_en__date=hoy).values('producto__nombre').annotate(
            total_vendidos=Count('id')
        ).order_by('-total_vendidos')[:5]
        extra_context['top_productos'] = top
        
        return super().changelist_view(request, extra_context=extra_context)