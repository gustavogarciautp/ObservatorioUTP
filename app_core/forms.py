from django import forms
#from .models import Paises

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
