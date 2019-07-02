from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from app_registrarse.models import Perfil
from app_registrarse.views import EgresadoRequiredMixin


# Create your views here.
class ProfileListView(EgresadoRequiredMixin,ListView):
    model = Perfil
    template_name = 'perfiles/profile_list.html'
    paginate_by = 3

class ProfileDetailView(EgresadoRequiredMixin, DetailView):
    model = Perfil
    template_name = 'perfiles/profile_detail.html'

    def get_object(self):
        return get_object_or_404(Perfil, user__email=self.kwargs['email'])