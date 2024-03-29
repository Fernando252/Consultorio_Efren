import datetime
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Abogado, Casos, Clientes, Documentos,Info_Abogado,Horario_atencion,Cita1
from .forms import DocumentoForm,DocumentoFormEdit,RegistroClienteForm, AbogadoForm,CasosForm,ADocumentoForm,HorarioAtencionForm,AgendarCitaForm,AgendarCitaForm1
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
def ver_documentos(request, caso_id):
    cliente_logueado = request.user.cliente

    # Obtener el caso seleccionado por el cliente logueado
    caso_seleccionado = get_object_or_404(Casos, id=caso_id, cliente=cliente_logueado)

    # Obtener los documentos asociados al caso seleccionado
    documentos = Documentos.objects.filter(caso=caso_seleccionado)

    contenido = {
        'caso_seleccionado': caso_seleccionado,
        'documentos': documentos,
    }
    return render(request, 'lista_documentos.html', contenido)
#______________________________________________________________________________

def ver_documento(request, codigo_documento):
   c = {}
   c['documento'] =  get_object_or_404(Documentos, pk=codigo_documento)
   return render(request, 'ver_documento.html', c)
#__________________________________________________________________ ____________


def editar_documento(request, codigo_documento):
    c = {}
    documento = get_object_or_404(Documentos, pk=codigo_documento)
    if request.method == 'POST':
        form = DocumentoFormEdit(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.save()
            return redirect(documento.get_absolute_url())
    else:
        form = DocumentoForm(instance=documento)
    c['form'] = form
    c['documento']= documento
    return render(request,'cliente_lista_doc.html', c)
#______________________________________________________________________________

@login_required
def eliminar_documento(request, codigo_documento):
    cliente_logueado = request.user.cliente

    # Obtener el documento a eliminar
    documento_a_eliminar = get_object_or_404(Documentos, id=codigo_documento, caso__cliente=cliente_logueado)

    # Eliminar el documento
    documento_a_eliminar.delete()
    messages.warning(request, 'El objeto se ha eliminado correctamente.')
    # Redirigir a la vista 'subir_documento' u otra vista adecuada
    return redirect('dashboard')

#______________________________________________________________________________

def subir_documento(request):
    cliente_logueado = request.user.cliente

    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        form.fields['caso'].queryset = Casos.objects.filter(cliente=cliente_logueado)
        messages.success(request, '¡Bien hecho! Has realizado una acción exitosa.')
        if form.is_valid():
            form.save()
            messages.warning(request, 'El documento se ha registrado correctamente.')
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
        form = DocumentoFormEdit(request.POST, request.FILES, instance=documento)
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
    messages.warning(request, 'El objeto se ha eliminado correctamente.')
    # Redirigir a la vista 'subir_documento' u otra vista adecuada
    return redirect('dashboard')


#casos
#______________________________________
#Vista de casos por cliente
@login_required
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
            messages.success(request, 'El caso se registro correctamente.')
            return redirect('dashboard')  
    else:
        form = CasosForm()

    return render(request, 'abogado_registrar_caso.html', {'form': form})

#Registrar Casos 
@login_required
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
@login_required
def abogado_ver_caso(request, codigo_caso):
   c = {}
   c['caso'] =  get_object_or_404(Casos, pk=codigo_caso)
   return render(request, 'abogado_ver_casoC.html', c)

#Abogado editar caso-cliente
@login_required
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
    messages.warning(request, 'El objeto se ha eliminado correctamente.')
    return redirect('clientes_con_casos')

#__________________________________________________________________________________________
#citas_Abogado
#______________________________________
@login_required
def registrar_horario(request):
    if request.method == 'POST':
        form = HorarioAtencionForm(request.POST)
        if form.is_valid():
            horario_atencion = form.save(commit=False)
            horario_atencion.abogado = request.user.abogado
            horario_atencion.save()
            messages.success(request, 'Se ha registrado correctamente.')
            return redirect('dashboard')
    else:
        form = HorarioAtencionForm()

    return render(request, 'registrar_horario.html', {'form': form})


@login_required
def lista_abogados_con_horario(request):
    # Verifica que el usuario autenticado sea un cliente, no un abogado
    if request.user.is_authenticated and hasattr(request.user, 'cliente'):
        abogados_con_horario = Abogado.objects.filter(horarios_atencion__isnull=False).distinct()
        context = {'abogados_con_horario': abogados_con_horario}
        return render(request, 'lista_abogados_con_horario.html', context)
    else:
        # Si el usuario no es un cliente, puedes redirigirlo a otra página o mostrar un mensaje de error
        return render(request, 'error.html', {'mensaje': 'Acceso no autorizado'})


@login_required
def registrar_cita(request, abogado_id):
    try:
        abogado = Abogado.objects.get(pk=abogado_id)
    except Abogado.DoesNotExist:
        raise Http404("El abogado no existe")

    fecha_filtro = request.GET.get('fecha_filtro')
    form = AgendarCitaForm(abogado_id=abogado_id)

    if request.method == 'POST':
        form = AgendarCitaForm(request.POST, abogado_id=abogado_id)
        if form.is_valid():
            nueva_cita = form.save(commit=False)

            if request.user.is_authenticated and hasattr(request.user, 'cliente'):
                nueva_cita.cliente = request.user.cliente
            else:
                messages.error(request, 'Error al registrar la cita. Por favor, inicia sesión como cliente.')
                return redirect('login')

            nueva_cita.abogado = abogado

            # Manejo de errores al intentar guardar la cita
            try:
                nueva_cita.save()
                messages.success(request, 'Cita registrada exitosamente.')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Error al guardar la cita: {str(e)}')
                # Puedes redirigir a una página de error o hacer algo más según tus necesidades
                return redirect('pagina_de_error') 

    # Filtrar los horarios por fecha si se proporciona una fecha en la solicitud
    if fecha_filtro:
        form.filtrar_horarios(filtro_fecha=fecha_filtro)

    context = {'form': form, 'abogado': abogado}
    return render(request, 'agendar_cita.html', context)




@login_required
def lista_clientes_citas_abogado(request):
    if not hasattr(request.user, 'abogado'):
        return render(request, 'error.html', {'mensaje': 'El usuario actual no es un abogado'})

    abogado = request.user.abogado
    citas_abogado = Cita1.objects.filter(abogado=abogado).values('cliente_id').distinct()
    
    print("Citas abogado:", citas_abogado)  # Imprimir para depuración

    clientes_con_citas = Clientes.objects.filter(id__in=citas_abogado)

    context = {'clientes_con_citas': clientes_con_citas, 'abogado_id': abogado.id}
    return render(request, 'abogado_lista_cita_clientes.html', context)


@login_required
def citas_cliente_con_abogado(request, cliente_id):
    abogado = request.user.abogado
    cliente_seleccionado = get_object_or_404(Clientes, id=cliente_id)

    citas_cliente_con_abogado = Cita1.objects.filter(abogado=abogado, cliente=cliente_seleccionado).order_by('horario_atencion__fecha')

    context = {'citas_cliente_con_abogado': citas_cliente_con_abogado, 'cliente_seleccionado': cliente_seleccionado}
    return render(request, 'citas_cliente_con_abogado.html', context)


@login_required
def lista_fechas_horarios_abogado(request):
    abogado = request.user.abogado
    fechas_horarios = Horario_atencion.objects.filter(abogado=abogado).values_list('fecha', flat=True).distinct().order_by('fecha')

    context = {'fechas_horarios': fechas_horarios}
    return render(request, 'abogado_lista_fechas_horarios.html', context)

@login_required
def horarios_en_fecha(request, fecha):
    abogado = request.user.abogado
    horarios_en_fecha = Horario_atencion.objects.filter(abogado=abogado, fecha=fecha)

    context = {'horarios_en_fecha': horarios_en_fecha, 'fecha': fecha}
    return render(request, 'abogado_horarios_en_fecha.html', context)

#____________________________________________________________________________________
#historial de citas por el cliente

@login_required
def historial_citas_clientes(request):
    cliente = request.user.cliente
    citas_cliente = Cita1.objects.filter(cliente=cliente).values('abogado_id').distinct()
    abogados_con_citas = Abogado.objects.filter(id__in=citas_cliente)

    context = {'abogados_con_citas': abogados_con_citas, 'cliente_id': cliente.id}
    return render(request, 'historial_citas_clientes.html', context)

@login_required
def detalle_citas_cliente(request, cliente_id, abogado_id):
    cliente = request.user.cliente
    citas_cliente_abogado = Cita1.objects.filter(cliente=cliente, abogado_id=abogado_id).order_by('horario_atencion__fecha')

    context = {'citas_cliente_abogado': citas_cliente_abogado}
    return render(request, 'detalle_citas_cliente.html', context)

@login_required
def eliminar_cita(request, codigo_cita):
    cliente = request.user.cliente

    # Obtener el documento a eliminar
    cita_a_eliminar = get_object_or_404(Cita1, id=codigo_cita, cliente=cliente)

    # Eliminar el documento
    cita_a_eliminar.delete()
    messages.warning(request, 'El objeto se ha eliminado correctamente.')
    # Redirigir a la vista 'subir_documento' u otra vista adecuada
    return redirect('dashboard')

@login_required
def editar_cita(request, codigo_cita):
    cita = get_object_or_404(Cita1, id=codigo_cita)
    
    # Obtener el abogado asociado a la cita
    abogado = cita.abogado
    
    if request.method == 'POST':
        form = AgendarCitaForm1(request.POST, instance=cita, abogado_id=cita.abogado_id)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita actualizada exitosamente.')
            return redirect('dashboard')
    else:
        form = AgendarCitaForm1(instance=cita, abogado_id=cita.abogado_id)

    return render(request, 'editar_cita_cliente.html', {'form': form, 'cita': cita, 'abogado': abogado})



#___________________________________________________________________________________________
def actualizar_horario(request, horario_id):
    # Obtener el horario de atención existente
    horario = get_object_or_404(Horario_atencion, id=horario_id)
    
    if request.method == 'POST':
        # Crear un formulario con los datos del horario existente
        form = HorarioAtencionForm(request.POST, instance=horario)
        if form.is_valid():
            # Guardar los cambios en el horario de atención
            horario = form.save()
            messages.success(request, 'Se ha actualizado el horario correctamente.')
            return redirect('dashboard')
    else:
        # Crear un formulario prellenado con los datos del horario existente
        form = HorarioAtencionForm(instance=horario)

    return render(request, 'abogado_horarios_en_fecha_editar.html', {'form': form, 'horario': horario})

@login_required
def eliminar_cita_abogado(request, horario_id):
    abogado_logueado = request.user.abogado

    # Obtener el caso a eliminar
    cita_a_eliminar = get_object_or_404(Horario_atencion, id=horario_id, abogado=abogado_logueado)

    # Eliminar el cita
    cita_a_eliminar.delete()
    messages.warning(request, 'Horario elegido se ha eliminado correctamente.')
    return redirect('dashboard')
   
@login_required
def ver_cliente(request):
    cliente = request.user.cliente
    return render(request, 'ver_cliente.html', {'cliente': cliente})

@login_required
def editar_cliente(request):
    cliente = request.user.cliente
    
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('ver_cliente')  
    else:
        form = RegistroClienteForm(instance=cliente)

    return render(request, 'editar_cliente.html', {'form': form})

@login_required
def ver_casos_cliente_doc(request):
    # Obtener los casos asociados al cliente logueado
    casos_cliente = Casos.objects.filter(cliente=request.user.cliente)

    return render(request, 'ver_casos_cliente_doc.html', {'casos_cliente': casos_cliente})

def actualizar_descripcion_caso(request, caso_id):
    caso = get_object_or_404(Casos, id=caso_id)

    if request.method == 'POST':
        nueva_descripcion = request.POST.get('nueva_descripcion')

        # Agregar la nueva actualización al historial con la fecha actual
        caso.historial_actualizaciones += f'\n{timezone.now()}: {nueva_descripcion}\n'
        caso.save()

        # Actualizar la descripción en el caso original si es necesario
        caso.descripcion = nueva_descripcion
        caso.save()

        return redirect('clientes_con_casos')  # Cambia 'detalles_caso' por la URL correcta

    # Resto de la lógica para mostrar detalles del caso y formularios
    context = {'caso': caso}
    return render(request, 'actualizar_caso.html', context)

def historial_caso(request, caso_id):
    caso = get_object_or_404(Casos, id=caso_id)

    # Dividir el historial de actualizaciones en una lista
    historial_actualizaciones = [actualizacion.strip() for actualizacion in caso.historial_actualizaciones.split('\n') if actualizacion.strip()]

    # Remover líneas vacías del historial
    historial_actualizaciones = [linea for linea in historial_actualizaciones if linea]

    context = {'caso': caso, 'historial_actualizaciones': historial_actualizaciones}
    return render(request, 'historial_caso.html', context)