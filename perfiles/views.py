from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
#from app_registrarse.models import Perfil
from app_core.models import Egresado
from app_registrarse.views import EgresadoRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# Create your views here.
class ProfileListView(EgresadoRequiredMixin,ListView):
    model = Egresado
    template_name = 'perfiles/profile_list.html'
    #paginate_by = 1

    def get(self, request, *args, **kwargs):
        name= request.GET.get("name")

        egresados = Egresado.objects.filter(activacion=True)
        if name:
            egresados = egresados.filter(nombres__icontains= name)
        paginator =Paginator(egresados,3)

        page = request.GET.get('page')
        egresados_page = paginator.get_page(page)
        #q = request.GET.get('q')
        #stuff = stuff.filter(user__icontains=q)
        return render(request, self.template_name, {'paginator':paginator,'egresado_list':egresados_page, 'is_paginated':True}) 

class ProfileDetailView(EgresadoRequiredMixin, DetailView):
    model = Egresado
    template_name = 'perfiles/profile_detail.html'

    def get_object(self):
        return get_object_or_404(Egresado, email=self.kwargs['email'])


