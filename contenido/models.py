from django.db import models
from ckeditor.fields import RichTextField
from app_core.models import Interes, Intereses
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save,m2m_changed
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from ckeditor_uploader.fields import RichTextUploadingField
from email.mime.image import MIMEImage
import re
import datetime

def slugify(s):
    s = s.lower()
    for c in [' ', '-', '.', '/']:
        s = s.replace(c, '_')
    s = re.sub('\W', '', s)
    s = s.replace('_', ' ')
    s = re.sub('\s+', ' ', s)
    s = s.strip()
    s = s.replace(' ', '-')

    return s

# Create your models here.
class Noticia(models.Model):
	titulo = models.CharField(max_length=200, verbose_name='Titulo')
	descripcion = RichTextUploadingField(blank=True, null=True,
                                      		external_plugin_resources=[(
                                          'youtube',
                                          '/static/contenido/css/youtube/youtube/',
                                          'plugin.js',
                                          )])  #RichTextField(verbose_name='Descripción')
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


@receiver(m2m_changed, sender= Noticia.categorias.through)
def publicar_noticia_email(sender,**kwargs):
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)    
    instance = kwargs.pop('instance',None) #Noticia Instance
    image_path = '/media/contenidos/contact_48mOI4g.jpg'
    if action == "post_add":
        categories = Interes.objects.filter(pk__in= pk_set)
        categories_piv =Intereses.objects.filter(interes__in=categories)
        emails=set()
        print(categories_piv)
        for category_piv in categories_piv:
            if category_piv.egresado.activacion:
                emails.add(category_piv.egresado.email)
        print(emails)
        asunto= 'Observatorio Egresado UTP'

        i=0
        categorias_content = ''''''
        for cat in instance.categorias.all():
            categorias_content+='''<a href="http://observatorioutp.pythonanywhere.com/publicaciones/categoria/'''+str(cat.id)+'''/" class="link">'''+cat.nombre+'''</a>'''
            if (i!=len(instance.categorias.all())-1):
                categorias_content+=''','''
            i+=1


        html_content='''
				<!DOCTYPE html>
				<html lang="es">
				<body>
				  <section class="page-section cta">
				    <div class="container">
				      <div class="row">
				        <div class="col-xl-9 mx-auto">
				          <div class="cta-innerv text-center rounded">
				            <h2 class="section-heading mb-5">
				              <span class="section-heading-lower">'''+instance.titulo+'''</span>
				            </h2>
				            <p class="mb-0">
				              <img class="mx-auto d-flex rounded img-fluid mb-3 mb-lg-0" src="http://observatorioutp.pythonanywhere.com'''+instance.Image.url+'''" alt="">
				            </p>
				            <br>
				            <br>
				            <div class="text-justify">
				            <p class="mb-0 mbt">
				              '''+instance.descripcion[:240]+'''...
				            </p>
				            </div>
				            <p><a href="http://observatorioutp.pythonanywhere.com/publicaciones/'''+str(instance.pk)+'''/'''+slugify(instance.titulo)+'''/">Leer más</a>
				          </p>
				          <p class="mb-0 mbt">
		                      <em>
		                      	'''+categorias_content+'''	
		                      </em>
		                  </p>
		                  Publicado: '''+instance.created.strftime("%Y"+"-"+"%m"+"-"+"%d")+'''
				          </div>

				        </div>
				      </div>
				    </div>
				  </section>
				</body>
				</html>
				'''

        messages=[]
        for email in emails:
            msg = EmailMultiAlternatives(asunto, '', to=[email])
            msg.attach_alternative(html_content, "text/html")
            msg.content_subtype = 'html'  # set primary content to be text/html
            msg.mixed_subtype = 'related' # it is important part that ensures embedding of image 
            messages.append(msg)

        connection = mail.get_connection()   # Use default email connection
        connection.send_messages(messages)
        
    """if kwargs.get('created', False): #con esto nos aseguramos que la instancia se acaba de crear   
        
        categories= instance.categorias.all()
        print(categories)
        print(instance.pk)
        #c=Noticia.objects.get(pk=15)
        print(instance.titulo)
        print(instance.descripcion)
        print(instance.categorias)


        categories_piv =Intereses.objects.filter(interes__in=categories)
        print(categories_piv)
        emails={}
        for category_piv in categories_piv:
            print(category_piv.egresado)
            if category_piv.egresado.activacion:
                emails.add(category_piv.egresado.email)
        asunto= 'Observatorio Egresado UTP'

        html_content='''
				<!DOCTYPE html>
				<html lang="es">
				<body>
				  <section class="page-section cta">
				    <div class="container">
				      <div class="row">
				        <div class="col-xl-9 mx-auto">
				          <div class="cta-innerv text-center rounded">
				            <h2 class="section-heading mb-5">
				              <span class="section-heading-lower">'''+instance.titulo+'''</span>
				            </h2>
				            <p class="mb-0">
				              <img class="mx-auto d-flex rounded img-fluid mb-3 mb-lg-0" src='''+instance.Image.url+''' alt="">
				            </p>
				            <br>
				            <br>
				            <div class="text-justify">
				            <p class="mb-0 mbt">
				              '''+instance.descripcion+'''
				            </p>
				            </div>
				            <p><a href="">Leer más</a>
				          </p>
				          </div>

				        </div>
				      </div>
				    </div>
				  </section>
				</body>
				</html>
				'''

        messages=[]
        for email in emails:
            msg = EmailMultiAlternatives(asunto, '', to=[email])
            msg.attach_alternative(html_content, "text/html")
            messages.append(msg)

        connection = mail.get_connection()   # Use default email connection
        connection.send_messages(messages)
		"""