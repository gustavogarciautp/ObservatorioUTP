from django.db import models
from app_core.models import Egresado

from django.dispatch import receiver
from django.db.models.signals import post_save

def custom_upload_to(instance, filename):
    old_instance = Perfil.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/'+filename

"""
class Perfil(models.Model):
    user= models.OneToOneField(Egresado, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to= custom_upload_to, null=True, blank=True)
    bio= models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['user__nombres']
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfil'

    def __str__(self):
        return self.user.nombres

"""
#Confirma que el perfil siempre existe

@receiver(post_save, sender= Egresado)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False): #con esto nos aseguramos que la instancia se acaba de crear   
        Perfil.objects.get_or_create(user=instance)
        print("Se ha acabado de crear un usuario y su perfil enlazado")

