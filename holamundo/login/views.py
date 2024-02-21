from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import Abogado, Casos, Clientes,Cita, Documentos, Info_Abogado

from .forms import CitaForm, DocumentoForm, RegistroClienteForm
from django.contrib.auth.decorators import login_required
from .models import Abogado, Casos, Clientes,Cita, Documentos,Perfil_Usuario

from .forms import CitaForm, DocumentoForm, RegistroClienteForm, Perfil_UsuarioForm
from django.views.generic import ListView
from django.http import HttpResponse
from .utils import extraer_clientes




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
            return redirect('login_cliente')  # Cambia 'login_cliente.html' con la URL correcta
    else:
        form = RegistroClienteForm()

    return render(request, 'registro_cliente.html', {'form': form})

def ver_casos(request):
    casos_por_abogado = Abogado.objects.annotate(num_casos=Count('casos'))
    contenido = {
        'casos_por_abogado': casos_por_abogado
    }
    template = "ver_casos.html"
    return render(request, template, contenido)


#casos

@login_required
def abogados_por_cliente(request):
    # Obtén el cliente logueado
    cliente_logueado = request.user.perfil.cliente

    # Filtra los casos del cliente logueado
    casos_cliente = Casos.objects.filter(cliente=cliente_logueado)

    # Obtén los abogados asociados a los casos del cliente
    abogados = Abogado.objects.filter(casos__in=casos_cliente).distinct()

    contenido = {
        'abogados': abogados,
        'cliente': cliente_logueado,
    }

    return render(request, 'lista_abogados.html', contenido)

@login_required
def ver_casos_abogado(request, codigo_abogado):
    # Recupera el abogado logueado
    abogado = get_object_or_404(Abogado, pk=codigo_abogado)

    # Asegúrate de tener la relación correcta entre User, Perfil_Usuario y Clientes
    perfil_usuario = get_object_or_404(Perfil_Usuario, user=request.user)
    cliente_logueado = perfil_usuario.cliente

    # Filtra los casos por el cliente logueado
    casos_abogado = Casos.objects.filter(abogado=abogado, cliente=cliente_logueado)

    contenido = {
        'casos_abogado': casos_abogado,
        'abogado': abogado,
    }
    template = "caso.html"
    return render(request, template, contenido)

@login_required
def registrar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            nueva_cita = form.save(commit=False)
            
            nueva_cita.save()
            return redirect('dashboard')  # Cambia 'index' con el nombre de tu vista principal
    else:
        form = CitaForm()

    abogados = Abogado.objects.all()
    clientes = Clientes.objects.all()
    return render(request, 'registrar_cita1.html', {'form': form, 'abogados': abogados, 'clientes': clientes})


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



    
    
@login_required
def citas_t(request):
    cliente_actual = request.user.perfil.cliente

    # Filtrar las citas solo para el cliente actual
    citas_cliente = Cita.objects.filter(cliente=cliente_actual)

    # Renderizar la plantilla con las citas del cliente
    return render(request, 'cita_general.html', {'citas_cliente': citas_cliente})




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

@login_required
def nueva_cita(request):
    contenido = {}
    if request.method == 'POST':
        contenido ['form'] = CitaForm(request.POST or None)
        if contenido ['form'].is_valid():
            contenido ['form'].save()
            return redirect(contenido['form'].instance.get_absolute_url())

    contenido ['instancia_cita'] = Cita()
    contenido ['form'] = CitaForm(
        request.POST or None,
        instance = contenido['instancia_cita']
    )
    template = 'registrar_cita1.html'
    return render(request, template, contenido)

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

@login_required
def editar_cita(request, codigo_cita):
    c = {}
    cita = get_object_or_404(Cita, pk=codigo_cita)
    if request.method == 'POST':
        form = CitaForm(request.POST, request.FILES, instance=cita)
        if form.is_valid():
            form.save()
            return redirect(cita.get_absolute_url())
    else:
        form = CitaForm(instance=cita)
    c['form'] = form
    c['cita']= cita
    return render(request,'registrar_cita1.html', c)

#calendario de citas

class CitaListView(ListView):
    model = Cita
    template_name = 'cita_list.html'
  
  
#Documentos 
def ver_documentos(request):
    documentos = Documentos.objects.all()
    contenido = {
        'documentos' : documentos
    }
    template = "lista_documentos.html"



    return render(request, template, contenido)

def ver_documento(request, codigo_documento):
   c = {}
   c['documento'] =  get_object_or_404(Documentos, pk=codigo_documento)
   return render(request, 'ver_documento.html', c)

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

def eliminar_documento(request, codigo_documento):
    documento = get_object_or_404(Documentos, id=codigo_documento)

    if request.method == 'POST':
        documento.delete()
        return redirect('lista_documentos')  
    return render(request, 'ver_documento.html', {'documento': documento})

def nueva_docu(request):
    contenido = {}
    if request.method == 'POST':
        contenido ['form'] = DocumentoForm(request.POST or None)
        if contenido ['form'].is_valid():
            contenido ['form'].save()
            return redirect(contenido['form'].instance.get_absolute_url())

    contenido ['instancia_documento'] = Documentos()
    contenido ['form'] = DocumentoForm(
        request.POST or None,
        instance = contenido['instancia_documento']
    )
    template = 'edit_documento.html'
    return render(request, template, contenido)



@login_required
def ver_perfil_usuario(request):
    contenido = {}
    if hasattr(request.user, 'perfil'):
        perfil = request.user.perfil
    else:
        perfil = Perfil_Usuario(user = request.user)
    if request.method == 'POST':
        form = Perfil_UsuarioForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
        
    else:
        form = Perfil_UsuarioForm(instance=perfil)
    contenido['form'] = form
    contenido['cliente'] = perfil

    return render(request, 'perfil_usuario.html',contenido)

#Abogados 



#Abogado perfil
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
