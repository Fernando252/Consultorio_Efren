from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Abogado, Casos, Clientes,Cita, Documentos,Info_Abogado
from .forms import CitaForm, DocumentoForm, RegistroClienteForm, AbogadoForm,CasosForm
from django.urls import reverse
from .utils import *
from django.contrib import messages


def editar_abogado(request, codigo_abogado):
    c = {}
    abogado = get_object_or_404(Abogado, pk=codigo_abogado)
    if request.method == 'POST':
        form = AbogadoForm(request.POST, request.FILES, instance=abogado)
        if form.is_valid():
            form.save()
            return redirect(abogado.get_absolute_url())
    else:
        form = CitaForm(instance=abogado)
    c['form'] = form
    c['abogado']= abogado
    return render(request,'formulario_abogado.html', c)
from django.http import HttpResponse
from .utils import extraer_clientes

#Views Clientes



def registro_abogado(request):
    ESPECIALIDAD_CHOICES = Abogado.ESPECIALIDAD_CHOICES
    if request.method == 'POST':
        cedula = request.POST['cedula']
        nombrea = request.POST['nombrea']
        apellido = request.POST['apellido']
        celular = request.POST['celular']
        correo = request.POST['correo']
        tipos_especialidad = request.POST['tipos_especialidad']


        # Crear una instancia de Abogado y guardarla en la base de datos
        abogado = Abogado.objects.create(
            cedula=cedula,
            nombrea=nombrea,
            apellido=apellido,
            celular=celular,
            correo=correo,
            tipos_especialidad=tipos_especialidad,
    
        )
        
        # Realizar cualquier otra acción o redirigir a una página específica
        return redirect('dashboard.html')  
    return render(request, 'registro_abogado.html', {'ESPECIALIDAD_CHOICES': ESPECIALIDAD_CHOICES})

# registo cliente
def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.save()
            return redirect('dashboard')  # Cambia 'login_cliente.html' con la URL correcta
    else:
        form = RegistroClienteForm()

    return render(request, 'registro_cliente.html', {'form': form})


#casos

@login_required
def abogados_por_cliente(request):
    cliente_actual = request.user.cliente

    # Obtener los casos para el cliente actual
    casos_cliente = Casos.objects.filter(cliente=cliente_actual)

    # Obtener la lista única de abogados asociados a esos casos
    abogados_con_casos = set([caso.abogado for caso in casos_cliente])

    # Renderizar la plantilla con la lista de abogados
    return render(request, 'lista_abogados.html', {'abogados_con_casos': abogados_con_casos})

@login_required
def ver_casos_abogado(request,codigo_abogado):
    
    if not es_abogado(request.user):
        messages.error(request, 'Acceso no permitido a panel de abogado')
        return HttpResponse('Acceso no permitido')
    
    abogado = get_object_or_404(Abogado, pk=codigo_abogado)

    # Asegúrate de tener la relación correcta entre User, Clientes, y Abogado
  
    # Filtra los casos por el cliente logueado
    casos_abogado = Casos.objects.filter(abogado=abogado)

    contenido = {
        'casos_abogado': casos_abogado,
        'abogado': abogado,
    }
    template = "caso.html"  # Asegúrate de que la plantilla tenga el formato correcto
    return render(request, template, contenido)

@login_required
def registrar_caso(request):
    if request.method == 'POST':
        form = CasosForm(request.POST)
        if form.is_valid():
            # Asigna el abogadp asociado al usuario actual
            caso = form.save(commit=False)
            caso.abogado = request.user.abogado  # Ajusta según tu lógica de relación con el abogado
            caso.save()
            return redirect('dashboard')  # Redirige a la página de inicio o donde desees
    else:
        form = CasosForm()

    return render(request, 'registrar_caso.html', {'form': form})

 # Citas
# Citas
#________________________________________________________________________________________
@login_required
def registrar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            # Asigna el cliente asociado al usuario actual
            cita = form.save(commit=False)
            cita.cliente = request.user.cliente 
            cita.save()
            return redirect('dashboard')  
    else:
        form = CitaForm()

    return render(request, 'registrar_cita1.html', {'form': form})

#________________________________________________________________________________________

@login_required
def citas_t(request):
    cliente_actual = request.user.cliente  # Accede al cliente del usuario
    citas_cliente = Cita.objects.filter(cliente=cliente_actual)
    return render(request, 'cita_general.html', {'citas_cliente': citas_cliente})
#________________________________________________________________________________________

@login_required
def citas_clientes(request,codigo_cliente):
    cliente = Clientes.objects.get(pk=codigo_cliente)
    citas_cliente = Cita.objects.filter(cliente=cliente)
    contenido = {
        'citas_cliente': citas_cliente,
        'cliente': cliente,
    }
    template = "cita_cliente.html"
    return render(request, template, contenido)
#________________________________________________________________________________________

@login_required
def eliminar_cita(request, codigo_cita):
    cita = get_object_or_404(Cita, id=codigo_cita)

    if request.method == 'POST':
        cita.delete()
        return redirect('lista_citas')  
    return render(request, 'ver_cita.html', {'cita': cita})

def ver_cita(request, codigo_cita):
   c = {}
   c['cita'] =  get_object_or_404(Cita, pk=codigo_cita)
   return render(request, 'ver_cita.html', c)

#________________________________________________________________________________________

@login_required
def editar_cita(request, codigo_cita):
    cita = get_object_or_404(Cita, pk=codigo_cita)

    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            # Utiliza reverse para obtener la URL de 'ver_cita' con el nuevo ID de la cita
            url_ver_cita = reverse('ver_cita', kwargs={'codigo_cita': cita.pk})
            return redirect(url_ver_cita)
    else:
        form = CitaForm(instance=cita)

    return render(request, 'editar_cita.html', {'form': form, 'cita': cita})
#________________________________________________________________________________________


#calendario de citas

class CitaListView(ListView):
    model = Cita
    template_name = 'cita_list.html'

#______________________________________________________________________________


#Casos

@login_required
def abogados_por_cliente(request):
    cliente_actual = request.user.cliente

    # Obtener los casos para el cliente actual
    casos_cliente = Casos.objects.filter(cliente=cliente_actual)

    # Obtener la lista única de abogados asociados a esos casos
    abogados_con_casos = set([caso.abogado for caso in casos_cliente])

    # Renderizar la plantilla con la lista de abogados
    return render(request, 'lista_abogados.html', {'abogados_con_casos': abogados_con_casos})

@login_required
def ver_casos_abogado(request,codigo_abogado):
    abogado = get_object_or_404(Abogado, pk=codigo_abogado)

    # Asegúrate de tener la relación correcta entre User, Clientes, y Abogado
    cliente_logueado = get_object_or_404(Clientes, user=request.user)

    # Filtra los casos por el cliente logueado
    casos_abogado = Casos.objects.filter(abogado=abogado, cliente=cliente_logueado)

    contenido = {
        'casos_abogado': casos_abogado,
        'abogado': abogado,
    }
    template = "caso.html"  # Asegúrate de que la plantilla tenga el formato correcto
    return render(request, template, contenido)
#______________________________________________________________________________


#Documentos 
def ver_documentos(request):
    cliente_logueado = Clientes.objects.get(user=request.user)

    # Filtrar los documentos por el cliente logueado
    documentos = Documentos.objects.filter(caso__cliente=cliente_logueado)

    contenido = {
        'documentos': documentos,
    }
    template = "lista_documentos.html"
    return render(request, template, contenido)

#______________________________________________________________________________

def ver_documento(request, codigo_documento):
   c = {}
   c['documento'] =  get_object_or_404(Documentos, pk=codigo_documento)
   return render(request, 'ver_documento.html', c)
#______________________________________________________________________________


def editar_documento(request, codigo_documento):
    c = {}
    documento = get_object_or_404(Documentos, pk=codigo_documento)
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.save()
            return redirect(documento.get_absolute_url())
    else:
        form = DocumentoForm(instance=documento)
    c['form'] = form
    c['documento']= documento
    return render(request,'edit_documento.html', c)
#______________________________________________________________________________


def eliminar_documento(request, codigo_documento):
    documento = get_object_or_404(Documentos, id=codigo_documento)

    if request.method == 'POST':
        documento.delete()
        return redirect('lista_documentos')  
    return render(request, 'ver_documento.html', {'documento': documento})

#______________________________________________________________________________

@login_required
def subir_documento(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = DocumentoForm()

    return render(request, 'subir_documento.html', {'form': form})
#______________________________________________________________________________


#perfil
@login_required
def ver_cliente_usuario(request):
    
    if hasattr(request.user, 'abogado'):
        #return redirect('detalle_casos', request.user.abogado.id)
    
        url = reverse('detalle_casos', kwargs={'codigo_abogado': request.user.abogado.pk})
        return redirect(url)
    
    try:
        cliente = request.user.cliente
    except Clientes.DoesNotExist:
        cliente = None

    if request.method == 'POST':
        # Si es una solicitud POST, procesar el formulario
        form = RegistroClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            # Guardar los datos actualizados del formulario
            cliente = form.save(commit=False)
            cliente.user = request.user
            cliente.save()
            return redirect('dashboard')  # Redirigir a una página exitosa
    else:
        if cliente is not None:
            # Si el cliente ya ha completado el cliente, redirigir al dashboard
            return redirect('dashboard')
        # Si es una solicitud GET, mostrar el formulario
        initial_data = {'correo': request.user.email} if cliente is None else None
        form = RegistroClienteForm(instance=cliente, initial=initial_data)

    return render(request, 'perfil_usuario.html', {'form': form})
#______________________________________________________________________________

#Abogado cliente
def ver_abogados(request):
    abogados = Abogado.objects.all()
    contenido = {
        'abogados' : abogados
    }
    template = "p_abogado.html"
    return render(request, template, contenido)

def detalle_abogado(request, codigo_abogado):
    abogado = get_object_or_404(Abogado, pk=codigo_abogado)
    detalle_abogado = Info_Abogado.objects.filter(abogado=abogado)
    contenido = {
        'detalle' : detalle_abogado, 
        'abogado' : abogado,
    }
    return render(request, 'detalle_abogado.html', contenido)

def clientesviews(request):
    extraer_clientes()
    return HttpResponse('Importado')
#______________________________________________________________________________

#Abogado cliente
