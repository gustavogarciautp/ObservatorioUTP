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
# Create your views here.

def noticia(request):
	if request.user.is_authenticated:
		publicaciones_list=[]
		template_base=''
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


class ContenidoCreate(CreateView):
	model = Noticia
	form_class = NoticiaForm
	success_url= reverse_lazy('contenido')


class ContenidoUpdate(UpdateView):
	model = Noticia
	form_class = NoticiaForm
	template_name_suffix= '_update_form'

	def get_success_url(self):
		return reverse_lazy('update', args=[self.object.id]) + '?ok'


class ContenidoDelete(DeleteView):
	model = Noticia
	success_url = reverse_lazy('contenido')
