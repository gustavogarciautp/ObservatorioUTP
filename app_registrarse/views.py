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
"""
def update():
    obj= Interes.objects.all()
    INTERESES=[]
    for interes in obj:
        INTERESES.append([interes.nombre,interes.nombre])
    return INTERESES
"""
def registrarse(request):
    registro_form = RegistroForm() #Hacemos la instancia del formulario
    #INTERESES=update()
    """registro_form.fields['interes_']= forms.MultipleChoiceField(
							            required=True,
							            label='Interes',
							            widget=CheckboxSelectMultiple(),
							            choices=INTERESES)"""
    #print(registro_form.nombres)
    if request.method == 'POST': #verificamos se el formulario se ha enviado por POST
        registro_form = RegistroForm(data= request.POST) #request.POST contiene los campos que hemos rellenado en el formulario
        if registro_form.is_valid():  #verifica que todos los campos esten rellenados correctamente
            DNI = request.POST.get('DNI')
            Tipo_de_identificacion = request.POST.get('Tipo_de_identificacion')
            nombres= request.POST.get('nombres')  #request es un diccionario por eso utilizamos get para obtener los valores

            apellidos = request.POST.get('apellidos')
            pais = request.POST.get('pais')
            pais_obj= Paises.objects.get(pais=pais)

            fecha_nacimiento_month= request.POST.get('fecha_nacimiento_month')
            fecha_nacimiento_day= request.POST.get('fecha_nacimiento_day')
            fecha_nacimiento_year= request.POST.get('fecha_nacimiento_year')
            date=datetime(int(fecha_nacimiento_year),
            				int(fecha_nacimiento_month),
            				int(fecha_nacimiento_day))

            email= request.POST.get('email')
            genero=request.POST.get('genero')
            contraseña=request.POST.get('contraseña')
            contraseña_cifrada= hashlib.sha1(contraseña.encode()).hexdigest()
            activacion=False
            validado = False
            graduate = EgresadosUTP.objects.get(DNI=DNI)

            if graduate:
                validado = True
            #intereses_=(request.POST.getlist('interes_'))

            obj = Egresado.objects.create(DNI=DNI, Tipo_de_identificacion=Tipo_de_identificacion, nombres=nombres, apellidos=apellidos, pais=pais_obj, fecha_nacimiento=date, genero=genero,email=email, password= contraseña_cifrada, activacion= activacion, validado= validado)
            """
            for interes_ in intereses_:
            	obj_int= Interes.objects.get(nombre=interes_)
            	obj_= Intereses.objects.create(interes=obj_int, egresado=obj)"""
            return redirect(reverse('login_')+'?registrado')

    return render(request, "app_registrarse/registrarse.html", {'form': registro_form})


@method_decorator(login_required, name= 'dispatch')
class ProfileUpdate(UpdateView):
	form_class = PerfilForm
	success_url = reverse_lazy('perfil')
	template_name= 'app_registrarse/perfil_form.html'
 
	def get_object(self):
		#recuperar el objeto que se va a editar
		perfil, creado= Perfil.objects.get_or_create(user=self.request.user)
		return perfil


@method_decorator(login_required, name= 'dispatch')
class EmailUpdate(UpdateView):
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
    print(json_response)
    return JsonResponse(json_response)