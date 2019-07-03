# Create your views here.

from django.shortcuts import render, redirect ##redirect sirve para redireccionar paginas
from .forms import RegistroForm, PerfilForm, EmailForm
from django.core.mail import EmailMessage
from django.urls import reverse
from  app_core.models import Egresado, Interes, Intereses, EgresadosUTP, Country, City
from datetime import datetime
import hashlib
import requests
import urllib
import json
from django import forms
from django.conf import settings
from django.contrib import messages
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django .urls import reverse_lazy
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, JsonResponse

from .models import Perfil

def registrarse(request):
    registro_form = RegistroForm() #Hacemos la instancia del formulario
    if request.method == 'POST': #verificamos se el formulario se ha enviado por POST
        registro_form = RegistroForm(data= request.POST) #request.POST contiene los campos que hemos rellenado en el formulario
        if registro_form.is_valid():  #verifica que todos los campos esten rellenados correctamente
            DNI = request.POST.get('DNI')
            Tipo_de_identificacion = request.POST.get('Tipo_de_identificacion')
            nombres= request.POST.get('nombres')  #request es un diccionario por eso utilizamos get para obtener los valores

            apellidos = request.POST.get('apellidos')
            pais = request.POST.get('pais')
            #pais_obj= Paises.objects.get(pais=pais)
            ciudad = request.POST.get('ciudad')

            fecha_nacimiento_month= request.POST.get('fecha_nacimiento_month')
            fecha_nacimiento_day= request.POST.get('fecha_nacimiento_day')
            fecha_nacimiento_year= request.POST.get('fecha_nacimiento_year')
            date=datetime(int(fecha_nacimiento_year),
            				int(fecha_nacimiento_month),
            				int(fecha_nacimiento_day))

            email= request.POST.get('email')
            genero=request.POST.get('genero')
            contraseña=request.POST.get('contraseña')
            activacion=False
            validado = False
            graduate = EgresadosUTP.objects.filter(DNI=DNI)

            if graduate:
                validado = True

            obj = Egresado(DNI=DNI, Tipo_de_identificacion=Tipo_de_identificacion, nombres=nombres, apellidos=apellidos, pais=pais, ciudad=ciudad,fecha_nacimiento=date, genero=genero,email=email, activacion= activacion, validado= validado, is_staff=False, is_superuser=False)
            obj.set_password(contraseña)
            obj.save()
            return redirect(reverse('login_')+'?registrado')

    return render(request, "app_registrarse/registrarse.html", {'form': registro_form})


class EgresadoRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_egresado:
            return super(EgresadoRequiredMixin, self).dispatch(request, *args, *kwargs)
        else:
            return redirect(reverse_lazy('login_'))


class ProfileUpdate(EgresadoRequiredMixin, UpdateView):
	form_class = PerfilForm
	success_url = reverse_lazy('perfil')
	template_name= 'app_registrarse/perfil_form.html'
 
	def get_object(self):
		#recuperar el objeto que se va a editar
		perfil, creado= Perfil.objects.get_or_create(user=self.request.user)
		return perfil


class EmailUpdate(EgresadoRequiredMixin,UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('perfil')
    template_name= 'app_registrarse/perfil_email.html'
 
    def get_object(self):
        #recuperar el objeto que se va a editar
        return self.request.user

    def get_form(self,form_class=None):
        form = super(EmailUpdate, self).get_form()

        form.fields['email'].widget= forms.EmailInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Email'})
        return form


def BuscarCiudades(request):
    json_response = {}
    pais_name = request.GET.get('pais', None)
    pais_obj = Country.objects.get(name=pais_name)
    ciudades = City.objects.filter(country_id=pais_obj.id)
    cities=[ciudad.name for ciudad in ciudades]
    json_response['ciudades']= cities 
    return JsonResponse(json_response)