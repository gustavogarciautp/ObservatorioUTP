from django.shortcuts import render, get_object_or_404, redirect
from .forms import LoginForm, Recuperar1Form, Recuperar2Form, EditProfileForm, FirstLoginAdmin, ChangeEgresadoPasswordForm
from .models import Administrador, Egresado, User, SuperUser
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse, resolve 
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as loginB
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.crypto import get_random_string
from django.views.generic.edit import UpdateView
from django .urls import reverse_lazy
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash

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
                        user = authenticate(request, email=email, password=password)    
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
        if request.user.is_administrador:
            return redirect(reverse('admin_site:index')) 
        elif request.user.is_egresado:
            return redirect(reverse('principal'))
        elif request.user.is_superusuario:
            return redirect(reverse('admin:index'))


def page404(request, exception=''):
    return render(request, "app_core/404.html")

def recuperar_1(request):
    recuperar1_form = Recuperar1Form() #Hacemos la instancia del formulario
    if request.method == 'POST': #verificamos se el formulario se ha enviado por POST
        recuperar1_form = Recuperar1Form(data= request.POST) #request.POST contiene los campos que hemos rellenado en el formulario
        if recuperar1_form.is_valid():  #verifica que todos los campos esten rellenados correctamente
            email= request.POST.get('email')
            obj=Egresado.objects.filter(email=email)
            if obj.exists():
                asunto= 'Restablece tu contraseña'
                #clave= random.randint(1000,100000)
                clave=get_random_string(length=50)
                #link='http://127.0.0.1:8000/recuperar_2/'+str(clave_cifrada)

                html_content='<p>Ha recibido este correo electrónico porque ha solicitado restablecer la contraseña para su cuenta en <a href="http://observatorioutp.pythonanywhere.com">http://observatorioutp.pythonanywhere.com</a></p></br><p>Por favor vaya a la siguiente página y escoja una nueva contraseña.</p></br><a href="http://observatorioutp.pythonanywhere.com/recuperar_2/'+clave+'">Recuperar contraseña</a></br></br><p>¡Gracias por usar nuestro sitio!</p></br>El equipo de <a href="http://observatorioutp.pythonanywhere.com">Observatorio Egresados</a>'
                msg = EmailMultiAlternatives(asunto, '', to=[email])
                msg.attach_alternative(html_content, "text/html")

                user_egresado= obj[0]
                user_egresado.id_restablecimiento=clave
                user_egresado.save()

                msg.send()

                #email.send() #enviamos el mensaje
                return redirect(reverse('recuperar_1')+'?send')
            else:
                return redirect(reverse('recuperar_1')+'?nofound')


    return render(request, "app_core/recuperar_pass_1.html", {'form':recuperar1_form})


def recuperar_2(request, id_recuperacion):
    user_egresado= Egresado.objects.filter(id_restablecimiento=id_recuperacion)
    if user_egresado.exists():
        page= user_egresado[0]
        recuperar2_form = Recuperar2Form() #Hacemos la instancia del formulario
        if request.method == 'POST': #verificamos se el formulario se ha enviado por POST
            recuperar2_form = Recuperar2Form(data= request.POST) #request.POST contiene los campos que hemos rellenado en el formulario
            if recuperar2_form.is_valid():  #verifica que todos los campos esten rellenados correctamente
                password= request.POST.get('contraseña')
                confirmar_password = request.POST.get('confirmar_contraseña')
                if password==confirmar_password:
                    page.id_restablecimiento=''
                    page.set_password(password)
                    page.save()
                    return  redirect(reverse('login_')+'?recuperado')
                else:
                    return redirect(reverse('recuperar_2', kwargs={'id_recuperacion':id_recuperacion})+'?nomatch')
        return render(request, "app_core/recuperar_pass_2.html", {'form':recuperar2_form})
    else:
        return render(request, "app_core/404.html")


def first_login_admin(request, id_change):
    admin= Administrador.objects.filter(id_restablecimiento=id_change)
    if admin.exists():
        page= admin[0]
        formulario = FirstLoginAdmin()
        if request.method == 'POST':
            formulario = FirstLoginAdmin(data= request.POST)
            if formulario.is_valid():
                password_old= request.POST.get('antigua')
                new_password = request.POST.get('contraseña')
                confirmar_password = request.POST.get('confirmar_contraseña')
                if new_password == confirmar_password:
                    page.id_restablecimiento=''
                    page.set_password(new_password)
                    page.save()
                    return redirect(reverse('admin_')+'?changepassword')
                else:
                    return redirect(reverse('first_admin_login')+'?nomatch')
        return render(request, "app_core/first_admin_login.html", {'form':formulario})
    else:
        return render(request, "app_core/404.html")


def principal(request):
    if request.user.is_authenticated and request.user.is_egresado:
        return render(request, "app_core/principal.html")
    else:
        return redirect(reverse('login_'))

def home(request):
    return render(request, "app_core/index.html")

def EditUser(request):
    if request.user.is_authenticated and request.user.is_administrador:
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                #Actualizar el objeto
                user = form.save()
                return HttpResponseRedirect(reverse('admin_'))
        else:
            form = EditProfileForm(instance=request.user)
        return render(request, 'app_core/user_change.html', {'form': form})
    else:
        return redirect(reverse('login_'))

def ChangeEgresadoPassword(request):
    if request.user.is_authenticated and request.user.is_egresado:
        formulario = ChangeEgresadoPasswordForm()
        if request.method == 'POST':
            formulario = ChangeEgresadoPasswordForm(data=request.POST)
            if formulario.is_valid():
                password=request.POST.get('contraseña')
                contraseñanueva = request.POST.get('contraseñanueva')
                confirmar_contraseña = request.POST.get('confirmarcontraseña')
                success=request.user.check_password(password)
                if not success:
                    return redirect(reverse('change_egresado_password')+'?nofound')
                elif contraseñanueva!= confirmar_contraseña:
                    return redirect(reverse('change_egresado_password')+'?nomatch')
                else:
                    request.user.set_password(contraseñanueva)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    return redirect(reverse('perfil'))
        return render(request, "app_core/egresado_change_password.html", {'form':formulario})
    else:
        return redirect(reverse('login_'))

