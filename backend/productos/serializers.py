from rest_framework import serializers
from .models import Categoria, Producto, Variante, Personalizacion, Pedido, DetallePedido

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class VarianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variante
        fields = ['id', 'nombre', 'precio_extra', 'disponible']

class PersonalizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personalizacion
        fields = ['id', 'nombre', 'precio_extra', 'disponible']

class ProductoSerializer(serializers.ModelSerializer):
    variantes = VarianteSerializer(many=True, read_only=True)
    personalizaciones = PersonalizacionSerializer(many=True, read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'categoria', 'categoria_nombre', 'nombre', 'descripcion', 
                  'imagen', 'precio_base', 'stock', 'disponible', 'activo', 'variantes', 'personalizaciones']

class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    
    class Meta:
        model = DetallePedido
        fields = ['id', 'producto', 'producto_nombre', 'variante', 'cantidad', 'precio_unitario']

class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'folio', 'estado', 'total', 'detalles', 'creado_en', 'usuario']
        read_only_fields = ['folio', 'creado_en', 'usuario']

    def create(self, validated_data):
        detalles_data = self.initial_data.get('detalles', [])
        pedido = Pedido.objects.create(**validated_data)
        
        for detalle_data in detalles_data:
            producto = Producto.objects.get(id=detalle_data['producto'])
            if producto.stock >= detalle_data['cantidad']:
                producto.stock -= detalle_data['cantidad']
            else:
                producto.stock = 0
            if producto.stock == 0:
                producto.disponible = False
            producto.save()
            
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                variante_id=detalle_data.get('variante'),
                cantidad=detalle_data['cantidad'],
                precio_unitario=detalle_data['precio_unitario']
            )
        return pedido