from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Noticia
from app_core.models import Intereses, Interes

# Create your views here.

def noticia(request):
	contenidos=[]
	categorias=[]
	categorias_piv = Intereses.objects.filter(egresado__email=request.user.email)
	#print(categorias_piv)
	for categoria_piv in categorias_piv:
		categorias.append(categoria_piv.interes)
	#print(categorias)
	publicaciones = Noticia.objects.filter(categorias__in= categorias)
	#print(publicaciones)
	return render(request, "contenido/noticias.html", {'publicaciones':publicaciones,'categorias':categorias})

def categoria(request, categoria_id):
    #category= Category.objects.get(id=category_id)  #get nos permite obtener un solo registro filtrando por una serie de campos
    category = get_object_or_404(Interes, id= categoria_id)
    #print("kllllllllllllllllllllllll")
    #print(category)
    #posts= Post.objects.filter(categorias= category)
    return render(request, "contenido/categorias.html", {'categoria':category})#, 'posts':posts})
