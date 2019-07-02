# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Noticia
from app_core.models import Intereses, Interes
from django.urls import reverse

# Create your views here.

def noticia(request):
	if request.user.is_authenticated and request.user.is_egresado:
		categorias=[]
		categorias_piv = Intereses.objects.filter(egresado__email=request.user.email)
		#print(categorias_piv)
		for categoria_piv in categorias_piv:
			categorias.append(categoria_piv.interes)
		#print(categorias)
		publicaciones = Noticia.objects.filter(categorias__in= categorias)
		#print(publicaciones)
		return render(request, "contenido/noticias.html", {'publicaciones':publicaciones,'categorias':categorias})
	else:
		return redirect(reverse('login_'))

def categoria(request, categoria_id):
	if request.user.is_authenticated and request.user.is_egresado:
		#category= Category.objects.get(id=category_id)  #get nos permite obtener un solo registro filtrando por una serie de campos
		category = get_object_or_404(Interes, id= categoria_id)
		#posts= Post.objects.filter(categorias= category)
		return render(request, "contenido/categorias.html", {'categoria':category})#, 'posts':posts})
	else:
		return redirect(reverse('login_'))
