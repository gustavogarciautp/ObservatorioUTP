from django.contrib import admin
from django.contrib.admin import AdminSite
# Register your models here.
from .models import Egresado, Administrador, Intereses, Interes, User, EgresadosUTP, City, Country
from django.contrib.auth.models import Group
from .forms import AdminForm

class AdminSuperuser(admin.ModelAdmin):
	exclude= ('id_restablecimiento','is_staff','is_superuser','is_active', 'is_superusuario','is_administrador', 'is_egresado')
	readonly_fields = ('last_login',)
	search_fields = ['nombres','apellidos','email']
	list_display= ('nombres','apellidos','email')

	def get_form(self, request, obj=None, **kwargs):
		return AdminForm


admin.site.register(Administrador, AdminSuperuser)
admin.site.unregister(Group)

#Quitar ver sitio
#admin.site.site_url=None


class Admin_Site(AdminSite):
    site_header = "Administrador"
    site_title = "Portal administrativo"
    index_title = "Bienvenido al portal de administración"

admin_site = Admin_Site(name='admin_site')

admin_site.register(Intereses)
admin_site.register(Interes)

class AdminEgresado(admin.ModelAdmin):
	#exclude= ('is_superuser','is_staff','id_restablecimiento', 'is_active','is_egresado','is_administrador', 'is_superusuario')
	fields = ('Tipo_de_identificacion','DNI','nombres','apellidos', 'genero','email','pais','ciudad','validado','activacion','last_login')
	search_fields = ['nombres','apellidos','email']
	list_display= ('nombres','apellidos','email', 'activacion','validado')
	readonly_fields = ('DNI','Tipo_de_identificacion','nombres','apellidos','genero','email','pais','ciudad','validado','last_login')

admin_site.register(Egresado, AdminEgresado)