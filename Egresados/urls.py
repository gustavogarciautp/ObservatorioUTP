"""Egresados URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from app_core import views as app_core_views  #importamos de nuestra app core el fichero views
from app_registrarse import views as app_registrarse_views
from django.conf import settings
from app_core.admin import admin_site
from app_registrarse.views import ProfileUpdate, EmailUpdate, BuscarCiudades
from perfiles.urls import profiles_patterns
from messenger.urls import messenger_patterns
from contenido.urls import contenido_patterns

urlpatterns = [
    path('registrarse/', app_registrarse_views.registrarse, name='registrarse'),
    path('', app_core_views.home, name="home_page"),
    path('jet/', include('jet.urls', 'jet')),
	path('login/', app_core_views.login,name='login_'),
    
    path('ad-min/', app_core_views.login, name='admin_'),
    path('admin_admin/', admin_site.urls, name='admin2'),
	path('accounts/', include('django.contrib.auth.urls')),    
    path('recuperar_1/', app_core_views.recuperar_1, name='recuperar_1'),
    path('recuperar_2/', include('app_core.urls'), name='recuperar_1'),
    
    path('principal/', app_core_views.principal, name='principal'),
    
    path('admin_super_user/', admin.site.urls, name='super2'),
    path('super-user/', app_core_views.login, name='super'),
    
    path('404/', app_core_views.page404, name='404'),
    path('perfil/', ProfileUpdate.as_view(), name='perfil'),
    path('perfil/email/', EmailUpdate.as_view(), name='perfil_email'),

    path('profiles/', include(profiles_patterns)),

    path('messenger/', include(messenger_patterns)),

    path('publicaciones/', include(contenido_patterns)),

    path('ciudades/', BuscarCiudades, name="cities"),
    path('adminprofile/', app_core_views.EditUser, name='perfil_admin'),

]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'Observatorio UTP'
