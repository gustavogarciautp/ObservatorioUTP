from django.conf import settings
from django.contrib.auth.hashers import check_password
from app_core.models import Administrador, Egresado, User, SuperUser
from django.urls import resolve 


class AdminBackend:
	def authenticate(self, request, email=None, password=None):
		current_url= resolve(request.path_info).url_name
		if current_url=="admin_":
			try:
				#user = 	Administrador.objects.get(email=email, password=password)
				user = 	Administrador.objects.get(email=email)
				success=user.check_password(password)
				if success:
					return user
				else:
					return None
				return user
			except Administrador.DoesNotExist:
				return None
		else:
			return None

	def get_user(self, user_id):
		try:
			return Administrador.objects.get(pk=user_id)
		except Administrador.DoesNotExist:
			return None

class EgresadoBackend:    
	def authenticate(self, request, email=None, password=None):
		current_url= resolve(request.path_info).url_name
		if current_url=="login_":
			try:
				user = 	Egresado.objects.get(email=email)
				success=user.check_password(password)
				if success:
					return user
				else:
					return None
			except Egresado.DoesNotExist:
				return None
		else:
			None

	def get_user(self, user_id):
		try:
			return Egresado.objects.get(pk=user_id)
		except Egresado.DoesNotExist:
			return None

class SuperUserBackend:   
	def authenticate(self, request, email=None, password=None):
		current_url= resolve(request.path_info).url_name
		if current_url=="super":
			try:
				user = 	SuperUser.objects.get(email=email)
				success=user.check_password(password)
				current_url= resolve(request.path_info).url_name
				if success:
					return user
				else:
					return None
			except SuperUser.DoesNotExist:
				return None
		else:
			return None

	def get_user(self, user_id):
		try:
			return SuperUser.objects.get(pk=user_id)
		except SuperUser.DoesNotExist:
			return None



