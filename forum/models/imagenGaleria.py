from django.db import models
from forum.models.galeriaCategoria import GaleriaCategoria

class ImagenGaleria(models.Model):
    categoria = models.ForeignKey(
        GaleriaCategoria, 
        on_delete=models.CASCADE,
        related_name='imagenes'
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='galeria/')
    created_at = models.DateTimeField(auto_now_add=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name_plural = "Imágenes de galería"
        ordering = ['orden', 'created_at']