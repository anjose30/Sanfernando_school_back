# forum/views.py
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .models.categoria import Categoria
from .models.noticia import Noticia
from .models.galeriaCategoria import GaleriaCategoria
from .models.imagenGaleria import ImagenGaleria
from .serializers.serializers import (
    CategoriaSerializer, NoticiaListSerializer, NoticiaDetailSerializer,
    NoticiaCreateUpdateSerializer, GaleriaCategoriaSerializer,
    ImagenGaleriaSerializer, UserSerializer
)
from .services.services import NoticiaService

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # GET público, resto con auth

class NoticiaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]  # GET público, resto con auth
    
    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Noticia.objects.all()
        return Noticia.objects.filter(publicado=True)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NoticiaListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return NoticiaCreateUpdateSerializer
        return NoticiaDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)
    
    @action(detail=True, methods=['post'])
    def incrementar_visitas(self, request, pk=None):
        noticia = self.get_object()
        noticia = NoticiaService.incrementar_visitas(noticia.id)
        return Response({'visitas': noticia.visitas})
    
    @action(detail=False, methods=['get'])
    def recientes(self, request):
        limit = request.query_params.get('limit', 5)
        noticias = NoticiaService.get_noticias_recientes(int(limit))
        serializer = NoticiaListSerializer(noticias, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def mas_vistas(self, request):
        limit = request.query_params.get('limit', 5)
        noticias = NoticiaService.get_noticias_mas_vistas(int(limit))
        serializer = NoticiaListSerializer(noticias, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        query = request.query_params.get('q', '')
        noticias = NoticiaService.buscar_noticias(query)
        serializer = NoticiaListSerializer(noticias, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        categoria_id = request.query_params.get('categoria_id')
        if not categoria_id:
            return Response(
                {'error': 'Se requiere categoria_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        noticias = NoticiaService.get_noticias_por_categoria(categoria_id)
        serializer = NoticiaListSerializer(noticias, many=True)
        return Response(serializer.data)

class GaleriaCategoriaViewSet(viewsets.ModelViewSet):
    queryset = GaleriaCategoria.objects.all()
    serializer_class = GaleriaCategoriaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # GET público, resto con auth

class ImagenGaleriaViewSet(viewsets.ModelViewSet):
    queryset = ImagenGaleria.objects.filter(activo=True)
    serializer_class = ImagenGaleriaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # GET público, resto con auth
    
    def get_queryset(self):
        queryset = super().get_queryset()
        categoria_id = self.request.query_params.get('categoria_id')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        return queryset.order_by('orden')

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Totalmente público