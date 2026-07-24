# forum/serializers/serializers.py
from rest_framework import serializers
from ..models.categoria import Categoria
from ..models.noticia import Noticia
from ..models.galeriaCategoria import GaleriaCategoria
from ..models.imagenGaleria import ImagenGaleria
from django.contrib.auth.models import User

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'created_at']

class NoticiaListSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    autor_nombre = serializers.CharField(source='autor.username', read_only=True)
    resumen = serializers.SerializerMethodField()
    
    class Meta:
        model = Noticia
        fields = [
            'id', 'titulo', 'resumen', 'imagen_destacada', 
            'categoria', 'categoria_nombre', 'autor_nombre',
            'created_at', 'publicado', 'visitas'
        ]
    
    def get_resumen(self, obj):
        return obj.get_resumen()

class NoticiaDetailSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    autor_nombre = serializers.CharField(source='autor.username', read_only=True)
    
    class Meta:
        model = Noticia
        fields = [
            'id', 'titulo', 'contenido', 'imagen_destacada',
            'categoria', 'categoria_nombre', 'autor', 'autor_nombre',
            'created_at', 'updated_at', 'publicado', 'visitas'
        ]
        read_only_fields = ['autor', 'visitas']

class NoticiaCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = [
            'id', 'titulo', 'contenido', 'imagen_destacada',
            'categoria', 'publicado'
        ]

class GaleriaCategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GaleriaCategoria
        fields = ['id', 'nombre', 'descripcion', 'created_at']

class ImagenGaleriaSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    
    class Meta:
        model = ImagenGaleria
        fields = [
            'id', 'categoria', 'categoria_nombre', 'titulo', 
            'descripcion', 'imagen', 'created_at', 'orden', 'activo'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']