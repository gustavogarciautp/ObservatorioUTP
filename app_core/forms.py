from django import forms
from .models import Administrador, Country, City, Egresado, Interes
from django.contrib.auth.forms import UserChangeForm

countries=Country.objects.all()
PAISES=[[x.name,x.name] for x in countries]
#CIUDADES= [[x.name, x.name] for x in City.objects.filter(country_id=countries[0].id)]

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email",required=True, widget=forms.EmailInput(
        attrs= {'id':'lol','class':'form-control', 'placeholder':'ejemplo@utp.edu.co'}), max_length=100, min_length=3) #campo opcional
    
    contraseña = forms.CharField(label="Contraseña", required=True, widget= forms.PasswordInput(attrs= {'class':'form-control', 'placeholder':'Contraseña'})) 

class Recuperar1Form(forms.Form):
    email = forms.EmailField(label="Email",required=True, widget=forms.EmailInput(
        attrs= {'class':'form-control', 'placeholder':'ejemplo@utp.edu.co'}), max_length=100, min_length=3) #campo opcional
    

class Recuperar2Form(forms.Form):
	contraseña = forms.CharField(label="Contraseña", required=True, widget= forms.PasswordInput(attrs= {'class':'form-control', 'placeholder':'Nueva contraseña'})) 
	confirmar_contraseña = forms.CharField(label="confirmar_Contraseña", required=True, widget= forms.PasswordInput(attrs= {'class':'form-control', 'placeholder':'Confirmar contraseña'})) 

	def clean_contraseña(self):
		contraseña= self.cleaned_data['contraseña']
		if contraseña.isdigit():
			raise forms.ValidationError('Su contraseña no puede ser completamente numérica')
		elif len(contraseña)<8:
			raise forms.ValidationError('Su contraseña debe tener al menos 8 caracteres')
		return contraseña

class FirstLoginAdmin(forms.Form):
	antigua = forms.CharField(label= "Contraseña Antigua", required=True, widget= forms.PasswordInput(attrs= {'class':'form-control', 'placeholder':'Antigua contraseña'}))
	contraseña = forms.CharField(label="Contraseña", required=True, widget= forms.PasswordInput(attrs= {'class':'form-control', 'placeholder':'Nueva contraseña'})) 
	confirmar_contraseña = forms.CharField(label="confirmar_Contraseña", required=True, widget= forms.PasswordInput(attrs= {'class':'form-control', 'placeholder':'Confirmar contraseña'})) 

	def clean_contraseña(self):
		contraseña= self.cleaned_data['contraseña']
		if contraseña.isdigit():
			raise forms.ValidationError('Su contraseña no puede ser completamente numérica')
		elif len(contraseña)<8:
			raise forms.ValidationError('Su contraseña debe tener al menos 8 caracteres')
		return contraseña	


class InteresForm(forms.ModelForm):
	class Meta:
		model = Interes
		fields = ('nombre',)

	def clean_nombre(self):
		nombre= self.cleaned_data['nombre']
		if len(nombre)>=31:
			raise forms.ValidationError('Tamaño máximo: 30 caracteres')
		words=nombre.split()
		for word in words:
			if not word.isalpha():
				raise forms.ValidationError('Introduce un interes valido (solo letras)')
		return nombre

class AdminForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AdminForm, self).__init__(*args, **kwargs)
		admin_instance = self.instance
		if admin_instance.email:
			id_pais= Country.objects.get(name= admin_instance.pais).id
			self.CIUDADES = [[x.name, x.name] for x in City.objects.filter(country_id=id_pais)]
		else:
			#self.CIUDADES=[[x.name, x.name] for x in City.objects.filter(country_id=countries[0].id)]
			self.CIUDADES=[["init","init"]]
		self.fields['ciudad']= forms.CharField(label="Ciudad", widget= forms.Select(choices=self.CIUDADES))

	class Meta:
		model = Administrador
		fields = ('Tipo_de_identificacion','DNI','nombres','apellidos', 'genero','email','pais','ciudad','direccion','telefono')
		widgets = {
			'pais': forms.Select(choices=PAISES, attrs={'onchange':'changecountry()'}),
			#'ciudad': forms.Select(choices=self.CIUDADES)
		}

	def clean_nombres(self):
		nombres = self.cleaned_data['nombres']
		if not nombres.isalpha():
			raise forms.ValidationError('Introduce un nombre valido')            
		return nombres  

	def clean_apellidos(self):
		apellidos = self.cleaned_data['apellidos']
		if not apellidos.isalpha():
			raise forms.ValidationError('Introduce un apellido valido')            
		return apellidos

	def clean_email(self):
		email = self.cleaned_data['email']
		if not email.endswith('@utp.edu.co'):
			raise forms.ValidationError('El email debe ser @utp.edu.co')  	
		else:
			obj=Administrador.objects.filter(email=email)
			if obj.exists() and self.instance.email!= obj[0].email:
				raise forms.ValidationError('El email ya esta registrado, prueba con otro')
		return email

	def clean_contraseña(self):
		contraseña= self.cleaned_data['contraseña']
		if contraseña.isdigit():
			raise forms.ValidationError('Su contraseña no puede ser completamente numérica')
		elif len(contraseña)<8:
			raise forms.ValidationError('Su contraseña debe tener al menos 8 caracteres')
		return contraseña


	def clean_DNI(self):
		IDENTIFICACION= ["Cédula de ciudadania", "Pasaporte"]
		dni= self.cleaned_data['DNI']
		Tipo_de_identificacion = self.cleaned_data['Tipo_de_identificacion']
		if  Tipo_de_identificacion==IDENTIFICACION[1]:
			if not dni[0:3].isalpha() or not dni[3:6].isdigit():
				raise  forms.ValidationError("DNI invalido")
		elif Tipo_de_identificacion==IDENTIFICACION[0]:
			if len(dni) <8 or len(dni)>10:
				raise forms.ValidationError("DNI debe tener de 8 a 10 digitos")
			elif not dni.isdigit():
				raise forms.ValidationError("DNI solo debe contener numeros del 0-9")
		return dni

class EditProfileForm(UserChangeForm):

	class Meta:
		model = Administrador
		fields = ('Tipo_de_identificacion','DNI','nombres','apellidos', 'genero','email','pais','ciudad','direccion','telefono')
		widgets = {
			'pais': forms.Select(choices=PAISES, attrs={'onchange':'changecountry()'}),
			#'ciudad': forms.Select(choices=self.CIUDADES)
		}

	def __init__(self, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		admin_instance = self.instance
		if admin_instance.email:
			id_pais= Country.objects.get(name= admin_instance.pais).id
			self.CIUDADES = [[x.name, x.name] for x in City.objects.filter(country_id=id_pais)]
		else:
			#self.CIUDADES=[[x.name, x.name] for x in City.objects.filter(country_id=countries[0].id)]
			self.CIUDADES=[["init","init"]]
		self.fields['ciudad']= forms.CharField(label="Ciudad", widget= forms.Select(choices=self.CIUDADES))

	def clean_nombres(self):
		nombres = self.cleaned_data['nombres']
		if not nombres.isalpha():
			raise forms.ValidationError('Introduce un nombre valido')            
		return nombres;    

	def clean_apellidos(self):
		apellidos = self.cleaned_data['apellidos']
		if not apellidos.isalpha():
			raise forms.ValidationError('Introduce un apellido valido')            
		return apellidos

	def clean_email(self):
		email = self.cleaned_data['email']
		if not email.endswith('@utp.edu.co'):
			raise forms.ValidationError('El email debe ser @utp.edu.co')  	
		else:
			obj=Administrador.objects.filter(email=email)
			if obj.exists() and self.instance.email!= obj[0].email:
				raise forms.ValidationError('El email ya esta registrado, prueba con otro')
		return email

	def clean_DNI(self):
		IDENTIFICACION= ["Cédula de ciudadania", "Pasaporte"]
		dni= self.cleaned_data['DNI']
		Tipo_de_identificacion = self.cleaned_data['Tipo_de_identificacion']
		if  Tipo_de_identificacion==IDENTIFICACION[1]:
			if not dni[0:3].isalpha() or not dni[3:6].isdigit():
				raise  forms.ValidationError("DNI invalido")
		elif Tipo_de_identificacion==IDENTIFICACION[0]:
			if len(dni) <8 or len(dni)>10:
				raise forms.ValidationError("DNI debe tener de 8 a 10 digitos")
			elif not dni.isdigit():
				raise forms.ValidationError("DNI solo debe contener numeros del 0-9")
		return dni



class ChangeEgresadoPasswordForm(forms.Form):
	contraseña= forms.CharField(label="Contraseña", required=True, widget= forms.PasswordInput(attrs= {'class':'form-control mb-2', 'placeholder':'Contraseña antigua'})) 
	contraseñanueva = forms.CharField(label="Contraseña nueva", required=True, widget= forms.PasswordInput(attrs= {'class':'form-control mb-2', 'placeholder':'Contraseña nueva'})) 
	confirmarcontraseña = forms.CharField(label="Confirmar contraseña", required=True, widget= forms.PasswordInput(attrs= {'class':'form-control mb-2', 'placeholder':'Confirmar contraseña'})) 


	def clean_contraseñanueva(self):
		contraseñanueva= self.cleaned_data['contraseñanueva']
		if contraseñanueva.isdigit():
			raise forms.ValidationError('Su contraseña no puede ser completamente numérica')
		elif len(contraseñanueva)<8:
			raise forms.ValidationError('Su contraseña debe tener al menos 8 caracteres')
		return contraseñanueva

	def clean_confirmarcontraseña(self):
		confirmarcontraseña= self.cleaned_data['confirmarcontraseña']
		if confirmarcontraseña.isdigit():
			raise forms.ValidationError('Su contraseña no puede ser completamente numérica')
		elif len(confirmarcontraseña)<8:
			raise forms.ValidationError('Su contraseña debe tener al menos 8 caracteres')
		return confirmarcontraseña
