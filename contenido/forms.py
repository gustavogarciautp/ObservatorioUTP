from django import forms
from .models import Noticia

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo','descripcion','Image','categorias']
        widgets = {
        	'titulo': forms.TextInput(attrs={"class":"form-control"}),
        	'descripcion': forms.Textarea(attrs={"class":"form-control"}),
        }