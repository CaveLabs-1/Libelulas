from django.shortcuts import render, get_object_or_404
from .forms import UserForm, UpdatePasswordForm, UpdateUserForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import User
from coaches.models import PreRegistro
import uuid
from django.core.mail import send_mail

def lista_administrador(request):
    lista = User.objects.all()
    return render(request, 'lista_administrador.html', {'lista': lista})

def agregar_administrador(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            informacion = form.save(commit=False)
            administrador = User()
            administrador.first_name = informacion.first_name
            administrador.username = informacion.username
            administrador.email = informacion.email
            administrador.set_password('temporal')
            administrador.save()
            messages.success(request, 'Administrador agregado exitosamente')
            return HttpResponseRedirect(reverse('administrador:confirmar_contrasena', kwargs={'id_administrador':administrador.id}))
    else:
        form = UserForm()
    return render(request, 'agregar_administrador.html', {'form': form})

def confirmar_contrasena(request, id_administrador):
    administrador = get_object_or_404(User, id=id_administrador)
    if request.method == "POST":
        form = UpdatePasswordForm(data=request.POST, instance=request.user)
        if form.is_valid():
            actualizar = form.save(commit=False)
            administrador.set_password(actualizar.password)
            administrador.save()
            messages.success(request, 'Contraseña actualizada exitosamente.')
            url = reverse('administrador:editar_administrador', kwargs={'id_administrador':id_administrador})
            return HttpResponseRedirect(url)
    else:
        form = UpdatePasswordForm()
    return render(request, 'confirmar_contrasena.html', {'form': form, 'administrador': administrador})

def editar_administrador(request, id_administrador):
    administrador = get_object_or_404(User, id=id_administrador)
    if request.method == "POST":
        form = UpdateUserForm(data=request.POST, instance=administrador)
        if form.is_valid():
            actualizar = form.save(commit=False)
            administrador.first_name = actualizar.first_name
            administrador.email = actualizar.email
            administrador.save()
            messages.success(request, 'Administrador editado exitosamente')
            url = reverse('administrador:editar_administrador', kwargs={'id_administrador':id_administrador})
            return HttpResponseRedirect(url)
    else:
        form = UpdateUserForm(instance=administrador)
    return render(request, 'editar_administrador.html', {'form': form, 'administrador': administrador})

def eliminar_administrador(request, id_administrador):
    administrador = get_object_or_404(User, id=id_administrador)
    administrador.delete()
    messages.warning(request, 'Administrador eliminado exitosamente.')
    return HttpResponseRedirect(reverse('administrador:lista_administrador'))


def eliminar_preregsitro(request, id_preregistro):
    pre = get_object_or_404(PreRegistro, id=id_preregistro)
    pre.delete()
    messages.warning(request, 'Pre-registro eliminado exitosamente.')
    return HttpResponseRedirect(reverse('administrador:lista_PreRegistro'))

def lista_PreRegistro(request):
    PreResgistros = PreRegistro.objects.all()
    return render(request, 'lista_preRegistro.html', {'PreRegistros': PreResgistros})

def aceptar_PreRegistro(request, id_preregistro):
    pre = get_object_or_404(PreRegistro, id=id_preregistro)
    pre.codigo = uuid.uuid4().hex[:16].upper()
    pre.save()
    liga = request.build_absolute_uri(reverse('coaches:registrar_equipo',  kwargs={'codigo': pre.codigo}))
    message = "¡Gracias por solicitar un registro en Plan Libélula! Sólo hay un paso más para poder inscribirse en un " \
              "torneo. Para activar su cuenta, haga clic en el siguiente enlace: "+liga+" Si eso no funciona, copie y pegue " \
              "el enlace en la barra de direcciones de su navegador"

    send_mail(
        'Aceptación de Pre Registro',
        message,
        'A01208598@itesm.mx',
        [pre.correo],
        fail_silently=False,
    )
    return HttpResponseRedirect(reverse('administrador:lista_PreRegistro'))




