from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .models import Categoria, Producto, Variante, Personalizacion, Pedido
from .serializers import (
    CategoriaSerializer, ProductoSerializer, VarianteSerializer, 
    PersonalizacionSerializer, PedidoSerializer
)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.filter(activa=True)
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.filter(activo=True, disponible=True)
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

class VarianteViewSet(viewsets.ModelViewSet):
    queryset = Variante.objects.all()
    serializer_class = VarianteSerializer
    permission_classes = [AllowAny]

class PersonalizacionViewSet(viewsets.ModelViewSet):
    queryset = Personalizacion.objects.all()
    serializer_class = PersonalizacionSerializer
    permission_classes = [AllowAny]

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def get_permissions(self):
        # Permitimos que CUALQUIERA (cliente o cocinero) vea y actualice los pedidos
        # Esto hace que los botones de la cocina funcionen sin problemas.
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            username = request.data.get('username')
            try:
                user = User.objects.get(username=username)
                response.data['is_staff'] = user.is_staff
            except User.DoesNotExist:
                response.data['is_staff'] = False
        return response