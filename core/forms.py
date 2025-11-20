"""
Formularios del sistema ARCA Construcción
Centralizados para mejor mantenimiento
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class ClienteForm(forms.ModelForm):
    """Formulario para clientes"""
    
    class Meta:
        model = Cliente
        fields = [
            'razon_social', 'codigo_fiscal', 'email', 'telefono', 
            'direccion', 'activo'
        ]
        widgets = {
            'razon_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Razón social del cliente'
            }),
            'codigo_fiscal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código fiscal o NIT'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+502 1234-5678'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class ProyectoForm(forms.ModelForm):
    """Formulario para proyectos"""
    
    class Meta:
        model = Proyecto
        fields = [
            'nombre', 'descripcion', 'cliente', 'presupuesto', 
            'fecha_inicio', 'fecha_fin', 'estado', 'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del proyecto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del proyecto'
            }),
            'cliente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'presupuesto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class ColaboradorForm(forms.ModelForm):
    """Formulario para colaboradores"""
    
    class Meta:
        model = Colaborador
        fields = [
            'nombre', 'dpi', 'direccion', 'telefono', 'email', 
            'salario', 'fecha_contratacion', 'fecha_vencimiento_contrato', 'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'dpi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1234567890101'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Dirección'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+502 1234-5678'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'salario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'fecha_contratacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_vencimiento_contrato': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class FacturaForm(forms.ModelForm):
    """Formulario para facturas"""
    
    class Meta:
        model = Factura
        fields = [
            'numero_factura', 'proyecto', 'cliente', 'tipo', 'estado',
            'fecha_emision', 'fecha_vencimiento', 'monto_subtotal',
            'monto_iva', 'monto_total', 'descripcion_servicios',
            'porcentaje_avance', 'metodo_pago', 'referencia_pago',
            'banco_origen', 'observaciones'
        ]
        widgets = {
            'numero_factura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'F001-2025'
            }),
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cliente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_emision': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'monto_subtotal': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'monto_iva': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'monto_total': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'descripcion_servicios': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de los servicios facturados'
            }),
            'porcentaje_avance': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-select'
            }),
            'referencia_pago': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de referencia'
            }),
            'banco_origen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Banco de origen'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales'
            })
        }


class GastoForm(forms.ModelForm):
    """Formulario para gastos"""
    
    class Meta:
        model = Gasto
        fields = [
            'proyecto', 'categoria', 'descripcion', 'monto', 
            'fecha_gasto', 'comprobante'
        ]
        widgets = {
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del gasto'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'fecha_gasto': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'comprobante': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            })
        }


class CategoriaGastoForm(forms.ModelForm):
    """Formulario para categorías de gasto"""
    
    class Meta:
        model = CategoriaGasto
        fields = ['nombre', 'descripcion', 'color', 'icono']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción de la categoría'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
            'icono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-tools'
            })
        }


class UsuarioForm(UserCreationForm):
    """Formulario para crear usuarios"""
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirmar contraseña'
            })
        }


class RolForm(forms.ModelForm):
    """Formulario para roles"""
    
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion', 'modulos_activos']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del rol'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción del rol'
            }),
            'modulos_activos': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            })
        }


class PerfilUsuarioForm(forms.ModelForm):
    """Formulario para perfil de usuario"""
    
    class Meta:
        model = PerfilUsuario
        fields = ['rol', 'telefono', 'direccion', 'activo']
        widgets = {
            'rol': forms.Select(attrs={
                'class': 'form-select'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+502 1234-5678'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Dirección'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class EventoCalendarioForm(forms.ModelForm):
    """Formulario para eventos del calendario"""
    
    class Meta:
        model = EventoCalendario
        fields = [
            'titulo', 'descripcion', 'fecha_inicio', 'fecha_fin',
            'hora_inicio', 'hora_fin', 'tipo', 'color', 'todo_el_dia',
            'proyecto', 'factura'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del evento'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción del evento'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'hora_inicio': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'hora_fin': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'color': forms.Select(attrs={
                'class': 'form-select'
            }),
            'todo_el_dia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'factura': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class ArchivoProyectoForm(forms.ModelForm):
    """Formulario para archivos de proyecto"""
    
    def __init__(self, *args, **kwargs):
        proyecto = kwargs.pop('proyecto', None)
        super().__init__(*args, **kwargs)
        if proyecto:
            self.fields['carpeta'].queryset = CarpetaProyecto.objects.filter(proyecto=proyecto, activa=True)
    
    class Meta:
        model = ArchivoProyecto
        fields = ['nombre', 'descripcion', 'archivo', 'carpeta', 'tipo', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del archivo'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción del archivo'
            }),
            'archivo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.gif,.zip,.rar'
            }),
            'carpeta': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class CarpetaProyectoForm(forms.ModelForm):
    """Formulario para carpetas de proyecto"""
    
    class Meta:
        model = CarpetaProyecto
        fields = ['nombre', 'descripcion', 'carpeta_padre', 'activa']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la carpeta'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción de la carpeta'
            }),
            'carpeta_padre': forms.Select(attrs={
                'class': 'form-select'
            }),
            'activa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class PagoForm(forms.ModelForm):
    """Formulario para pagos"""
    
    class Meta:
        model = Pago
        fields = [
            'factura', 'monto', 'fecha_pago', 'metodo_pago', 
            'estado', 'comprobante_pago'
        ]
        widgets = {
            'factura': forms.Select(attrs={
                'class': 'form-select'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'fecha_pago': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'comprobante_pago': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            })
        }


class AnticipoForm(forms.ModelForm):
    """Formulario para anticipos"""
    
    class Meta:
        model = Anticipo
        fields = [
            'cliente', 'proyecto', 'monto', 'tipo', 'estado', 
            'fecha_recepcion', 'observaciones'
        ]
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_recepcion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones del anticipo'
            })
        }


class PresupuestoForm(forms.ModelForm):
    """Formulario para presupuestos"""
    
    class Meta:
        model = Presupuesto
        fields = ['proyecto', 'nombre', 'version', 'estado']
        widgets = {
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del presupuesto'
            }),
            'version': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1.0'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class PartidaPresupuestoForm(forms.ModelForm):
    """Formulario para partidas de presupuesto"""
    
    class Meta:
        model = PartidaPresupuesto
        fields = [
            'presupuesto', 'codigo', 'descripcion', 'unidad', 
            'cantidad', 'precio_unitario', 'subtotal'
        ]
        widgets = {
            'presupuesto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código de la partida'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción de la partida'
            }),
            'unidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Unidad de medida'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'subtotal': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            })
        }


class VariacionPresupuestoForm(forms.ModelForm):
    """Formulario para variaciones de presupuesto"""
    
    class Meta:
        model = VariacionPresupuesto
        fields = [
            'presupuesto', 'tipo', 'descripcion', 'monto_variacion', 
            'fecha_variacion', 'aprobado'
        ]
        widgets = {
            'presupuesto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción de la variación'
            }),
            'monto_variacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'fecha_variacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'aprobado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class CategoriaInventarioForm(forms.ModelForm):
    """Formulario para categorías de inventario"""
    
    class Meta:
        model = CategoriaInventario
        fields = ['nombre', 'descripcion', 'color', 'icono', 'activa']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción de la categoría'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
            'icono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-tools'
            }),
            'activa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class ItemInventarioForm(forms.ModelForm):
    """Formulario para items de inventario"""
    
    class Meta:
        model = ItemInventario
        fields = [
            'categoria', 'nombre', 'descripcion', 'codigo', 
            'unidad_medida', 'precio_unitario', 'stock_minimo', 'activo'
        ]
        widgets = {
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del item'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción del item'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código del item'
            }),
            'unidad_medida': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Unidad de medida'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class AsignacionInventarioForm(forms.ModelForm):
    """Formulario para asignaciones de inventario"""
    
    class Meta:
        model = AsignacionInventario
        fields = [
            'proyecto', 'item', 'cantidad', 'fecha_asignacion', 
            'responsable', 'observaciones', 'activa'
        ]
        widgets = {
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'item': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'fecha_asignacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'responsable': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Responsable de la asignación'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones de la asignación'
            }),
            'activa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class TrabajadorDiarioForm(forms.ModelForm):
    """Formulario para trabajadores diarios"""
    
    def __init__(self, *args, **kwargs):
        # Extraer parámetros que no son del modelo pero se pasan desde la vista
        self.planilla = kwargs.pop('planilla', None)
        self.proyecto = kwargs.pop('proyecto', None)
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = TrabajadorDiario
        fields = [
            'nombre', 'pago_diario', 'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'pago_diario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class RegistroTrabajoForm(forms.ModelForm):
    """Formulario para registros de trabajo"""
    
    class Meta:
        model = RegistroTrabajo
        fields = [
            'proyecto', 'trabajador', 'fecha_trabajo', 'horas_trabajadas', 
            'descripcion_trabajo', 'observaciones'
        ]
        widgets = {
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'trabajador': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_trabajo': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'horas_trabajadas': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.5',
                'min': '0',
                'max': '24'
            }),
            'descripcion_trabajo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción del trabajo realizado'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales'
            })
        }


class AnticipoTrabajadorDiarioForm(forms.ModelForm):
    """Formulario para anticipos de trabajadores diarios"""
    
    def __init__(self, *args, **kwargs):
        proyecto_id = kwargs.pop('proyecto_id', None)
        trabajador_id = kwargs.pop('trabajador_id', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar trabajadores por proyecto
        if proyecto_id:
            self.fields['trabajador'].queryset = TrabajadorDiario.objects.filter(
                proyecto_id=proyecto_id,
                activo=True
            ).order_by('nombre')
        
        # Preseleccionar trabajador si se pasa trabajador_id
        if trabajador_id and not self.instance.pk:
            try:
                trabajador = TrabajadorDiario.objects.get(id=trabajador_id)
                self.fields['trabajador'].initial = trabajador
            except TrabajadorDiario.DoesNotExist:
                pass
        
        # El estado no debe ser editable en el formulario (se establece automáticamente)
        if 'estado' in self.fields:
            self.fields['estado'].widget = forms.HiddenInput()
    
    class Meta:
        model = AnticipoTrabajadorDiario
        fields = [
            'trabajador', 'monto', 'fecha_anticipo', 
            'observaciones'
        ]
        widgets = {
            'trabajador': forms.Select(attrs={
                'class': 'form-select'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'fecha_anticipo': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales'
            })
        }
        widgets = {
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'trabajador': forms.Select(attrs={
                'class': 'form-select'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'fecha_anticipo': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción del anticipo'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-select'
            }),
            'referencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de referencia'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }