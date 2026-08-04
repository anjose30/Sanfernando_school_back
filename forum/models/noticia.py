from django.db import models
from django.conf import settings
from .categoria import Categoria
from ckeditor_uploader.fields import RichTextUploadingField

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = RichTextUploadingField()  # Editor WYSIWYG con imágenes
    imagen_destacada = models.ImageField(
        upload_to='noticias/portadas/', 
        blank=True, 
        null=True
    )
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='noticias'
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='noticias'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=True)
    visitas = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.titulo
    
    def get_resumen(self):
        """Obtiene un resumen del contenido (primeros 200 caracteres)"""
        from django.utils.html import strip_tags
        texto_plano = strip_tags(self.contenido)
        return texto_plano[:200] + '...' if len(texto_plano) > 200 else texto_plano
    
    class Meta:
        verbose_name_plural = "Noticias"
        ordering = ['-created_at']