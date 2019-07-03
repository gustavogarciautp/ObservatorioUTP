from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone 
import re
from cities_light.abstract_models import AbstractCity, AbstractRegion,AbstractCountry
from cities_light.receivers import connect_default_signals
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives



IDENTIFICACION= [["Cédula de ciudadania","Cédula de ciudadania"], ["Pasaporte", "Pasaporte"]]

GENEROS= (
    ('Masculino','Masculino'),
    ('Femenino', 'Femenino'),
    ('Otros', 'Otros'),
    )

years=[i for i in range(1930,1999)]


months= {
    1: ('Enero'), 2: ('Febrero'), 3: ('Marzo'), 4: ('Abril'), 5: ('Mayo'), 6: ('Junio'),
    7: ('Julio'), 8: ('Agosto'), 9: ('Septiembre'), 10: ('Octubre'), 11: ('Noviembre'),
    12: ('Diciembre')
}

def custom_upload_to(instance, filename):
    old_instance = Egresado.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/'+filename


class Country(AbstractCountry):
    def __str__(self):
        return self.name

connect_default_signals(Country)
class Region(AbstractRegion):
    pass
connect_default_signals(Region)
class City(AbstractCity):
    def __str__(self):
        return self.name
connect_default_signals(City)

class SuperUser(AbstractBaseUser):
    email= models.EmailField(verbose_name="Email",default='',null= False, blank= False, unique=True, max_length=255) #campo opcional
    password = models.CharField(verbose_name="Password",default='',null= False, blank= False, max_length=128) #campo opcional
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_egresado = models.BooleanField(default=False)
    is_administrador = models.BooleanField(default=False)
    is_superusuario = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        patron=re.compile(r'egresado|interes|noticia|city|country|region')
        m= patron.search(perm)
        if m:
            return False
        else:
            return True


    def has_module_perms(self, app_label):
        if app_label=='app_core':
            return True
        else:
            return False

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    """def create_superuser(self, email, password):
        print("hola")
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = False
        user.is_superuser = True
        user.save(using=self._db)
        return user"""
    def create_superuser(self, email, password):
        user = SuperUser.objects.create(email=email)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    Tipo_de_identificacion = models.CharField(verbose_name= "Identificacion", default='Cédula de ciudadania', null=False, blank=False,max_length=20, choices=IDENTIFICACION)
    DNI  = models.CharField(verbose_name= "DNI", default= '', null=False, blank=False, max_length=10)
    nombres =models.CharField(verbose_name= "Nombres", default='',max_length=30, blank= False, null=False)
    apellidos = models.CharField(verbose_name= "Apellidos", default='',max_length=30, blank= False, null=False)
    pais = models.CharField(verbose_name="Pais", default='', null=False, blank= False, max_length=30) 
    ciudad= models.CharField(verbose_name="Ciudad", max_length=30, default='')
    email = models.EmailField(verbose_name="Email",default='',null= False, blank= False, unique=False, max_length=255) #campo opcional
    genero = models.CharField(verbose_name="Genero",default='',null= True, blank= True, max_length=10, choices=GENEROS) #campo opcional
    #contraseña = models.CharField(verbose_name="Contraseña",default='',null= False, blank= False, max_length=128) #campo opcional
    id_restablecimiento = models.CharField(verbose_name="Id Recuperacion", default='', null=True, blank=True, max_length=180)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    password = models.CharField(verbose_name="Password",default='',null= False, blank= False, max_length=128) #campo opcional

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    """"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    """

    def __str__(self):
        return self.email

class Administrador (User):
    telefono = models.IntegerField(verbose_name= "Telefono", default='', null=True, blank=True)
    direccion = models.CharField(verbose_name= "Direccion", max_length=30, blank= False, null=False)
    is_active = models.BooleanField(default=True)
    is_egresado = models.BooleanField(default=False)
    is_administrador = models.BooleanField(default=True)
    is_superusuario = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        patron=re.compile(r'administrador|city|country|region')
        m= patron.search(perm)
        if m:
            return False
        else:          
            return True

    def has_module_perms(self, app_label):
        if app_label=='app_core' or app_label=='contenido':
            return True
        else:
            return False

    class Meta:
        verbose_name = 'Administrador'
        verbose_name_plural= 'Administradores'

    def __str__(self):
        return self.nombres

@receiver(post_save, sender= Administrador)
def make_first_password(sender, instance, **kwargs):
    if kwargs.get('created', False): #con esto nos aseguramos que la instancia se acaba de crear   
        password_gen = get_random_string(length=15)
        #instance.password = password_gen
        instance.set_password(password_gen)

        asunto= '!Bienvenido al sitio de administración del Sistema de Egresados UTP!'

        clave=get_random_string(length=50)
        instance.id_restablecimiento=clave

        html_content='<p>Ha recibido este correo electrónico porque ha sido registrada una cuenta de administrador con los siguientes datos:</p></br><p>Nombre de Usuario: '+instance.email+'</p></br><p>Contraseña: '+password_gen+'</p></br><p>Para iniciar sesión por primera vez debera cambiar su actual contraseña, puede hacerlo a través del siguiente enlace:</p></br><p><a href="http://127.0.0.1:8000/change_password/first/'+clave+'">Cambiar contraseña</a></p></br><p>¡Gracias por usar nuestro sitio!</p></br><p>El equipo de <a href=" http://127.0.0.1:8000">Observatorio Egresados</a></p>'
        msg = EmailMultiAlternatives(asunto, '', to=[instance.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        instance.save()



class Egresado (User):
    activacion= models.BooleanField(verbose_name= "Activacion", default= False, null=True, blank= False)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento",null= True, blank= True) #campo opcional
    is_active = models.BooleanField(default=True)
    is_egresado = models.BooleanField(default=True)
    is_administrador = models.BooleanField(default=False)
    is_superusuario = models.BooleanField(default=False)
    validado = models.BooleanField(default= False)
    avatar = models.ImageField(upload_to= custom_upload_to, null=True, blank=True)
    avatar_p = models. BooleanField(null = False, blank = False, default = True)
    bio_p = models. BooleanField(null = False, blank = False, default = True)
    nombres_p = models. BooleanField(null = False, blank = False, default = True)
    fecha_p = models. BooleanField(null = False, blank = False, default = True)
    email_p = models. BooleanField(null = False, blank = False, default = True)
    pais_p = models. BooleanField(null = False, blank = False, default = True)
    bio= models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Egresado'
        verbose_name_plural= 'Egresados'
        #ordering = ['order','title']

    def has_perm(self, perm, obj=None):
        return False

    def has_module_perms(self, app_label):
        return False

    def activate(self):
        return self.activacion

    def __str__(self):
        return self.nombres



class Interes(models.Model):
    nombre = models.CharField(verbose_name= "Nombre", default='', null=True, blank= False, max_length=30)
    created = models.DateTimeField(auto_now_add= True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")


    class Meta:
        verbose_name = 'Interes'
        verbose_name_plural= 'Interes'
        ordering = ['-created']

    def __str__(self):
        return self.nombre


class Intereses(models.Model):
    interes = models.ForeignKey(Interes, on_delete=models.CASCADE)
    egresado= models.ForeignKey(Egresado, on_delete= models.CASCADE)

    class Meta:
        verbose_name = 'Intereses'
        verbose_name_plural= 'Intereses'

    def __str__(self):
        return self.egresado.nombres+'-'+self.interes.nombre



class EgresadosUTP(models.Model):
    DNI  = models.CharField(verbose_name= "DNI", default= '', null=False, blank=False, max_length=10)
    # 8-10 numeros, pasaporte 3 primeras letras y siguientes 3 numeros, 
    nombres =models.CharField(verbose_name= "Nombres", default='',max_length=30, blank= False, null=False)
    apellidos = models.CharField(verbose_name= "Apellidos", default='',max_length=30, blank= False, null=False)
    email = models.EmailField(verbose_name="Email",default='',null= False, blank= False, unique=True, max_length=255) #campo opcional



