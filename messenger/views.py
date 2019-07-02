from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Thread, Message
from django.views.generic import TemplateView
from django.http import Http404, JsonResponse
from app_registrarse.models import Egresado
from django.urls import reverse_lazy, reverse
from app_registrarse.views import EgresadoRequiredMixin

# Create your views here.
class ThreadList(EgresadoRequiredMixin, TemplateView):
	template_name = "messenger/thread_list.html"

class ThreadDetail(EgresadoRequiredMixin, DetailView):
	model = Thread

	def get_object(self):
		obj = super(ThreadDetail, self).get_object()
		if self.request.user not in obj.users.all():
			raise Http404
		return obj

def add_message(request, pk):
	json_response = {'created': False}
	if request.user.is_authenticated and request.user.is_egresado:
		content = request.GET.get('content', None)
		if content:
			thread = get_object_or_404(Thread, pk= pk)
			message = Message.objects.create(user= request.user, content= content)
			thread.messages.add(message)
			json_response['created']= True
			if len(thread.messages.all()) is 1:
				json_response['first'] = True
	else:
		raise Http404("Usuario is not authenticated")
	return JsonResponse(json_response)

def start_thread(request, email):
	if request.user.is_authenticated and request.user.is_egresado:
		user = get_object_or_404(Egresado, email= email)
		thread = Thread.objects.find_or_create(user, request.user)
		return redirect(reverse_lazy('messenger:detail', args=[thread.pk]))
	else:
		return redirect(reverse('login_'))