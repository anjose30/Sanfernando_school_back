# forum/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet, NoticiaViewSet,
    GaleriaCategoriaViewSet, ImagenGaleriaViewSet, UserViewSet
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'noticias', NoticiaViewSet, basename='noticia')
router.register(r'galeria-categorias', GaleriaCategoriaViewSet, basename='galeriacategoria')
router.register(r'galeria-imagenes', ImagenGaleriaViewSet, basename='galeriaimagen')
router.register(r'usuarios', UserViewSet, basename='usuario')

urlpatterns = [
    path('', include(router.urls)),
]