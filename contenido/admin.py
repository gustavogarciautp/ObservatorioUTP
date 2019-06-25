from .models import Noticia
from app_core.admin import admin_site
from django.contrib import admin

class NoticiaAdmin(admin.ModelAdmin):
	#readonly_fields = ('created', 'updated')


	class  Media :
		css = {
		' all ' : ('contenido/css/custom_ckeditor.css',)
	}
# Register your models here.
#admin_site.register(Noticia, NoticiaAdmin)
admin_site.register(Noticia)

