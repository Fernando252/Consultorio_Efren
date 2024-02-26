from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Abogado, Casos, Clientes,Cita, Documentos,Info_Abogado
from .forms import CitaForm, DocumentoForm, RegistroClienteForm, AbogadoForm,CasosForm,ADocumentoForm
from django.urls import reverse
from .utils import *
from django.contrib import messages




#Views Clientes

#________________________________________________________________________________________________
#casos
@login_required
def cliente_por_abogado(request):
    abogado_actual = request.user.abogado

    casos_abogado = Casos.objects.filter(abogado=abogado_actual)

 
    clientes_con_casos = set([caso.cliente for caso in casos_abogado])

    return render(request, 'lista_clientes.html', {'clientes_con_casos': clientes_con_casos})

@login_required
def abogados_por_cliente(request):
    cliente_actual = request.user.cliente

    casos_cliente = Casos.objects.filter(cliente=cliente_actual)

    abogados_con_casos = set([caso.abogado for caso in casos_cliente])

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

   
    casos_cliente = Casos.objects.filter(cliente=cliente_actual)

    abogados_con_casos = set([caso.abogado for caso in casos_cliente])

    return render(request, 'lista_abogados.html', {'abogados_con_casos': abogados_con_casos})

@login_required
def ver_casos_abogado(request,codigo_abogado):
    abogado = get_object_or_404(Abogado, pk=codigo_abogado)

    cliente_logueado = get_object_or_404(Clientes, user=request.user)

    casos_abogado = Casos.objects.filter(abogado=abogado, cliente=cliente_logueado)

    contenido = {
        'casos_abogado': casos_abogado,
        'abogado': abogado,
    }
    template = "caso.html"  
    return render(request, template, contenido)
#______________________________________________________________________________
#Documentos 
def ver_documentos(request):
    # Intentar obtener el cliente logueado
    try:
        cliente_logueado = request.user.cliente
    except AttributeError:

        return redirect('dashboard')  

    documentos = Documentos.objects.filter(caso__cliente=cliente_logueado)

    contenido = {
        'documentos': documentos,
    }
    return render(request, 'lista_documentos.html', contenido)
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

def subir_documento(request):
    cliente_logueado = request.user.cliente

    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        form.fields['caso'].queryset = Casos.objects.filter(cliente=cliente_logueado)

        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = DocumentoForm()
        form.fields['caso'].queryset = Casos.objects.filter(cliente=cliente_logueado)

    return render(request, 'subir_documento.html', {'form': form})
#______________________________________________________________________________


#perfil
@login_required
def ver_cliente_usuario(request):
    
    if hasattr(request.user, 'abogado'):

        url = reverse('ver_abogado')
        return redirect(url)
    
    try:
        cliente = request.user.cliente
    except Clientes.DoesNotExist:
        cliente = None

    if request.method == 'POST':
 
        form = RegistroClienteForm(request.POST, instance=cliente)
        if form.is_valid():
        
            cliente = form.save(commit=False)
            cliente.user = request.user
            cliente.save()
            return redirect('dashboard')  
    else:
        if cliente is not None:
            return redirect('dashboard')
     
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


#abogados 
#Ver abogado 
def ver_abogado(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'abogado'):
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para ver este perfil'})

    abogado = request.user.abogado

    if request.method == 'POST':
        form = AbogadoForm(request.POST, request.FILES, instance=abogado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información actualizada exitosamente.')
            return redirect('ver_abogado')
        else:
            messages.error(request, 'Error al actualizar la información. Por favor, revisa los campos.')
    else:
        form = AbogadoForm(instance=abogado)

    contenido = {
        'abogado': abogado,
        'form': form,
    }
    return render(request, 'abogado_detalle.html', contenido)


#Editar abogado 
def editar_abogado(request, codigo_abogado):
    abogado = get_object_or_404(Abogado, pk=codigo_abogado)

    if request.method == 'POST':
        form = AbogadoForm(request.POST, instance=abogado)
        if form.is_valid():
            form.save()
            return redirect('ver_abogado')
        else:
            return render(request, 'editar_abogado.html', {'form': form, 'abogado': abogado})
    else:
        form = AbogadoForm(instance=abogado)
        return render(request, 'abogado_editar.html', {'form': form, 'abogado': abogado})
    
#______________________________________________________________________________
    
#Documento_abogados 
def abogado_subir_documento(request):

    if not hasattr(request.user, 'abogado'):
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para acceder a esta página'})
    
    abogado = request.user.abogado
    
    if request.method == 'POST':
        form = ADocumentoForm(abogado, request.POST, request.FILES)
        
        if form.is_valid():
            documento = form.save(commit=False)
            documento.save()
            return redirect('dashboard')
    else:
        form = ADocumentoForm(abogado)
    
    return render(request, 'abogado_subir_documento.html', {'form': form})


#Ver Documento_abogados 
def abogado_ver_documentos(request):
    if not hasattr(request.user, 'abogado'):
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para acceder a esta página'})

    abogado_logueado = request.user.abogado

    clientes_con_documentos = Clientes.objects.filter(casos__abogado=abogado_logueado, casos__documentos__isnull=False).distinct()

    contenido = {
        'clientes_con_documentos': clientes_con_documentos,
    }
    template = "abogado_lista_doc.html"
    return render(request, template, contenido)

#Ver los casos que tiene el cliente
def abogado_ver_casos_cliente(request, cliente_id):
    abogado_logueado = request.user.abogado

    cliente_seleccionado = get_object_or_404(Clientes, id=cliente_id)


    casos_cliente_abogado = Casos.objects.filter(cliente=cliente_seleccionado, abogado=abogado_logueado)

    contenido = {
        'cliente': cliente_seleccionado,
        'casos_cliente_abogado': casos_cliente_abogado,
    }
    template = "abogado_ver_casos_cliente.html"
    return render(request, template, contenido)

#Ver casos_Documento_abogados 
def ver_documentos_caso(request, caso_id):
    abogado_logueado = request.user.abogado


    caso_seleccionado = get_object_or_404(Casos, id=caso_id, abogado=abogado_logueado)
    documentos_caso = Documentos.objects.filter(caso=caso_seleccionado)

    contenido = {
        'caso': caso_seleccionado,
        'documentos_caso': documentos_caso,
    }
    template = "abogado_ver_doc_caso.html"
    return render(request, template, contenido)

#Editar documentos abogados

def editar_documento_abogado(request, codigo_documento):
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
    return render(request,'abogado_editar_documento.html', c)
    

    
@login_required
def eliminar_documento_abogado(request, codigo_documento):
    abogado_logueado = request.user.abogado

    # Obtener el documento a eliminar
    documento_a_eliminar = get_object_or_404(Documentos, id=codigo_documento, caso__abogado=abogado_logueado)

    # Eliminar el documento
    documento_a_eliminar.delete()

    # Redirigir a la vista 'subir_documento' u otra vista adecuada
    return redirect('dashboard')


#casos
#______________________________________
#Vista de casos por cliente
def clientes_con_casos(request):
    abogado_logueado = request.user.abogado

    clientes_con_casos = Clientes.objects.filter(casos__abogado=abogado_logueado).distinct()

    contenido = {
        'clientes_con_casos': clientes_con_casos,
    }
    template = "abogado_lista_casos.html"
    return render(request, template, contenido)

#Registrar Casos 
def registrar_caso(request):
    if request.method == 'POST':
        form = CasosForm(request.POST)
        if form.is_valid():
            caso = form.save(commit=False)
            caso.abogado = request.user.abogado  
            caso.save()
            return redirect('dashboard')  
    else:
        form = CasosForm()

    return render(request, 'abogado_registrar_caso.html', {'form': form})

#Registrar Casos 

def ver_casos_cliente(request, cliente_id):
    abogado_logueado = request.user.abogado

  
    cliente_seleccionado = get_object_or_404(Clientes, id=cliente_id)

    casos_cliente_abogado = Casos.objects.filter(cliente=cliente_seleccionado, abogado=abogado_logueado)

    contenido = {
        'cliente': cliente_seleccionado,
        'casos_cliente_abogado': casos_cliente_abogado,
    }
    template = "abogado_casos_cliente.html"
    return render(request, template, contenido)

#Ver un solo caso de abogado por cliente
def abogado_ver_caso(request, codigo_caso):
   c = {}
   c['caso'] =  get_object_or_404(Casos, pk=codigo_caso)
   return render(request, 'abogado_ver_casoC.html', c)

#Abogado editar caso-cliente
def editar_caso_abogado(request, codigo_caso):
    caso = get_object_or_404(Casos, pk=codigo_caso)

    if request.method == 'POST':
        form = CasosForm(request.POST, instance=caso)
        if form.is_valid():
            form.save()
             # Utiliza reverse para obtener la URL de 'ver_cita' con el nuevo ID de la cita
            url_ver_caso = reverse('abogado_ver_caso', kwargs={'codigo_caso': caso.pk})
            return redirect(url_ver_caso)
        else:
            return render(request, 'Abogado_editar_caso.html', {'form': form, 'caso': caso})
    else:
        form = CasosForm(instance=caso)
        return render(request, 'Abogado_editar_caso.html', {'form': form, 'caso': caso})
    
    
@login_required
def eliminar_caso(request, codigo_caso):
    abogado_logueado = request.user.abogado

    # Obtener el caso a eliminar
    caso_a_eliminar = get_object_or_404(Casos, id=codigo_caso, abogado=abogado_logueado)

    # Eliminar el caso
    caso_a_eliminar.delete()
    return redirect('clientes_con_casos')

#__________________________________________________________________________________________
#citas_Abogado
#______________________________________
def registrar_horario(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.abogado = request.user
            cita.save()
            return redirect('ver_horarios')  # Reemplaza 'ver_horarios' con el nombre de la vista para ver horarios
    else:
        form = CitaForm()

    return render(request, 'registrar_horario.html', {'form': form})