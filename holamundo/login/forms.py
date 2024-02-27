from django import forms
from bootstrap_datepicker_plus.widgets import DateTimePickerInput,DatePickerInput
from httpcore import request
from .models import Cita, Documentos, Clientes, Abogado, Casos,Horario_atencion,Cita1


class RegistroClienteForm(forms.ModelForm):
   class Meta:
        model = Clientes
        fields = ['cedula', 'nombrec', 'apellido', 'direccion', 'celular', 'correo', ]
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'nombrec': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.TextInput(attrs={'class': 'form-control'}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['correo'].widget.attrs['readonly'] = True 



class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['abogado', 'fecha_cita', 'lugar_cita', 'descripcion']
        widgets = {
            'abogado': forms.Select(attrs={'class': 'form-control'}),
            'fecha_cita': DateTimePickerInput(attrs={'class': 'form-control datetimepicker-input'}),
            'lugar_cita': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }
        def __init__(self, *args, **kwargs):
            super(CitaForm, self).__init__(*args, **kwargs)
            self.fields['abogado'].queryset = Abogado.objects.all()


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documentos
        fields = ['caso', 'tipo_documento', 'descripcion_documento', 'archivo_adjunto',]
        widgets = {
            'caso': forms.Select(attrs={'class': 'form-control'}),
            'tipo_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_documento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'archivo_adjunto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ADocumentoForm(forms.ModelForm):
    class Meta:
        model = Documentos
        fields = ['caso', 'tipo_documento', 'descripcion_documento', 'archivo_adjunto',]
        widgets = {
            'caso': forms.Select(attrs={'class': 'form-control'}),
            'tipo_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_documento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'archivo_adjunto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, abogado, *args, **kwargs):
        super(ADocumentoForm, self).__init__(*args, **kwargs)

        # Filtrar los casos relacionados con el abogado logueado
        self.fields['caso'].queryset = abogado.casos.all()



class AbogadoForm(forms.ModelForm):
    class Meta:
        model = Abogado
        fields = ['nombrea', 'apellido', 'celular', 'correo', 'experiencia','facebook', 'instagram', 'twitter', 'descripcion', 'tipos_especialidad', 'foto']
    widgets = {   
        'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
    }
    

class CasosForm(forms.ModelForm):
    class Meta:
        model=Casos
        fields= ['cliente','nombre','tipos_casos','Estado','descripcion']
        widgets = {
        
        'cliente':forms.Select(attrs={'class': 'form-control'}),
        'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        'tipos_casos': forms.Select(attrs={'class': 'form-control'}),
        'Estado':forms.Select(attrs={'class': 'form-control'}),
        'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }
        
class HorarioAtencionForm(forms.ModelForm):
    class Meta:
        model = Horario_atencion
        fields = ['fecha', 'hora']
        widgets = {
 
            'fecha': DatePickerInput(attrs={'class': 'form-control datepicker-input'}),

        }

    def __init__(self, *args, **kwargs):
        super(HorarioAtencionForm, self).__init__(*args, **kwargs)



class AgendarCitaForm(forms.ModelForm):
    class Meta:
        model = Cita1
        fields = ['horario_atencion']

    def __init__(self, *args, abogado_id=None, **kwargs):
        super(AgendarCitaForm, self).__init__(*args, **kwargs)
        self.abogado_id = abogado_id
        self.filtrar_horarios()

    def filtrar_horarios(self):
        if self.abogado_id is not None:
            # Filtrar horarios disponibles basados en el abogado y si ya están seleccionados
            horarios_elegidos = Cita1.objects.filter(abogado__id=self.abogado_id).values_list('horario_atencion_id', flat=True)
            self.fields['horario_atencion'].queryset = Horario_atencion.objects.filter(abogado_id=self.abogado_id).exclude(id__in=horarios_elegidos)


            