from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone 
import re
from cities_light.abstract_models import AbstractCity, AbstractRegion,AbstractCountry
from cities_light.receivers import connect_default_signals

IDENTIFICACION= ["Cédula de ciudadania", "Pasaporte"]

#COUNTRIES=["Afganistán", "Akrotiri", "Albania", "Alemania", "Andorra", "Angola", "Anguila", "Antártida", "Antigua y Barbuda", "Antillas Neerlandesas", "Arabia Saudí", "Arctic Ocean", "Argelia", "Argentina", "Armenia", "Aruba", "Ashmore andCartier Islands", "Atlantic Ocean", "Australia", "Austria", "Azerbaiyán", "Bahamas", "Bahráin", "Bangladesh", "Barbados", "Bélgica", "Belice", "Benín", "Bermudas", "Bielorrusia", "Birmania Myanmar", "Bolivia", "Bosnia y Hercegovina", "Botsuana", "Brasil", "Brunéi", "Bulgaria", "Burkina Faso", "Burundi", "Bután", "Cabo Verde", "Camboya", "Camerún", "Canadá", "Chad", "Chile", "China", "Chipre", "Clipperton Island", "Colombia", "Comoras", "Congo", "Coral Sea Islands", "Corea del Norte", "Corea del Sur", "Costa de Marfil", "Costa Rica", "Croacia", "Cuba", "Dhekelia", "Dinamarca", "Dominica", "Ecuador", "Egipto", "El Salvador", "El Vaticano", "Emiratos Árabes Unidos", "Eritrea", "Eslovaquia", "Eslovenia", "España", "Estados Unidos", "Estonia", "Etiopía", "Filipinas", "Finlandia", "Fiyi", "Francia", "Gabón", "Gambia", "Gaza Strip", "Georgia", "Ghana", "Gibraltar", "Granada", "Grecia", "Groenlandia", "Guam", "Guatemala", "Guernsey", "Guinea", "Guinea Ecuatorial", "Guinea-Bissau", "Guyana", "Haití", "Honduras", "Hong Kong", "Hungría", "India", "Indian Ocean", "Indonesia", "Irán", "Iraq", "Irlanda", "Isla Bouvet", "Isla Christmas", "Isla Norfolk", "Islandia", "Islas Caimán", "Islas Cocos", "Islas Cook", "Islas Feroe", "Islas Georgia del Sur y Sandwich del Sur", "Islas Heard y McDonald", "Islas Malvinas", "Islas Marianas del Norte", "IslasMarshall", "Islas Pitcairn", "Islas Salomón", "Islas Turcas y Caicos", "Islas Vírgenes Americanas", "Islas Vírgenes Británicas", "Israel", "Italia", "Jamaica", "Jan Mayen", "Japón", "Jersey", "Jordania", "Kazajistán", "Kenia", "Kirguizistán", "Kiribati", "Kuwait", "Laos", "Lesoto", "Letonia", "Líbano", "Liberia", "Libia", "Liechtenstein", "Lituania", "Luxemburgo", "Macao", "Macedonia", "Madagascar", "Malasia", "Malaui", "Maldivas", "Malí", "Malta", "Man, Isle of", "Marruecos", "Mauricio", "Mauritania", "Mayotte", "México", "Micronesia", "Moldavia", "Mónaco", "Mongolia", "Montserrat", "Mozambique", "Namibia", "Nauru", "Navassa Island", "Nepal", "Nicaragua", "Níger", "Nigeria", "Niue", "Noruega", "Nueva Caledonia", "Nueva Zelanda", "Omán", "Pacific Ocean", "Países Bajos", "Pakistán", "Palaos", "Panamá", "Papúa-Nueva Guinea", "Paracel Islands", "Paraguay", "Perú", "Polinesia Francesa", "Polonia", "Portugal", "Puerto Rico", "Qatar", "Reino Unido", "República Centroafricana", "República Checa", "República Democrática del Congo", "República Dominicana", "Ruanda", "Rumania", "Rusia", "Sáhara Occidental", "Samoa", "Samoa Americana", "San Cristóbal y Nieves", "San Marino", "San Pedro y Miquelón", "San Vicente y las Granadinas", "Santa Helena", "Santa Lucía", "Santo Tomé y Príncipe", "Senegal", "Seychelles", "Sierra Leona", "Singapur", "Siria", "Somalia", "Southern Ocean", "Spratly Islands", "Sri Lanka", "Suazilandia", "Sudáfrica", "Sudán", "Suecia", "Suiza", "Surinam", "Svalbard y Jan Mayen", "Tailandia", "Taiwán", "Tanzania", "Tayikistán", "TerritorioBritánicodel Océano Indico", "Territorios Australes Franceses", "Timor Oriental", "Togo", "Tokelau", "Tonga", "Trinidad y Tobago", "Túnez", "Turkmenistán", "Turquía", "Tuvalu", "Ucrania", "Uganda", "Unión Europea", "Uruguay", "Uzbekistán", "Vanuatu", "Venezuela", "Vietnam", "Wake Island", "Wallis y Futuna", "West Bank", "World", "Yemen", "Yibuti", "Zambia", "Zimbabue"]  

#PAISES=[[x,x] for x in COUNTRIES]

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

class Country(AbstractCountry):
    pass

connect_default_signals(Country)
class Region(AbstractRegion):
    pass
connect_default_signals(Region)
class City(AbstractCity):
    pass
connect_default_signals(City)

"""
class Paises(models.Model):
    iso= models.CharField(max_length=4, primary_key=True)
    pais=models.CharField(max_length=20, null=False, default='', blank=False, choices=PAISES)

    class Meta:
        verbose_name = 'Pais'
        verbose_name_plural = "Paises"

    def __str__(self):
        return self.pais

class Ciudades(models.Model):
    pais_iso= models.ForeignKey(Paises, on_delete=models.CASCADE)
    ciudad= models.CharField(max_length=20, null=False, default='', blank=False)
    autocomplete_fields = ['pais_iso']
    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = "Ciudades"

    def __str__(self):
        return self.ciudad
"""
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
        patron=re.compile(r'egresado')
        m= patron.search(perm)
        if m:
            return False
        else:
            patron=re.compile(r'interes')
            m=patron.search(perm)
            if m:
                return False
            else:     
                patron=re.compile(r'noticia')
                m=patron.search(perm)          
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
    nombres =models.CharField(verbose_name= "Nombres", default='',max_length=30, blank= False, null=False)
    apellidos = models.CharField(verbose_name= "Apellidos", default='',max_length=30, blank= False, null=False)
    pais = models.ForeignKey(City, on_delete=models.CASCADE, default='', blank=True, null=True)
    email = models.EmailField(verbose_name="Email",default='',null= False, blank= False, unique=True, max_length=255) #campo opcional
    genero = models.CharField(verbose_name="Genero",default='',null= True, blank= True, max_length=10, choices=GENEROS) #campo opcional
    #contraseña = models.CharField(verbose_name="Contraseña",default='',null= False, blank= False, max_length=128) #campo opcional
    id_restablecimiento = models.CharField(verbose_name="Id Recuperacion", default='', null=True, blank=True, max_length=60)
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
    Tipo_de_identificacion = models.CharField(verbose_name= "ID", default='Cédula de ciudadania', null=False, blank=False, max_length=20)
    DNI  = models.CharField(verbose_name= "DNI", default= '', null=False, blank=False, max_length=10)
    telefono = models.IntegerField(verbose_name= "Telefono", default='', null=True, blank=True)
    direccion = models.CharField(verbose_name= "Direccion", max_length=30, blank= False, null=False)
    ciudad= models.ForeignKey(City, on_delete= models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_egresado = models.BooleanField(default=False)
    is_administrador = models.BooleanField(default=True)
    is_superusuario = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        patron=re.compile(r'administrador')
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


class Egresado (User):
    Tipo_de_identificacion = models.CharField(verbose_name= "Identificacion", default='Cédula de ciudadania', null=False, blank=False,max_length=20)
    DNI  = models.CharField(verbose_name= "DNI", default= '', null=False, blank=False, max_length=10)
    activacion= models.BooleanField(verbose_name= "Activacion", default= False, null=True, blank= False)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento",null= True, blank= True) #campo opcional
    is_active = models.BooleanField(default=True)
    is_egresado = models.BooleanField(default=True)
    is_administrador = models.BooleanField(default=False)
    is_superusuario = models.BooleanField(default=False)
    validado = models.BooleanField(default= False)

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



