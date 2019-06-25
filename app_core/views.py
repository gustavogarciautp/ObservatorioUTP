from django.shortcuts import render, get_object_or_404, redirect
from .forms import LoginForm, Recuperar1Form, Recuperar2Form
import hashlib
from .models import Administrador, Egresado, User, SuperUser
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse, resolve 
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as loginB
from django.shortcuts import HttpResponseRedirect

# Create your views here.
def login(request):
    #print(request.user.is_authenticated)
    current_url= resolve(request.path_info).url_name

    if not request.user.is_authenticated:
        login_form = LoginForm() 
        if request.method == 'POST': 
            login_form = LoginForm(data= request.POST) 
            if login_form.is_valid():  
                email= request.POST.get('email')
                password=request.POST.get('contraseña')
                #current_url= resolve(request.path_info).url_name
                try:
                    if current_url=='login_':
                        password_cifrada= hashlib.sha1(password.encode()).hexdigest()
                        user = authenticate(request, email=email, password=password_cifrada)    
                        if user:
                            if not user.activate():
                                return redirect(reverse('login_')+'?fail') 
                            else:
                                loginB(request, user, 'app_core.backends.EgresadoBackend')
                                return redirect(reverse('principal'))
                        else:
                            return redirect(reverse('login_')+'?nofound')
                    elif current_url=='admin_':
                        user = authenticate(request, email=email, password=password)
                        loginB(request, user, 'app_core.backends.AdminBackend')
                        return redirect(reverse('admin_site:index')) 
                    elif current_url=='super':
                        user = authenticate(request, email=email, password=password)
                        loginB(request, user, 'app_core.backends.SuperUserBackend')       
                        return redirect(reverse('admin:index'))              
                except:
                    if current_url=='login_':
                        return redirect(reverse('login_')+'?nofound')
                    elif current_url=='admin_':
                        return redirect(reverse('admin_')+'?nofound')
                    elif current_url=='super':
                        return redirect(reverse('super')+'?nofound')
        return render(request, "app_core/login.html", {'form':login_form, 'url':current_url})
    else:
        if current_url=='admin_' and request.user.is_administrador:
            return redirect(reverse('admin_site:index')) 
        if current_url=='login_' and request.user.is_egresado:
            return redirect(reverse('principal'))
        if current_url=='super' and request.user.is_superusuario:
            return redirect(reverse('admin:index'))
        return redirect(reverse('404'))


def page404(request):
    return render(request, "app_core/404.html")


def recuperar_1(request):
    recuperar1_form = Recuperar1Form() #Hacemos la instancia del formulario
    if request.method == 'POST': #verificamos se el formulario se ha enviado por POST
        recuperar1_form = Recuperar1Form(data= request.POST) #request.POST contiene los campos que hemos rellenado en el formulario
        if recuperar1_form.is_valid():  #verifica que todos los campos esten rellenados correctamente
            email= request.POST.get('email')
            obj=Egresado.objects.filter(email=email)
            if obj:
                asunto= 'Restablece tu password'
                #clave= random.randint(1000,100000)
                clave_cifrada= hashlib.sha1(str(obj.id).encode()).hexdigest()
                link='http://127.0.0.1:8000/recuperar_2/'+str(clave_cifrada)

                html_content='<p>Ha recibido este correo electrónico porque ha solicitado restablecer la password para su cuenta en <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a></p></br><p>Por favor vaya a la pagina siguiente y escoja una nueva password.</p></br><a href="http://127.0.0.1:8000/recuperar_2/'+str(clave_cifrada)+'">Recuperar password</a></br><p>Su nombre de usuario en caso de haberlo olvidado.</p></br><p>¡Gracias por usar nuestro sitio!</p></br>El equipo de <a href=" http://127.0.0.1:8000">Observatorio Egresados</a>'
                msg = EmailMultiAlternatives(asunto, content, to=[email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                #email.send() #enviamos el mensaje

                obj.id_restablecimiento=clave_cifrada
                obj.save()
            else:
                return redirect(reverse('recuperar_1')+'?nofound')


    return render(request, "app_core/recuperar_pass_1.html", {'form':recuperar1_form})


def recuperar_2(request, id_recuperacion):
    page= get_object_or_404(Egresado, id_restablecimiento=id_recuperacion)
    id_recuperacion=''
    recuperar2_form = Recuperar2Form() #Hacemos la instancia del formulario
    if request.method == 'POST': #verificamos se el formulario se ha enviado por POST
        recuperar2_form = Recuperar2Form(data= request.POST) #request.POST contiene los campos que hemos rellenado en el formulario
        if recuperar2_form.is_valid():  #verifica que todos los campos esten rellenados correctamente
            password= request.POST.get('password')
            confirmar_password = request.POST.get('confirmar_password')
            if password==confirmar_password:
                page.id_restablecimiento=''
                page.password= hashlib.sha1(password.encode()).hexdigest()
                page.save()
            else:
                return redirect(reverse('recuperar_2')+'?nomatch')


    return render(request, "app_core/recuperar_pass_2.html", {'form':recuperar2_form})


def principal(request):
    if request.user.is_authenticated and request.user.is_egresado:
        return render(request, "app_core/principal.html")
    else:
        return render(request, "app_core/404.html")

def home(request):
    return render(request, "app_core/index.html")