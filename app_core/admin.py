from django.contrib import admin
from django.contrib.admin import AdminSite
# Register your models here.
from .models import Egresado, Administrador, Intereses, Interes, User, EgresadosUTP, City, Country
from django.contrib.auth.models import Group


class AdminSuperuser(admin.ModelAdmin):
	exclude= ('id_restablecimiento','is_staff','is_superuser','is_active', 'is_superusuario','is_administrador', 'is_egresado')
	readonly_fields = ('last_login',)
	list_display= ('nombres','apellidos','email')


admin.site.register(Administrador, AdminSuperuser)
admin.site.unregister(Group)
#Quitar ver sitio
admin.site.site_url=None


class Admin_Site(AdminSite):
    site_header = "Administrador"
    site_title = "Portal administratico"
    index_title = "Bienvenido al portal de administración"

admin_site = Admin_Site(name='admin_site')

admin_site.register(Intereses)
admin_site.register(Interes)
#admin_site.register(Paises)
#admin_site.register(Ciudades)
#admin_site.register(EgresadosUTP)

class AdminEgresado(admin.ModelAdmin):
	exclude= ('is_superuser','is_staff','id_restablecimiento', 'is_active','is_egresado','is_administrador', 'is_superusuario')
	search_fields = ['ciudad']
	list_display= ('nombres','apellidos','email', 'activacion','validado')
	readonly_fields = ('DNI','Tipo_de_identificacion', 'validado')

admin_site.register(Egresado, AdminEgresado)