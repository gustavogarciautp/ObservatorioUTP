# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Noticia
from app_core.models import Intereses, Interes
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from app_registrarse.views import EgresadoRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import NoticiaForm
from django.http import JsonResponse
# Create your views here.

def noticia(request):
	if request.user.is_authenticated:
		publicaciones_list=[]
		template_base=''
		title = request.GET.get("title")
		description = request.GET.get("description")
		category = request.GET.get("category")
		if request.user.is_egresado:
			categorias=[]
			categorias_piv = Intereses.objects.filter(egresado__email=request.user.email)
			#print(categorias_piv)
			for categoria_piv in categorias_piv:
				categorias.append(categoria_piv.interes)
			#print(categorias)
			publicaciones = Noticia.objects.filter(categorias__in= categorias)
			#print(publicaciones)
			publicaciones_list = publicaciones.distinct()
			template_base="app_core/principal.html"
		else:
			publicaciones_list = Noticia.objects.all()
			template_base= "app_core/index.html"

		if title:
			publicaciones_list = publicaciones_list.filter(titulo__icontains = title)
		if description:
			publicaciones_list = publicaciones_list.filter(descripcion__icontains = description)
		if category:
			category=Interes.objects.get(nombre=category)
			publicaciones_list = publicaciones_list.filter(categorias__in= [category])

		paginator =Paginator(publicaciones_list,1)

		page = request.GET.get('page')
		publicaciones_page = paginator.get_page(page)

		return render(request, "contenido/noticias.html", {'paginator':paginator,'publicaciones':publicaciones_page,'template_base':template_base})
	else:
		return redirect(reverse('login_'))

def categoria(request, categoria_id):
	if request.user.is_authenticated:
		if request.user.is_egresado:
			template_base="app_core/principal.html"
		else:
			template_base="app_core/index.html"
		#category= Category.objects.get(id=category_id)  #get nos permite obtener un solo registro filtrando por una serie de campos
		category = get_object_or_404(Interes, id= categoria_id)
		#posts= Post.objects.filter(categorias= category)
		publicaciones = category.get_noticias.all().distinct()

		paginator =Paginator(publicaciones,1)

		page = request.GET.get('page')
		publicaciones_page = paginator.get_page(page)

		return render(request, "contenido/categorias.html", {'paginator':paginator,'publicaciones':publicaciones_page, 'template_base': template_base})#, 'posts':posts})
	else:
		return redirect(reverse('login_'))

class ContenidoRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(ContenidoRequiredMixin, self).dispatch(request, *args, *kwargs)
        else:
            return redirect(reverse_lazy('login_'))

class NoticiaFull(ContenidoRequiredMixin, DetailView):
    model = Noticia


class ContenidoCreate(ContenidoRequiredMixin,CreateView):
	model = Noticia
	form_class = NoticiaForm
	success_url= reverse_lazy('contenido')


class ContenidoUpdate(ContenidoRequiredMixin,UpdateView):
	model = Noticia
	form_class = NoticiaForm
	template_name_suffix= '_update_form'

	def get_success_url(self):
		return reverse_lazy('update', args=[self.object.id]) + '?ok'


class ContenidoDelete(ContenidoRequiredMixin, DeleteView):
	model = Noticia
	success_url = reverse_lazy('contenido')


def BuscarCategorias(request):
    json_response = {}
    email = request.GET.get('email', None)
    tipo = request.GET.get('type', None)
    categorias=[]

    if tipo == "True":
    	categorias_ = Interes.objects.all()
    	for categoria in categorias_:
    		categorias.append(categoria.nombre)
    else: 
        categorias_piv = Intereses.objects.filter(egresado__email=email)
        for categoria_piv in categorias_piv:
            categorias.append(categoria_piv.interes.nombre)
    
    json_response['categorias']= categorias
    print(json_response) 
    return JsonResponse(json_response)