from django.urls import path, include
from .views import noticia, categoria, NoticiaFull, ContenidoCreate, ContenidoUpdate, ContenidoDelete

contenido_patterns = [
	path('', noticia, name="contenido"),
	path('categoria/<int:categoria_id>/', categoria, name="categoria"),
	path('<int:pk>/<slug:slug>/', NoticiaFull.as_view(), name='noticefull'),
	path('create/', ContenidoCreate.as_view(), name='create'),
	path('update/<int:pk>', ContenidoUpdate.as_view(), name='update'),
	path('delete/<int:pk>', ContenidoDelete.as_view(), name='delete')
	]
