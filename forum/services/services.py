# forum/services/services.py
from ..models.noticia import Noticia
from ..models.categoria import Categoria
from ..models.galeriaCategoria import GaleriaCategoria
from ..models.imagenGaleria import ImagenGaleria
from django.db.models import Q

class NoticiaService:
    @staticmethod
    def get_noticias_publicadas():
        """Obtiene todas las noticias publicadas"""
        return Noticia.objects.filter(publicado=True)

    @staticmethod
    def get_noticias_por_categoria(categoria_id):
        """Obtiene noticias por categoría"""
        return Noticia.objects.filter(categoria_id=categoria_id, publicado=True)

    @staticmethod
    def get_noticias_recientes(limit=5):
        """Obtiene las noticias más recientes"""
        return Noticia.objects.filter(publicado=True).order_by('-created_at')[:limit]

    @staticmethod
    def get_noticias_mas_vistas(limit=5):
        """Obtiene las noticias más vistas"""
        return Noticia.objects.filter(publicado=True).order_by('-visitas')[:limit]

    @staticmethod
    def buscar_noticias(query):
        """Busca noticias por título o contenido"""
        return Noticia.objects.filter(
            Q(titulo__icontains=query) | Q(contenido__icontains=query),
            publicado=True
        )

    @staticmethod
    def incrementar_visitas(noticia_id):
        """Incrementa el contador de visitas"""
        noticia = Noticia.objects.get(id=noticia_id)
        noticia.visitas += 1
        noticia.save()
        return noticia

class CategoriaService:
    @staticmethod
    def get_all_categorias():
        return Categoria.objects.all()

    @staticmethod
    def get_categoria_by_id(categoria_id):
        return Categoria.objects.get(id=categoria_id)

class GaleriaService:
    @staticmethod
    def get_categorias_galeria():
        return GaleriaCategoria.objects.all()

    @staticmethod
    def get_imagenes_por_categoria(categoria_id):
        return ImagenGaleria.objects.filter(
            categoria_id=categoria_id, 
            activo=True
        ).order_by('orden')

    @staticmethod
    def get_all_imagenes_activas():
        return ImagenGaleria.objects.filter(activo=True).order_by('orden')