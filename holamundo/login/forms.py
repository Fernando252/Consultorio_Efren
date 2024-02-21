from django import forms
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from .models import Cita, Documentos, Clientes, Perfil_Usuario, Abogado

class RegistroClienteForm(forms.ModelForm):
   contraseña = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
   class Meta:
        model = Clientes
        fields = ['cedula', 'nombrec', 'apellido', 'direccion', 'celular', 'correo']
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'nombrec': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['abogado', 'cliente', 'fecha_cita', 'lugar_cita', 'descripcion']
        widgets = {
            'abogado': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'fecha_cita': DateTimePickerInput(attrs={'class': 'form-control datetimepicker-input'}),
            'lugar_cita': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Obtén el usuario logueado desde los argumentos del formulario
        user = kwargs.pop('user', None)
        super(CitaForm, self).__init__(*args, **kwargs)

        # Filtra las opciones del campo 'cliente' para que solo muestre el cliente logueado
        if user:
            self.fields['cliente'].queryset = Clientes.objects.filter(perfil_usuarios__user=user)
        else:
            self.fields['cliente'].queryset = Clientes.objects.none()

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documentos
        fields = ['caso', 'tipo_documento', 'descripcion_documento', 'archivo_adjunto']
        widgets = {
            'caso': forms.Select(attrs={'class': 'form-control'}),
            'tipo_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_documento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'archivo_adjunto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class Perfil_UsuarioForm(forms.ModelForm):

    class Meta:
        model = Perfil_Usuario
        fields = ['celular', 'ubicacion','foto_usuario']

class AbogadoForm(forms.ModelForm):
    class Meta:
        model = Abogado
        fields = ['nombrea', 'apellido', 'celular', 'correo', 'experiencia','facebook', 'instagram', 'twitter', 'descripcion', 'tipos_especialidad', 'foto']
    widgets = {   
        'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
    }