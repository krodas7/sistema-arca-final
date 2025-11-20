"""
Formularios simplificados del sistema ARCA Construcción
Solo los formularios esenciales que funcionan correctamente
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
    
    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto is not None:
            # Convertir a string para validar formato
            monto_str = str(monto)
            try:
                # Validar que sea un número válido
                monto_float = float(monto_str)
                if monto_float < 0:
                    raise forms.ValidationError('El monto no puede ser negativo.')
                if monto_float > 999999.99:
                    raise forms.ValidationError('El monto no puede exceder Q999,999.99.')
                
                # Validar que no tenga más de 2 decimales
                if '.' in monto_str:
                    decimal_part = monto_str.split('.')[1]
                    if len(decimal_part) > 2:
                        raise forms.ValidationError('El monto no puede tener más de 2 decimales.')
                
                return monto_float
            except ValueError:
                raise forms.ValidationError('Ingrese un monto válido.')
        return monto
    
    class Meta:
        model = Gasto
        fields = [
            'proyecto', 'categoria', 'descripcion', 'monto', 
            'fecha_gasto', 'fecha_vencimiento', 'aprobado', 
            'observaciones', 'comprobante'
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
            'monto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'pattern': '[0-9]+(\.[0-9]{1,2})?'
            }),
            'fecha_gasto': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'aprobado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control form-textarea',
                'rows': 4,
                'placeholder': 'Observaciones adicionales (opcional)'
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


class ArchivoProyectoForm(forms.ModelForm):
    """Formulario para archivos de proyecto"""
    
    def __init__(self, *args, **kwargs):
        self.proyecto = kwargs.pop('proyecto', None)
        super().__init__(*args, **kwargs)
        if self.proyecto:
            # Filtrar carpetas del proyecto
            self.fields['carpeta'].queryset = CarpetaProyecto.objects.filter(
                proyecto=self.proyecto, 
                activa=True
            )
            self.fields['carpeta'].required = False
    
    def clean_archivo(self):
        """Validar el archivo subido"""
        import logging
        logger = logging.getLogger(__name__)
        
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            # Extensiones permitidas (COMPLETA)
            extensiones_permitidas = [
                # Documentos
                '.pdf', '.doc', '.docx', '.odt', '.txt', '.rtf',
                # Excel
                '.xls', '.xlsx', '.xlsm', '.xlsb', '.csv',
                # Imágenes
                '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg',
                # Comprimidos
                '.zip', '.rar', '.7z', '.tar', '.gz',
                # CAD
                '.dwg', '.dxf', '.dwf',
                # Otros
                '.ppt', '.pptx', '.xml', '.json'
            ]
            
            # Obtener la extensión del archivo
            nombre_archivo = archivo.name.lower()
            logger.info(f"📎 Archivo recibido: {nombre_archivo}")
            logger.info(f"📎 Tamaño: {archivo.size} bytes")
            
            extension_valida = any(nombre_archivo.endswith(ext) for ext in extensiones_permitidas)
            
            if not extension_valida:
                logger.error(f"❌ Extensión no válida para: {nombre_archivo}")
                raise forms.ValidationError(
                    f'Tipo de archivo no permitido: "{nombre_archivo}". Extensiones permitidas: {", ".join(extensiones_permitidas)}'
                )
            
            logger.info(f"✅ Extensión válida para: {nombre_archivo}")
            
            # Validar tamaño del archivo (máximo 100MB)
            if archivo.size > 100 * 1024 * 1024:  # 100MB
                raise forms.ValidationError('El archivo es demasiado grande. Tamaño máximo: 100MB')
            
            logger.info(f"✅ Tamaño válido: {archivo.size} bytes")
        
        return archivo
    
    class Meta:
        model = ArchivoProyecto
        fields = ['nombre', 'descripcion', 'archivo', 'carpeta', 'tipo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del archivo (opcional, se usa el nombre del archivo si está vacío)'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción del archivo (opcional)'
            }),
            'archivo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.xlsm,.xlsb,.csv,.jpg,.jpeg,.png,.gif,.zip,.rar'
            }),
            'carpeta': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class CarpetaProyectoForm(forms.ModelForm):
    """Formulario para carpetas de proyecto"""
    
    def __init__(self, *args, **kwargs):
        import logging
        logger = logging.getLogger(__name__)
        
        self.proyecto = kwargs.pop('proyecto', None)
        logger.info(f"🔍 CarpetaProyectoForm.__init__ - Proyecto recibido: {self.proyecto}")
        
        super().__init__(*args, **kwargs)
        
        logger.info(f"🔍 Fields disponibles: {list(self.fields.keys())}")
        
        if self.proyecto:
            # Filtrar carpetas padre del mismo proyecto
            self.fields['carpeta_padre'].queryset = CarpetaProyecto.objects.filter(
                proyecto=self.proyecto, 
                activa=True
            )
            self.fields['carpeta_padre'].required = False
            logger.info(f"✅ Carpeta padre configurada para proyecto {self.proyecto.id}")
    
    class Meta:
        model = CarpetaProyecto
        fields = ['nombre', 'descripcion', 'carpeta_padre']
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


class AnticipoForm(forms.ModelForm):
    """Formulario para anticipos"""
    
    class Meta:
        model = Anticipo
        fields = [
            'cliente', 'proyecto', 'numero_anticipo', 'monto', 'tipo', 
            'metodo_pago', 'referencia_pago', 'banco_origen',
            'fecha_recepcion', 'descripcion', 'observaciones'
        ]
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'proyecto': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'numero_anticipo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: ANT-2025-001'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-select'
            }),
            'referencia_pago': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de cheque, transferencia, etc.'
            }),
            'banco_origen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Banco de origen del pago'
            }),
            'fecha_recepcion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción detallada del anticipo'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales'
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
            'cantidad', 'precio_unitario', 'monto_estimado', 'categoria',
            'subcategoria', 'notas', 'orden'
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
            'monto_estimado': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'subcategoria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subcategoría'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Notas adicionales'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            })
        }


class CategoriaInventarioForm(forms.ModelForm):
    """Formulario para categorías de inventario"""
    
    class Meta:
        model = CategoriaInventario
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción de la categoría'
            })
        }


class ItemInventarioForm(forms.ModelForm):
    """Formulario para items de inventario"""
    
    class Meta:
        model = ItemInventario
        fields = [
            'categoria', 'nombre', 'descripcion', 'codigo', 
            'unidad_medida', 'precio_unitario', 'stock_actual', 'stock_minimo', 
            'proveedor', 'fecha_ultima_compra', 'activo'
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
            'proveedor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Proveedor'
            }),
            'fecha_ultima_compra': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
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
            'proyecto', 'item', 'cantidad_asignada', 'fecha_devolucion', 
            'estado', 'notas'
        ]
        widgets = {
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'item': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cantidad_asignada': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'fecha_devolucion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Notas de la asignación'
            })
        }


class TrabajadorDiarioForm(forms.ModelForm):
    """Formulario para trabajadores diarios"""
    
    class Meta:
        model = TrabajadorDiario
        fields = [
            'planilla', 'nombre', 'pago_diario', 'activo'
        ]
        widgets = {
            'planilla': forms.Select(attrs={
                'class': 'form-control'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del trabajador'
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
    
    def __init__(self, *args, **kwargs):
        self.planilla = kwargs.pop('planilla', None)
        proyecto = kwargs.pop('proyecto', None)
        super().__init__(*args, **kwargs)
        
        # Cargar planillas del proyecto
        if proyecto:
            self.fields['planilla'].queryset = PlanillaTrabajadoresDiarios.objects.filter(proyecto=proyecto)
            self.fields['planilla'].empty_label = "Selecciona una planilla"
        
        # Si se pasa una planilla específica, seleccionarla
        if self.planilla:
            self.fields['planilla'].initial = self.planilla


class RegistroTrabajoForm(forms.ModelForm):
    """Formulario para registros de trabajo"""
    
    class Meta:
        model = RegistroTrabajo
        fields = [
            'trabajador', 'fecha_inicio', 'fecha_fin', 'dias_trabajados', 
            'observaciones'
        ]
        widgets = {
            'trabajador': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'dias_trabajados': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones del período de trabajo'
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
    
    def clean(self):
        cleaned_data = super().clean()
        trabajador = cleaned_data.get('trabajador')
        monto = cleaned_data.get('monto')
        
        # Validar que se haya seleccionado un trabajador
        if not trabajador:
            raise forms.ValidationError({
                'trabajador': 'Debes seleccionar un trabajador'
            })
        
        # Validar que el monto sea mayor a 0
        if monto is not None and monto <= 0:
            raise forms.ValidationError({
                'monto': 'El monto debe ser mayor a 0'
            })
        
        return cleaned_data
    
    class Meta:
        model = AnticipoTrabajadorDiario
        fields = [
            'trabajador', 'monto', 'fecha_anticipo', 'observaciones'
        ]
        widgets = {
            'trabajador': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'required': True
            }),
            'fecha_anticipo': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales'
            })
        }


class PlanillaTrabajadoresDiariosForm(forms.ModelForm):
    """Formulario para crear/editar planillas de trabajadores diarios"""
    
    class Meta:
        model = PlanillaTrabajadoresDiarios
        fields = [
            'nombre', 'descripcion', 'observaciones'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Planilla Semana 1, Planilla Enero 2025'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la planilla'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales'
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.proyecto = kwargs.pop('proyecto', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
