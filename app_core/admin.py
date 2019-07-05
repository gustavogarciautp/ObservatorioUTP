from django.contrib import admin
from django.contrib.admin import AdminSite
# Register your models here.
from .models import Egresado, Administrador, Intereses, Interes, User, EgresadosUTP, City, Country
from django.contrib.auth.models import Group
from .forms import AdminForm
#from app_registrarse.models import Perfil

class AdminSuperuser(admin.ModelAdmin):
	exclude= ('id_restablecimiento','is_staff','is_superuser','is_active', 'is_superusuario','is_administrador', 'is_egresado','password')
	readonly_fields = ('last_login',)
	search_fields = ['nombres','apellidos','email']
	list_display= ('nombres','apellidos','email','last_login')
	list_filter = ['Tipo_de_identificacion','genero','last_login']

	def get_form(self, request, obj=None, **kwargs):
		return AdminForm


admin.site.register(Administrador, AdminSuperuser)

#Quitar ver sitio
#admin.site.site_url=None


class Admin_Site(AdminSite):
    site_header = "Administrador"
    site_title = "Portal administrativo"
    index_title = "Bienvenido al portal de administración"

admin_site = Admin_Site(name='admin_site')

class AdminEgresado(admin.ModelAdmin):
	#exclude= ('is_superuser','is_staff','id_restablecimiento', 'is_active','is_egresado','is_administrador', 'is_superusuario')
	fieldsets = [
		(None, {'fields': ['Tipo_de_identificacion','DNI','nombres','apellidos', 'genero','email','pais','ciudad','validado','activacion','last_login']}),
		('Perfil', {'fields':['bio','avatar']})]
	search_fields = ['nombres','apellidos','email']
	list_display= ('nombres','apellidos','email', 'activacion','validado','last_login')
	readonly_fields = ('DNI','Tipo_de_identificacion','nombres','apellidos','genero','email','pais','ciudad','validado','last_login','bio','avatar')
	list_filter = ['Tipo_de_identificacion','genero','activacion','validado','last_login']

admin_site.register(Egresado, AdminEgresado)

class InteresEgresado(admin.ModelAdmin):
	search_fields = ('nombre',)
	list_filter = ['created','updated']
	list_display = ('nombre','created','updated')

admin_site.register(Interes, InteresEgresado)
admin_site.register(Intereses)