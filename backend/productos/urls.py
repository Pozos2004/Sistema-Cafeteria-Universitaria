from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet, 
    ProductoViewSet, 
    VarianteViewSet, 
    PersonalizacionViewSet,
    PedidoViewSet
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'variantes', VarianteViewSet)
router.register(r'personalizaciones', PersonalizacionViewSet)
router.register(r'pedidos', PedidoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]