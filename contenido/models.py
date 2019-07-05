from django.db import models
from ckeditor.fields import RichTextField
from app_core.models import Interes
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.core import mail
from django.core.mail import EmailMultiAlternatives


# Create your models here.
class Noticia(models.Model):
	titulo = models.CharField(max_length=200, verbose_name='Titulo')
	descripcion = RichTextField(verbose_name='Descripción')
	Image= models.ImageField(verbose_name='Imagen', upload_to='contenidos')
	created = models.DateTimeField(auto_now_add= True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
	categorias = models.ManyToManyField(Interes, related_name="get_noticias")


	class Meta:
		verbose_name = 'Noticia'
		verbose_name_plural= 'Noticias'
		ordering = ["-created"]
	def __str__(self):
		return self.titulo

"""
@receiver(post_save, sender= Noticia)
def publicar_noticia_email(sender, instance, **kwargs):
    if kwargs.get('created', False): #con esto nos aseguramos que la instancia se acaba de crear   
        
        categories= instance.categorias.all()
        categories_piv =Intereses.objects.filter(interes__in=categories)
        emails={}
        for category_piv in categories_piv:
        	emails.add(category_piv.egresado.email)

        asunto= 'Observatorio Egresado UTP'

        html_content='<p></p>'

        messages=[]
        for email in emails:
	        msg = EmailMultiAlternatives(asunto, '', to=[email])
	        msg.attach_alternative(html_content, "text/html")
	        messages.append(msg)

	  	connection = mail.get_connection()   # Use default email connection
        connection.send_messages(messages)
"""