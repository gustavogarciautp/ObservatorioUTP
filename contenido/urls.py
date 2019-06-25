from django.urls import path
from .views import noticia, categoria

contenido_patterns = [
	path('', noticia, name="contenido"),
	path('categoria/<int:categoria_id>/', categoria, name="categoria")]
