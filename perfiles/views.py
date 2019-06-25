from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from app_registrarse.models import Perfil


# Create your views here.
class ProfileListView(ListView):
    print("------------------------------------")
    model = Perfil
    template_name = 'perfiles/profile_list.html'
    paginate_by = 3

class ProfileDetailView(DetailView):
    model = Perfil
    template_name = 'perfiles/profile_detail.html'

    def get_object(self):
        print(self.kwargs)
        return get_object_or_404(Perfil, user__nombres=self.kwargs['email'])