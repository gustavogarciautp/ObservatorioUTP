from django.urls import path

from . import views

urlpatterns = [
    path('<id_recuperacion>/', views.recuperar_2, name="recuperar_2"),
]
