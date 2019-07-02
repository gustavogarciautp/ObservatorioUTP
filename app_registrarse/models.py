from django.db import models
from app_core.models import Egresado

from django.dispatch import receiver
from django.db.models.signals import post_save

def custom_upload_to(instance, filename):
    old_instance = Perfil.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/'+filename

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

#Confirma que el perfil siempre existe

@receiver(post_save, sender= Egresado)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False): #con esto nos aseguramos que la instancia se acaba de crear   
        Perfil.objects.get_or_create(user=instance)
        print("Se ha acabado de crear un usuario y su perfil enlazado")

"""

COUNTRIES=["Afganistán", "Akrotiri", "Albania", "Alemania", "Andorra", "Angola", "Anguila", "Antártida", "Antigua y Barbuda", "Antillas Neerlandesas", "Arabia Saudí", "Arctic Ocean", "Argelia", "Argentina", "Armenia", "Aruba", "Ashmore andCartier Islands", "Atlantic Ocean", "Australia", "Austria", "Azerbaiyán", "Bahamas", "Bahráin", "Bangladesh", "Barbados", "Bélgica", "Belice", "Benín", "Bermudas", "Bielorrusia", "Birmania Myanmar", "Bolivia", "Bosnia y Hercegovina", "Botsuana", "Brasil", "Brunéi", "Bulgaria", "Burkina Faso", "Burundi", "Bután", "Cabo Verde", "Camboya", "Camerún", "Canadá", "Chad", "Chile", "China", "Chipre", "Clipperton Island", "Colombia", "Comoras", "Congo", "Coral Sea Islands", "Corea del Norte", "Corea del Sur", "Costa de Marfil", "Costa Rica", "Croacia", "Cuba", "Dhekelia", "Dinamarca", "Dominica", "Ecuador", "Egipto", "El Salvador", "El Vaticano", "Emiratos Árabes Unidos", "Eritrea", "Eslovaquia", "Eslovenia", "España", "Estados Unidos", "Estonia", "Etiopía", "Filipinas", "Finlandia", "Fiyi", "Francia", "Gabón", "Gambia", "Gaza Strip", "Georgia", "Ghana", "Gibraltar", "Granada", "Grecia", "Groenlandia", "Guam", "Guatemala", "Guernsey", "Guinea", "Guinea Ecuatorial", "Guinea-Bissau", "Guyana", "Haití", "Honduras", "Hong Kong", "Hungría", "India", "Indian Ocean", "Indonesia", "Irán", "Iraq", "Irlanda", "Isla Bouvet", "Isla Christmas", "Isla Norfolk", "Islandia", "Islas Caimán", "Islas Cocos", "Islas Cook", "Islas Feroe", "Islas Georgia del Sur y Sandwich del Sur", "Islas Heard y McDonald", "Islas Malvinas", "Islas Marianas del Norte", "IslasMarshall", "Islas Pitcairn", "Islas Salomón", "Islas Turcas y Caicos", "Islas Vírgenes Americanas", "Islas Vírgenes Británicas", "Israel", "Italia", "Jamaica", "Jan Mayen", "Japón", "Jersey", "Jordania", "Kazajistán", "Kenia", "Kirguizistán", "Kiribati", "Kuwait", "Laos", "Lesoto", "Letonia", "Líbano", "Liberia", "Libia", "Liechtenstein", "Lituania", "Luxemburgo", "Macao", "Macedonia", "Madagascar", "Malasia", "Malaui", "Maldivas", "Malí", "Malta", "Man, Isle of", "Marruecos", "Mauricio", "Mauritania", "Mayotte", "México", "Micronesia", "Moldavia", "Mónaco", "Mongolia", "Montserrat", "Mozambique", "Namibia", "Nauru", "Navassa Island", "Nepal", "Nicaragua", "Níger", "Nigeria", "Niue", "Noruega", "Nueva Caledonia", "Nueva Zelanda", "Omán", "Pacific Ocean", "Países Bajos", "Pakistán", "Palaos", "Panamá", "Papúa-Nueva Guinea", "Paracel Islands", "Paraguay", "Perú", "Polinesia Francesa", "Polonia", "Portugal", "Puerto Rico", "Qatar", "Reino Unido", "República Centroafricana", "República Checa", "República Democrática del Congo", "República Dominicana", "Ruanda", "Rumania", "Rusia", "Sáhara Occidental", "Samoa", "Samoa Americana", "San Cristóbal y Nieves", "San Marino", "San Pedro y Miquelón", "San Vicente y las Granadinas", "Santa Helena", "Santa Lucía", "Santo Tomé y Príncipe", "Senegal", "Seychelles", "Sierra Leona", "Singapur", "Siria", "Somalia", "Southern Ocean", "Spratly Islands", "Sri Lanka", "Suazilandia", "Sudáfrica", "Sudán", "Suecia", "Suiza", "Surinam", "Svalbard y Jan Mayen", "Tailandia", "Taiwán", "Tanzania", "Tayikistán", "TerritorioBritánicodel Océano Indico", "Territorios Australes Franceses", "Timor Oriental", "Togo", "Tokelau", "Tonga", "Trinidad y Tobago", "Túnez", "Turkmenistán", "Turquía", "Tuvalu", "Ucrania", "Uganda", "Unión Europea", "Uruguay", "Uzbekistán", "Vanuatu", "Venezuela", "Vietnam", "Wake Island", "Wallis y Futuna", "West Bank", "World", "Yemen", "Yibuti", "Zambia", "Zimbabue"]  

PAISES=[[x,x] for x in COUNTRIES]

GENEROS= (
    ('Masculino','Masculino'),
    ('Femenino', 'Femenino'),
    ('Otros', 'Otros'),
    )

years=[i for i in range(1930,2010)]


months= {
    1: ('Enero'), 2: ('Febrero'), 3: ('Marzo'), 4: ('Abril'), 5: ('Mayo'), 6: ('Junio'),
    7: ('Julio'), 8: ('Agosto'), 9: ('Septiembre'), 10: ('Octubre'), 11: ('Noviembre'),
    12: ('Diciembre')
}

class Registrarse (models.Model):
    #DNI = models.CharField(primary_key=True, max_length=20)
    nombres =models.CharField(verbose_name= "Nombres", max_length=30, blank= False, null=False)
    apellidos = models.CharField(verbose_name= "Apellidos", default='',max_length=30, blank= False, null=False)
    pais = models.CharField(verbose_name="Pais",default='',null= False, blank= False, max_length=30, choices=PAISES) #campo opcional
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento",null= True, blank= True) #campo opcional
    email = models.EmailField(verbose_name="Email",default='',null= False, blank= False, unique=True) #campo opcional
    genero = models.CharField(verbose_name="Genero",default='',null= True, blank= True, max_length=10, choices=GENEROS) #campo opcional
    contraseña = models.CharField(verbose_name="Contraseña",default='',null= False, blank= False, max_length=50) #campo opcional
    id_restablecimiento = models.CharField(verbose_name="Id Recuperacion", default='', null=True, blank=True, max_length=60)
    activacion = models.BooleanField(verbose_name="activacion",default=False, null= False, blank= False) #campo opcional


    def activate(self):
        return self.activacion

    class Meta:
        verbose_name = 'Egresado'
        verbose_name_plural= 'Egresados'
        #ordering = ['order','title']

    def __str__(self):
        return self.nombres

        """