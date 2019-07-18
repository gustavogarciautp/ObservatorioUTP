from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Thread, Message
from django.views.generic import TemplateView
from django.http import Http404, JsonResponse
from app_registrarse.models import Egresado
from django.urls import reverse_lazy, reverse
from app_registrarse.views import EgresadoRequiredMixin
from django.views import View
from app_core.models import Circulo


from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.enums import PNStatusCategory
from pubnub.callbacks import SubscribeCallback 

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-d21b3856-9daf-11e9-b575-2aabfc211be0"
pnconfig.publish_key = "pub-c-a0748278-adf4-4a7b-b141-c2d7a2571a42"
pnconfig.ssl = False
 
pubnub = PubNub(pnconfig)

"""
class MyListener(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            pass
 
    def message(self, pubnub, message):
        print(message.message)
 
    def presence(self, pubnub, presence):
        pass
 
my_listener = MyListener()
 
pubnub.add_listener(my_listener)
 
pubnub.subscribe().channels("sala1").execute()
"""

# Create your views here.
class ThreadList(EgresadoRequiredMixin, TemplateView):

	template_name = "messenger/thread_list.html"


class ThreadDetail(EgresadoRequiredMixin, DetailView):
	model = Thread


	def get_object(self):
		#print("2222222222222222S")
		obj = super(ThreadDetail, self).get_object()
		if self.request.user not in obj.users.all() or len(obj.users.all())<2:
			raise Http404
		return obj


def add_message(request, pk):
	json_response = {'created': False}
	if request.user.is_authenticated and request.user.is_egresado:
		content = request.GET.get('content', None)
		if content:
			pubnub.publish().channel(pk).message({"Remitente":request.user.nombres,"Mensaje": content}).sync()

			thread = get_object_or_404(Thread, pk= pk)
			message = Message.objects.create(user= request.user, content= content)
			thread.messages.add(message)
			print(message.created)
			print(type(message.created))
			print(str(message.created))
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