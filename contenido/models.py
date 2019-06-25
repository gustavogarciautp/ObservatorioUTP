from django.db import models
from ckeditor.fields import RichTextField
from app_core.models import Interes

# Create your models here.
class Noticia(models.Model):
	titulo = models.CharField(max_length=200, verbose_name='Titulo')
	descripcion = RichTextField(verbose_name='Descripcion')
	Image= models.ImageField(verbose_name='Imagen', upload_to='contenidos')
	created = models.DateTimeField(auto_now_add= True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
	categorias = models.ManyToManyField(Interes, related_name="get_noticias")


	class Meta:
		verbose_name = 'Noticia'
		verbose_name_plural= 'Noticias'
		ordering = ["-created"]
	def __str__(self):
		return self.titulo
