from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
#from app_registrarse.models import Perfil
from app_core.models import Egresado, Circulo
from app_registrarse.views import EgresadoRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

class ProfileListView(EgresadoRequiredMixin,ListView):
    model = Egresado
    template_name = 'perfiles/profile_list.html'
    #paginate_by = 1

    def get(self, request, *args, **kwargs):
        name= request.GET.get("name")
        user = request.user
        
        circulo = Circulo.objects.get_or_create(usuario_id= user.pk)

        friends= circulo[0].amigos.all()           
        
        egresados = Egresado.objects.filter(activacion=True).exclude(pk=user.pk)

        unfriends = egresados.difference(friends)
        unfriends = unfriends.exclude(pk=user.pk)

        if name:
            unfriends = unfriends.filter(nombres__icontains= name)
        paginator =Paginator(unfriends,1)

        page = request.GET.get('page')
        egresados_page = paginator.get_page(page)
        #q = request.GET.get('q')
        #stuff = stuff.filter(user__icontains=q)
        return render(request, self.template_name, {'paginator':paginator,'egresado_list':egresados_page, 'is_paginated':True}) 

 


class FriendsListView(EgresadoRequiredMixin,ListView):
    model = Circulo
    template_name = 'perfiles/amigos.html'
    #paginate_by = 9

    def get(self, request, *args, **kwargs):
        name= request.GET.get("name")
        user = request.user

        circle = Circulo.objects.get(usuario = user) 
        friends = circle.amigos.all()
        if name:  
            friends = friends.filter(nombres__icontains= name)
        
        paginator =Paginator(friends,1)

        page = request.GET.get('page')
        friends_page = paginator.get_page(page)

        return render(request, self.template_name, {'paginator':paginator,'friends_list':friends_page, 'is_paginated':True}) 

 


class ProfileDetailView(EgresadoRequiredMixin, DetailView):
    model = Egresado
    template_name = 'perfiles/profile_detail.html'

    def get_object(self):
        return get_object_or_404(Egresado, email=self.kwargs['email'])

    def get(self, request, *args, **kwargs):
        user = request.user
        egresado = self.get_object()
        circulo = Circulo.objects.get_or_create(usuario_id= user.pk)
        amigo=False
        
        for e in circulo[0].amigos.all():
            if e.pk == egresado.pk:
                amigo = True
        return render (request, self.template_name, {'amigo':amigo, 'egresado':egresado})
