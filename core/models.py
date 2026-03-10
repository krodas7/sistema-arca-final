from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from django.core.exceptions import ValidationError


class Rol(models.Model):
    """Modelo para roles de usuario"""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    modulos_activos = models.ManyToManyField('Modulo', blank=True, related_name='roles_activos')
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return self.nombre


class Modulo(models.Model):
    """Modelo para módulos del sistema"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=50, blank=True, help_text="Clase CSS del icono")
    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['orden']
    
    def __str__(self):
        return self.nombre


class Permiso(models.Model):
    """Modelo para permisos específicos"""
    TIPO_CHOICES = [
        ('ver', 'Ver'),
        ('crear', 'Crear'),
        ('editar', 'Editar'),
        ('eliminar', 'Eliminar'),
        ('exportar', 'Exportar'),
        ('importar', 'Importar'),
        ('reset', 'Reset'),
    ]
    
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'
        unique_together = ['codigo', 'modulo']
    
    def __str__(self):
        return f"{self.modulo.nombre} - {self.nombre}"


class RolPermiso(models.Model):
    """Modelo para asignar permisos a roles"""
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Permiso de Rol'
        verbose_name_plural = 'Permisos de Rol'
        unique_together = ['rol', 'permiso']
    
    def __str__(self):
        return f"{self.rol.nombre} - {self.permiso.nombre}"


class PerfilUsuario(models.Model):
    """Modelo para extender el usuario de Django"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    ultimo_acceso = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'
    
    def __str__(self):
        if self.rol:
            return f"{self.usuario.get_full_name()} - {self.rol.nombre}"
        else:
            return f"{self.usuario.get_full_name()} - Sin rol"
    
    def tiene_permiso(self, codigo_permiso):
        """Verifica si el usuario tiene un permiso específico"""
        try:
            if not self.rol:
                return False
            return RolPermiso.objects.filter(
                rol=self.rol,
                permiso__codigo=codigo_permiso,
                activo=True
            ).exists()
        except:
            return False
    
    def tiene_permiso_modulo(self, codigo_modulo, tipo_permiso='ver'):
        """Verifica si el usuario tiene un permiso específico en un módulo"""
        try:
            if not self.rol:
                return False
            return RolPermiso.objects.filter(
                rol=self.rol,
                permiso__modulo__nombre=codigo_modulo,
                permiso__tipo=tipo_permiso,
                activo=True
            ).exists()
        except:
            return False


class Cliente(models.Model):
    """Modelo para clientes"""
    razon_social = models.CharField(max_length=200)
    codigo_fiscal = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    
    def __str__(self):
        return self.razon_social


class Colaborador(models.Model):
    """Modelo para colaboradores"""
    nombre = models.CharField(max_length=100)
    dpi = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_contratacion = models.DateField(null=True, blank=True)
    fecha_vencimiento_contrato = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Colaborador'
        verbose_name_plural = 'Colaboradores'
    
    def __str__(self):
        return self.nombre
    
    def calcular_salario_neto(self, proyecto):
        """Calcula el salario neto considerando anticipos pendientes del proyecto"""
        salario_base = self.salario or 0
        anticipos_pendientes = self.anticipos_proyecto.filter(
            proyecto=proyecto,
            estado='pendiente'
        ).aggregate(total=Sum('monto'))['total'] or 0
        
        return salario_base - anticipos_pendientes


class Proyecto(models.Model):
    """Modelo para proyectos"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    colaboradores = models.ManyToManyField(Colaborador, blank=True, related_name='proyectos')
    presupuesto = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
    
    def clean(self):
        """Validaciones del modelo Proyecto"""
        if self.fecha_fin and self.fecha_inicio and self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")
        
        if self.presupuesto and self.presupuesto < 0:
            raise ValidationError("El presupuesto no puede ser negativo.")
    
    def __str__(self):
        return f"{self.nombre} - {self.cliente.razon_social}"
    
    def get_gastos_aprobados(self):
        """Obtener gastos aprobados del proyecto"""
        return self.gasto_set.filter(aprobado=True)
    
    def get_total_gastos_aprobados(self):
        """Calcular total de gastos aprobados"""
        from django.db.models import Sum
        total = self.gasto_set.filter(aprobado=True).aggregate(
            total=Sum('monto')
        )['total']
        return Decimal(str(total)) if total else Decimal('0.00')
    
    def get_total_gastos_pendientes(self):
        """Calcular total de gastos pendientes"""
        from django.db.models import Sum
        total = self.gasto_set.filter(aprobado=False).aggregate(
            total=Sum('monto')
        )['total']
        return Decimal(str(total)) if total else Decimal('0.00')
    
    def get_presupuesto_disponible(self):
        """Calcular presupuesto disponible (presupuesto - gastos aprobados)"""
        if self.presupuesto is None:
            return None
        return self.presupuesto - self.get_total_gastos_aprobados()


class ArchivoAdjunto(models.Model):
    """Modelo para archivos adjuntos"""
    TIPO_CHOICES = [
        ('cliente', 'Cliente'),
        ('proyecto', 'Proyecto'),
        ('factura', 'Factura'),
        ('gasto', 'Gasto'),
        ('pago', 'Pago'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    registro_id = models.IntegerField()
    nombre_archivo = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='archivos_adjuntos/')
    tipo_mime = models.CharField(max_length=100, blank=True)
    tamano = models.IntegerField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Archivo Adjunto'
        verbose_name_plural = 'Archivos Adjuntos'
    
    def __str__(self):
        return f"{self.nombre_archivo} - {self.tipo}"


class Factura(models.Model):
    """Modelo para manejar facturas de proyectos"""
    
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('emitida', 'Emitida'),
        ('enviada', 'Enviada al Cliente'),
        ('pagada', 'Pagada'),
        ('vencida', 'Vencida'),
        ('cancelada', 'Cancelada'),
    ]
    
    TIPO_CHOICES = [
        ('progreso', 'Factura por Progreso de Obra'),
        ('final', 'Factura Final'),
        ('adicional', 'Factura por Trabajos Adicionales'),
        ('retencion', 'Factura por Retención'),
        ('otros', 'Otros'),
    ]
    
    numero_factura = models.CharField(max_length=20, unique=True, help_text="Número único de la factura")
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='facturas')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='facturas')
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='progreso')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    
    fecha_emision = models.DateField(help_text="Fecha de emisión de la factura", default=timezone.now)
    fecha_vencimiento = models.DateField(help_text="Fecha de vencimiento para el pago", default=timezone.now)
    fecha_pago = models.DateField(null=True, blank=True, help_text="Fecha en que se pagó completamente")
    
    # Montos
    monto_subtotal = models.DecimalField(max_digits=12, decimal_places=2, help_text="Subtotal antes de impuestos", default=0)
    monto_iva = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Monto del IVA")
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, help_text="Monto total de la factura", default=0)
    monto_pagado = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Monto ya pagado")
    monto_anticipos = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Monto de anticipos aplicados")
    monto_pendiente = models.DecimalField(max_digits=12, decimal_places=2, help_text="Monto pendiente de pago", default=0)
    
    # Detalles
    descripcion_servicios = models.TextField(help_text="Descripción detallada de los servicios facturados", default="Servicios de construcción")
    porcentaje_avance = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Porcentaje de avance del proyecto")
    
    # Campos de pago
    metodo_pago = models.CharField(max_length=50, choices=[
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia Bancaria'),
        ('cheque', 'Cheque'),
        ('tarjeta', 'Tarjeta de Crédito/Débito'),
        ('anticipo', 'Anticipo'),
        ('otros', 'Otros'),
    ], blank=True)
    
    referencia_pago = models.CharField(max_length=100, blank=True, help_text="Número de referencia del pago")
    banco_origen = models.CharField(max_length=100, blank=True, help_text="Banco de origen del pago")
    
    # Campos adicionales
    observaciones = models.TextField(blank=True, help_text="Observaciones adicionales")
    archivos_adjuntos = models.ManyToManyField(ArchivoAdjunto, blank=True, related_name='facturas')
    
    # Campos de auditoría
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='facturas_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='facturas_modificadas')
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha_emision', '-numero_factura']
        indexes = [
            models.Index(fields=['proyecto', 'cliente']),
            models.Index(fields=['estado', 'fecha_vencimiento']),
            models.Index(fields=['numero_factura']),
        ]
    
    def clean(self):
        """Validaciones del modelo Factura"""
        if self.fecha_vencimiento and self.fecha_emision and self.fecha_vencimiento < self.fecha_emision:
            raise ValidationError("La fecha de vencimiento debe ser posterior a la fecha de emisión.")
        
        if self.monto_total and self.monto_total < 0:
            raise ValidationError("El monto total no puede ser negativo.")
        
        if self.monto_pagado and self.monto_pagado < 0:
            raise ValidationError("El monto pagado no puede ser negativo.")
        
        if self.monto_pagado and self.monto_total and self.monto_pagado > self.monto_total:
            raise ValidationError("El monto pagado no puede ser mayor al monto total.")
    
    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente.razon_social} - Q{self.monto_total}"
    
    def save(self, *args, **kwargs):
        # Calcular montos si no están definidos
        if not self.monto_total:
            self.monto_total = self.monto_subtotal + self.monto_iva
        
        # Calcular monto pendiente
        self.monto_pendiente = self.monto_total - self.monto_pagado - self.monto_anticipos
        
        # Actualizar estado basado en montos
        if self.monto_pendiente <= 0:
            self.estado = 'pagada'
            if not self.fecha_pago:
                self.fecha_pago = timezone.now().date()
        elif self.fecha_vencimiento and timezone.now().date() > self.fecha_vencimiento:
            if self.estado not in ['pagada', 'cancelada']:
                self.estado = 'vencida'
        
        super().save(*args, **kwargs)
    
    def es_vencida(self):
        """Verificar si la factura está vencida"""
        if not self.fecha_vencimiento:
            return False
        return timezone.now().date() > self.fecha_vencimiento and self.estado not in ['pagada', 'cancelada']
    
    def dias_para_vencer(self):
        """Calcular días restantes para vencer"""
        if not self.fecha_vencimiento:
            return None
        dias = (self.fecha_vencimiento - timezone.now().date()).days
        return dias if dias > 0 else 0
    
    @property
    def dias_vencimiento_formateado(self):
        """Formatear días de vencimiento para mostrar en la UI"""
        if not self.fecha_vencimiento:
            return "Sin fecha"
        
        dias = self.dias_para_vencer()
        if dias is None:
            return "Sin fecha"
        elif dias == 0:
            return "Vence hoy"
        elif dias < 0:
            return f"Vencida hace {abs(dias)} días"
        elif dias == 1:
            return "Vence mañana"
        elif dias <= 7:
            return f"Vence en {dias} días"
        else:
            return f"Vence en {dias} días"
    
    def actualizar_estado_vencimiento(self):
        """Actualizar estado de vencimiento manualmente"""
        if self.es_vencida():
            self.estado = 'vencida'
            self.save(update_fields=['estado'])
        return self.estado
    
    @property
    def dias_vencimiento(self):
        """Retorna los días hasta el vencimiento"""
        if self.fecha_vencimiento:
            fecha_vencimiento = self.fecha_vencimiento.date() if hasattr(self.fecha_vencimiento, 'date') else self.fecha_vencimiento
            delta = fecha_vencimiento - timezone.now().date()
            return delta.days
        return None
    
    @property
    def porcentaje_pagado(self):
        """Retorna el porcentaje de la factura que ya fue pagado"""
        if self.monto_total > 0:
            return ((self.monto_pagado + self.monto_anticipos) / self.monto_total) * 100
        return 0
    
    def puede_aplicar_anticipo(self, monto_anticipo):
        """Verifica si se puede aplicar un anticipo a esta factura"""
        return self.monto_pendiente >= monto_anticipo and self.estado not in ['pagada', 'cancelada']
    
    def aplicar_anticipo(self, anticipo, monto):
        """Aplica un anticipo a esta factura"""
        if not self.puede_aplicar_anticipo(monto):
            raise ValueError(f"No se puede aplicar Q{monto} del anticipo a esta factura")
        
        # Aplicar el anticipo
        anticipo.aplicar_a_factura(self, monto)
        return True


class Pago(models.Model):
    """Modelo para pagos"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('rechazado', 'Rechazado'),
    ]
    
    METODO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('cheque', 'Cheque'),
        ('tarjeta', 'Tarjeta'),
    ]
    
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='pagos')
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_pago = models.DateField()
    metodo_pago = models.CharField(max_length=20, choices=METODO_CHOICES, default='transferencia')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    comprobante_pago = models.FileField(upload_to='comprobantes/', blank=True)
    registrado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
    
    def __str__(self):
        return f"Pago {self.id} - {self.factura.numero_factura}"


class CategoriaGasto(models.Model):
    """Modelo para categorías de gastos"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text="Color hexadecimal (ej: #007bff)")
    icono = models.CharField(max_length=50, default='fas fa-tools', help_text="Clase de Font Awesome (ej: fas fa-tools)")
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoría de Gasto'
        verbose_name_plural = 'Categorías de Gastos'
    
    def __str__(self):
        return self.nombre


class Gasto(models.Model):
    """Modelo para gastos"""
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaGasto, on_delete=models.CASCADE)
    descripcion = models.TextField()
    monto = models.FloatField()
    fecha_gasto = models.DateField()
    fecha_vencimiento = models.DateField(null=True, blank=True, help_text="Fecha límite para el pago (opcional)")
    aprobado = models.BooleanField(default=False)
    aprobado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    observaciones = models.TextField(blank=True, help_text="Observaciones adicionales sobre el gasto")
    comprobante = models.FileField(upload_to='comprobantes_gastos/', blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
    
    def __str__(self):
        return f"{self.descripcion} - Q{self.monto}"


class GastoFijoMensual(models.Model):
    """Modelo para gastos fijos mensuales"""
    concepto = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Gasto Fijo Mensual'
        verbose_name_plural = 'Gastos Fijos Mensuales'
    
    def __str__(self):
        return f"{self.concepto} - Q{self.monto}"


class LogActividad(models.Model):
    """Modelo para log de actividades"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=100)
    modulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    fecha_actividad = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Log de Actividad'
        verbose_name_plural = 'Logs de Actividad'
        ordering = ['-fecha_actividad']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.accion} - {self.fecha_actividad}"


class Anticipo(models.Model):
    """Modelo para manejar anticipos de clientes a proyectos"""
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente de Aplicar'),
        ('aplicado', 'Aplicado a Facturas'),
        ('liquidado', 'Liquidado'),
        ('devuelto', 'Devuelto al Cliente'),
        ('cancelado', 'Cancelado'),
    ]
    
    TIPO_CHOICES = [
        ('anticipo', 'Anticipo de Obra'),
        ('materiales', 'Anticipo de Materiales'),
        ('gastos', 'Anticipo de Gastos'),
        ('otros', 'Otros Anticipos'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='anticipos')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='anticipos')
    numero_anticipo = models.CharField(max_length=20, unique=True, help_text="Número único del anticipo")
    
    monto = models.DecimalField(max_digits=12, decimal_places=2, help_text="Monto del anticipo en GTQ")
    monto_aplicado = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Monto ya aplicado a facturas")
    monto_disponible = models.DecimalField(max_digits=12, decimal_places=2, help_text="Monto disponible para aplicar")
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='anticipo')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    fecha_recepcion = models.DateField(help_text="Fecha en que se recibió el anticipo", default=timezone.now)
    fecha_vencimiento = models.DateField(null=True, blank=True, help_text="Fecha de vencimiento del anticipo")
    fecha_aplicacion = models.DateField(null=True, blank=True, help_text="Fecha en que se aplicó completamente")
    
    metodo_pago = models.CharField(max_length=50, choices=[
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia Bancaria'),
        ('cheque', 'Cheque'),
        ('tarjeta', 'Tarjeta de Crédito/Débito'),
        ('otros', 'Otros'),
    ], default='transferencia')
    
    referencia_pago = models.CharField(max_length=100, blank=True, help_text="Número de referencia, cheque, etc.")
    banco_origen = models.CharField(max_length=100, blank=True, help_text="Banco de origen del pago")
    
    descripcion = models.TextField(blank=True, help_text="Descripción detallada del anticipo")
    observaciones = models.TextField(blank=True, help_text="Observaciones adicionales")
    
    # Campos de auditoría
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='anticipos_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='anticipos_modificados')
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    # Campos para seguimiento
    facturas_aplicadas = models.ManyToManyField(Factura, through='AplicacionAnticipo', blank=True)
    
    # Campo para indicar si se aplicó al proyecto directamente
    aplicado_al_proyecto = models.BooleanField(default=False, help_text="Indica si el anticipo se aplicó directamente al proyecto")
    monto_aplicado_proyecto = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Monto aplicado directamente al proyecto")
    
    class Meta:
        verbose_name = 'Anticipo'
        verbose_name_plural = 'Anticipos'
        ordering = ['-fecha_recepcion', '-fecha_creacion']
        indexes = [
            models.Index(fields=['cliente', 'proyecto']),
            models.Index(fields=['estado', 'fecha_recepcion']),
            models.Index(fields=['numero_anticipo']),
        ]
    
    def __str__(self):
        return f"Anticipo {self.numero_anticipo} - {self.cliente.razon_social} - Q{self.monto}"
    
    def save(self, *args, **kwargs):
        # Calcular monto disponible considerando aplicaciones a facturas y al proyecto
        if not self.pk:  # Nuevo anticipo
            self.monto_disponible = self.monto
        else:
            total_aplicado = self.monto_aplicado + self.monto_aplicado_proyecto
            self.monto_disponible = self.monto - total_aplicado
        
        # Actualizar estado basado en montos
        total_aplicado = self.monto_aplicado + self.monto_aplicado_proyecto
        if total_aplicado >= self.monto:
            self.estado = 'liquidado'
            if not self.fecha_aplicacion:
                self.fecha_aplicacion = timezone.now().date()
        else:
            # Solo "pendiente" hasta que se aplique completamente
            self.estado = 'pendiente'
        
        super().save(*args, **kwargs)
    
    @property
    def total_aplicado(self):
        """Retorna el monto total aplicado (facturas + proyecto)"""
        return self.monto_aplicado + self.monto_aplicado_proyecto
    
    @property
    def porcentaje_aplicado(self):
        """Retorna el porcentaje del anticipo que ya fue aplicado"""
        if self.monto > 0:
            return float((self.total_aplicado / self.monto) * 100)
        return 0.0
    
    @property
    def dias_vencimiento(self):
        """Retorna los días hasta el vencimiento"""
        if self.fecha_vencimiento:
            delta = self.fecha_vencimiento - timezone.now().date()
            return delta.days
        return None
    
    def puede_aplicar(self, monto_factura):
        """Verifica si se puede aplicar un monto a una factura"""
        return self.monto_disponible >= monto_factura and self.estado == 'pendiente'
    
    def aplicar_a_factura(self, factura, monto):
        """Aplica el anticipo a una factura específica"""
        if not self.puede_aplicar(monto):
            raise ValueError(f"No se puede aplicar Q{monto} del anticipo")
        
        # Crear la aplicación
        AplicacionAnticipo.objects.create(
            anticipo=self,
            factura=factura,
            monto_aplicado=monto,
            fecha_aplicacion=timezone.now().date()
        )
        
        # Actualizar montos
        self.monto_aplicado += monto
        self.save()
        
        # Actualizar factura
        factura.monto_anticipos += monto
        factura.save()
        
        return True
    
    def aplicar_al_proyecto(self, monto):
        """Aplica el anticipo directamente al proyecto"""
        if not self.puede_aplicar(monto):
            raise ValueError(f"No se puede aplicar Q{monto} del anticipo al proyecto")
        
        # Actualizar montos y fecha de aplicación (sumar al existente)
        self.monto_aplicado_proyecto += monto
        self.aplicado_al_proyecto = True
        self.fecha_aplicacion = timezone.now().date()
        self.save()
        
        return True


class AplicacionAnticipo(models.Model):
    """Modelo para rastrear cómo se aplican los anticipos a las facturas"""
    
    anticipo = models.ForeignKey(Anticipo, on_delete=models.CASCADE, related_name='aplicaciones')
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='aplicaciones_anticipo')
    
    monto_aplicado = models.DecimalField(max_digits=12, decimal_places=2, help_text="Monto del anticipo aplicado a esta factura")
    fecha_aplicacion = models.DateField(auto_now_add=True)
    
    # Campos de auditoría
    aplicado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='aplicaciones_anticipo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Aplicación de Anticipo'
        verbose_name_plural = 'Aplicaciones de Anticipos'
        unique_together = ['anticipo', 'factura']
        ordering = ['-fecha_aplicacion']
    
    def __str__(self):
        return f"Aplicación Q{self.monto_aplicado} - {self.anticipo} → {self.factura}"


class ArchivoProyecto(models.Model):
    """Archivos adjuntos a proyectos (planos, documentos, imágenes)"""
    
    TIPO_CHOICES = [
        ('plano', 'Plano'),
        ('documento', 'Documento'),
        ('imagen', 'Imagen'),
        ('excel', 'Excel'),
        ('contrato', 'Contrato'),
        ('permiso', 'Permiso'),
        ('otro', 'Otro'),
    ]
    
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='archivos')
    carpeta = models.ForeignKey('CarpetaProyecto', on_delete=models.CASCADE, related_name='archivos', null=True, blank=True, help_text="Carpeta donde se almacena el archivo")
    nombre = models.CharField(max_length=255, help_text="Nombre descriptivo del archivo")
    archivo = models.FileField(upload_to='proyectos/archivos/', help_text="Archivo a subir")
    thumbnail = models.ImageField(upload_to='proyectos/thumbnails/', blank=True, null=True, help_text="Miniatura generada automáticamente")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='documento')
    descripcion = models.TextField(blank=True, help_text="Descripción del archivo")
    fecha_subida = models.DateTimeField(auto_now_add=True)
    subido_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='archivos_subidos')
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-fecha_subida']
        verbose_name = 'Archivo de Proyecto'
        verbose_name_plural = 'Archivos de Proyecto'
    
    def __str__(self):
        return f"{self.nombre} - {self.proyecto.nombre}"
    
    def get_extension(self):
        """Obtener la extensión del archivo"""
        return self.archivo.name.split('.')[-1].lower()
    
    def get_tamaño_archivo(self):
        """Obtener el tamaño del archivo en formato legible"""
        try:
            size = self.archivo.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except:
            return "N/A"
    
    def es_imagen(self):
        """Verificar si el archivo es una imagen"""
        extensiones_imagen = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']
        return self.get_extension() in extensiones_imagen
    
    def es_documento(self):
        """Verificar si el archivo es un documento"""
        extensiones_documento = ['pdf', 'doc', 'docx', 'txt', 'rtf', 'xlsx', 'xls']
        return self.get_extension() in extensiones_documento
    
    def es_plano(self):
        """Verificar si el archivo es un plano"""
        extensiones_plano = ['dwg', 'dxf', 'pdf', 'jpg', 'jpeg', 'png']
        return self.get_extension() in extensiones_plano
    
    def es_excel(self):
        """Verificar si el archivo es una hoja de cálculo Excel"""
        extensiones_excel = ['xlsx', 'xls']
        return self.get_extension() in extensiones_excel
    
    def generar_thumbnail(self):
        """Generar miniatura del archivo si es posible"""
        try:
            from PIL import Image
            import os
            from django.conf import settings
            
            # Solo generar thumbnail para imágenes
            if not self.es_imagen():
                return
            
            # Abrir la imagen
            img = Image.open(self.archivo.path)
            
            # Convertir a RGB si es necesario
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Redimensionar manteniendo proporción
            img.thumbnail((200, 200), Image.Resampling.LANCZOS)
            
            # Crear nombre para el thumbnail
            nombre_base = os.path.splitext(os.path.basename(self.archivo.name))[0]
            extension = 'jpg'
            nombre_thumbnail = f"{nombre_base}_thumb.{extension}"
            
            # Ruta completa para el thumbnail
            ruta_thumbnail = os.path.join('proyectos/thumbnails/', nombre_thumbnail)
            ruta_completa = os.path.join(settings.MEDIA_ROOT, ruta_thumbnail)
            
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
            
            # Guardar thumbnail
            img.save(ruta_completa, 'JPEG', quality=85, optimize=True)
            
            # Actualizar campo thumbnail
            self.thumbnail = ruta_thumbnail
            self.save(update_fields=['thumbnail'])
            
        except Exception as e:
            print(f"Error generando thumbnail para {self.nombre}: {e}")
            pass


class CarpetaProyecto(models.Model):
    """Carpetas para organizar archivos de proyectos"""
    
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='carpetas')
    carpeta_padre = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcarpetas', null=True, blank=True, help_text="Carpeta padre (dejar vacío para carpeta raíz)")
    nombre = models.CharField(max_length=255, help_text="Nombre de la carpeta")
    descripcion = models.TextField(blank=True, help_text="Descripción de la carpeta")
    color = models.CharField(max_length=7, default='#667eea', help_text="Color de la carpeta (hex)")
    icono = models.CharField(max_length=50, default='fas fa-folder', help_text="Clase del icono de FontAwesome")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creada_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carpetas_creadas')
    activa = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['nombre']
        verbose_name = 'Carpeta de Proyecto'
        verbose_name_plural = 'Carpetas de Proyecto'
        unique_together = ['proyecto', 'carpeta_padre', 'nombre']
    
    def __str__(self):
        if self.carpeta_padre:
            return f"{self.carpeta_padre.nombre} / {self.nombre}"
        return f"{self.proyecto.nombre} / {self.nombre}"
    
    def get_ruta_completa(self):
        """Obtener la ruta completa de la carpeta"""
        ruta = [self.nombre]
        carpeta_actual = self.carpeta_padre
        
        while carpeta_actual:
            ruta.insert(0, carpeta_actual.nombre)
            carpeta_actual = carpeta_actual.carpeta_padre
        
        return " / ".join(ruta)
    
    def get_nivel(self):
        """Obtener el nivel de profundidad de la carpeta"""
        nivel = 0
        carpeta_actual = self.carpeta_padre
        
        while carpeta_actual:
            nivel += 1
            carpeta_actual = carpeta_actual.carpeta_padre
        
        return nivel
    
    def get_total_archivos(self):
        """Obtener el total de archivos en esta carpeta y subcarpetas"""
        total = self.archivos.count()
        
        for subcarpeta in self.subcarpetas.filter(activa=True):
            total += subcarpeta.get_total_archivos()
        
        return total
    
    def get_subcarpetas_activas(self):
        """Obtener subcarpetas activas"""
        return self.subcarpetas.filter(activa=True)
    
    def es_carpeta_raiz(self):
        """Verificar si es una carpeta raíz"""
        return self.carpeta_padre is None
    
    def puede_eliminarse(self):
        """Verificar si la carpeta puede ser eliminada"""
        return self.archivos.count() == 0 and self.subcarpetas.filter(activa=True).count() == 0


class Presupuesto(models.Model):
    """Presupuesto inicial de un proyecto"""
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='presupuestos')
    nombre = models.CharField(max_length=200, help_text="Nombre descriptivo del presupuesto")
    version = models.CharField(max_length=20, default="1.0", help_text="Versión del presupuesto")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('borrador', 'Borrador'),
            ('en_revision', 'En Revisión'),
            ('aprobado', 'Aprobado'),
            ('rechazado', 'Rechazado'),
            ('obsoleto', 'Obsoleto')
        ],
        default='borrador'
    )
    monto_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    monto_aprobado = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='presupuestos_creados')
    aprobado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='presupuestos_aprobados')
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ['proyecto', 'version']
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Presupuesto {self.version} - {self.proyecto.nombre}"

    def calcular_total(self):
        """Calcular el monto total del presupuesto"""
        total = self.partidas.aggregate(
            total=models.Sum('monto_estimado')
        )['total'] or 0
        self.monto_total = total
        self.save(update_fields=['monto_total'])
        return total

    def obtener_variacion(self):
        """Obtener la variación entre presupuesto y gastos reales"""
        gastos_reales = Gasto.objects.filter(
            proyecto=self.proyecto,
            aprobado=True
        ).aggregate(total=models.Sum('monto'))['total'] or 0
        
        return {
            'presupuesto': self.monto_total,
            'gastos_reales': gastos_reales,
            'variacion': gastos_reales - self.monto_total,
            'porcentaje_variacion': (gastos_reales / self.monto_total * 100) if self.monto_total > 0 else 0
        }

class PartidaPresupuesto(models.Model):
    """Partida individual del presupuesto"""
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, related_name='partidas')
    codigo = models.CharField(max_length=20, help_text="Código de la partida")
    descripcion = models.CharField(max_length=500)
    unidad = models.CharField(max_length=50, help_text="Unidad de medida (m², m³, kg, etc.)")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    monto_estimado = models.DecimalField(max_digits=15, decimal_places=2)
    categoria = models.ForeignKey(CategoriaGasto, on_delete=models.SET_NULL, null=True, blank=True)
    subcategoria = models.CharField(max_length=100, blank=True)
    notas = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden', 'codigo']

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    def save(self, *args, **kwargs):
        """Calcular automáticamente el monto estimado"""
        if self.cantidad and self.precio_unitario:
            self.monto_estimado = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        # Actualizar total del presupuesto
        self.presupuesto.calcular_total()

class VariacionPresupuesto(models.Model):
    """Registro de variaciones del presupuesto"""
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, related_name='variaciones')
    partida = models.ForeignKey(PartidaPresupuesto, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(
        max_length=20,
        choices=[
            ('aumento', 'Aumento'),
            ('disminucion', 'Disminución'),
            ('nueva_partida', 'Nueva Partida'),
            ('eliminacion', 'Eliminación')
        ]
    )
    monto_anterior = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    monto_nuevo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    diferencia = models.DecimalField(max_digits=15, decimal_places=2)
    motivo = models.TextField()
    fecha_variacion = models.DateTimeField(auto_now_add=True)
    aprobado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('aprobada', 'Aprobada'),
            ('rechazada', 'Rechazada')
        ],
        default='pendiente'
    )

    class Meta:
        ordering = ['-fecha_variacion']

    def __str__(self):
        return f"Variación {self.tipo} - {self.presupuesto.proyecto.nombre}"

# ==================== MODELO DE NOTIFICACIONES ====================

class NotificacionSistema(models.Model):
    """Notificaciones personalizadas del sistema de construcción"""
    
    TIPO_CHOICES = [
        ('factura_vencida', 'Factura Vencida'),
        ('pago_pendiente', 'Pago Pendiente'),
        ('gasto_aprobacion', 'Gasto Requiere Aprobación'),
        ('proyecto_estado', 'Cambio de Estado del Proyecto'),
        ('anticipo_disponible', 'Anticipo Disponible'),
        ('presupuesto_revision', 'Presupuesto Requiere Revisión'),
        ('archivo_subido', 'Nuevo Archivo Subido'),
        ('sistema', 'Notificación del Sistema'),
    ]
    
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='media')
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_lectura = models.DateTimeField(null=True, blank=True)
    
    # Campos opcionales para enlazar con otros modelos
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True, blank=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, null=True, blank=True)
    gasto = models.ForeignKey(Gasto, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
    
    def __str__(self):
        return f"{self.tipo}: {self.titulo}"
    
    def marcar_como_leida(self):
        """Marca la notificación como leída"""
        self.leida = True
        self.fecha_lectura = timezone.now()
        self.save()
    
    def get_icono(self):
        """Retorna el icono apropiado según el tipo"""
        iconos = {
            'factura_vencida': 'fas fa-exclamation-triangle text-warning',
            'pago_pendiente': 'fas fa-clock text-info',
            'gasto_aprobacion': 'fas fa-check-circle text-primary',
            'proyecto_estado': 'fas fa-project-diagram text-success',
            'anticipo_disponible': 'fas fa-money-bill-wave text-success',
            'presupuesto_revision': 'fas fa-file-invoice-dollar text-warning',
            'archivo_subido': 'fas fa-file-upload text-info',
            'sistema': 'fas fa-cog text-secondary',
        }
        return iconos.get(self.tipo, 'fas fa-bell text-primary')
    
    def get_color_clase(self):
        """Retorna la clase de color según la prioridad"""
        colores = {
            'baja': 'text-muted',
            'media': 'text-info',
            'alta': 'text-warning',
            'urgente': 'text-danger',
        }
        return colores.get(self.prioridad, 'text-primary')


# ==================== MODELO DE CONFIGURACIÓN DE NOTIFICACIONES ====================

class ConfiguracionNotificaciones(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='configuracion_notificaciones')
    
    # Configuración general
    notificaciones_habilitadas = models.BooleanField(default=True, help_text="Activar/desactivar todas las notificaciones")
    
    # Tipos de notificaciones
    facturas_vencidas = models.BooleanField(default=True, help_text="Notificaciones de facturas vencidas")
    pagos_pendientes = models.BooleanField(default=True, help_text="Notificaciones de pagos pendientes")
    gastos_pendientes = models.BooleanField(default=True, help_text="Notificaciones de gastos pendientes")
    archivos_subidos = models.BooleanField(default=True, help_text="Notificaciones de archivos subidos")
    presupuestos_revision = models.BooleanField(default=True, help_text="Notificaciones de presupuestos en revisión")
    
    # Configuración de email
    email_habilitado = models.BooleanField(default=True, help_text="Recibir notificaciones por email")
    resumen_diario = models.BooleanField(default=False, help_text="Recibir resumen diario por email")
    frecuencia_email = models.CharField(
        max_length=20,
        choices=[
            ('inmediato', 'Inmediato'),
            ('cada_hora', 'Cada hora'),
            ('diario', 'Diario'),
            ('semanal', 'Semanal')
        ],
        default='inmediato',
        help_text="Frecuencia de envío de emails"
    )
    
    # Horario de notificaciones
    horario_inicio = models.TimeField(blank=True, null=True, help_text="Hora de inicio para recibir notificaciones")
    horario_fin = models.TimeField(blank=True, null=True, help_text="Hora de fin para recibir notificaciones")
    
    # Configuración de interfaz
    mostrar_popup = models.BooleanField(default=True, help_text="Mostrar popup de notificaciones")
    sonido_notificacion = models.BooleanField(default=True, help_text="Reproducir sonido de notificación")
    
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuración de Notificaciones"
        verbose_name_plural = "Configuraciones de Notificaciones"
    
    def __str__(self):
        return f"Configuración de {self.usuario.username}"
    
    def get_configuracion_activa(self):
        """Retorna la configuración activa para el usuario"""
        return {
            'notificaciones_habilitadas': self.notificaciones_habilitadas,
            'email_habilitado': self.email_habilitado,
            'resumen_diario': self.resumen_diario,
            'frecuencia_email': self.frecuencia_email,
            'horario_inicio': self.horario_inicio,
            'horario_fin': self.horario_fin,
            'mostrar_popup': self.mostrar_popup,
            'sonido_notificacion': self.sonido_notificacion
        }


class NotificacionProgramada(models.Model):
    """
    Modelo para notificaciones programadas para envío futuro
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones_programadas')
    
    tipo = models.CharField(
        max_length=50,
        choices=[
            ('factura', 'Factura'),
            ('proyecto', 'Proyecto'),
            ('gasto', 'Gasto'),
            ('archivo', 'Archivo'),
            ('sistema', 'Sistema'),
            ('recordatorio', 'Recordatorio'),
            ('cumpleanos', 'Cumpleaños'),
            ('evento', 'Evento')
        ]
    )
    
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    prioridad = models.CharField(
        max_length=20,
        choices=[
            ('baja', 'Baja'),
            ('normal', 'Normal'),
            ('alta', 'Alta'),
            ('urgente', 'Urgente')
        ],
        default='normal'
    )
    
    fecha_envio = models.DateTimeField(help_text="Fecha y hora programada para el envío")
    fecha_envio_real = models.DateTimeField(blank=True, null=True, help_text="Fecha y hora real del envío")
    
    estado = models.CharField(
        max_length=20,
        choices=[
            ('programada', 'Programada'),
            ('enviada', 'Enviada'),
            ('cancelada', 'Cancelada'),
            ('error', 'Error')
        ],
        default='programada'
    )
    
    # Campos opcionales para personalización
    datos_adicionales = models.JSONField(blank=True, null=True, help_text="Datos adicionales para la notificación")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Notificación Programada"
        verbose_name_plural = "Notificaciones Programadas"
        ordering = ['fecha_envio']
        indexes = [
            models.Index(fields=['estado', 'fecha_envio']),
            models.Index(fields=['usuario', 'estado']),
        ]
    
    def __str__(self):
        return f"Notificación programada para {self.usuario.username} - {self.titulo}"
    
    def esta_vencida(self):
        """Verifica si la notificación programada está vencida"""
        return timezone.now() > self.fecha_envio
    
    def puede_enviarse(self):
        """Verifica si la notificación puede ser enviada"""
        return self.estado == 'programada' and not self.esta_vencida()
    
    def cancelar(self):
        """Cancela la notificación programada"""
        self.estado = 'cancelada'
        self.save()
    
    def reprogramar(self, nueva_fecha):
        """Reprograma la notificación para una nueva fecha"""
        self.fecha_envio = nueva_fecha
        self.estado = 'programada'
        self.save()


class HistorialNotificaciones(models.Model):
    """Historial de notificaciones enviadas para auditoría"""
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    metodo_envio = models.CharField(max_length=20, choices=[
        ('sistema', 'Sistema'),
        ('email', 'Email'),
        ('push', 'Push'),
    ])
    estado = models.CharField(max_length=20, choices=[
        ('enviada', 'Enviada'),
        ('entregada', 'Entregada'),
        ('leida', 'Leída'),
        ('fallida', 'Fallida'),
    ], default='enviada')
    
    class Meta:
        ordering = ['-fecha_envio']
        verbose_name = 'Historial de Notificación'
        verbose_name_plural = 'Historial de Notificaciones'
    
    def __str__(self):
        return f"{self.tipo} - {self.usuario.username} - {self.fecha_envio}"


class CategoriaInventario(models.Model):
    """Modelo para categorías de inventario"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoría de Inventario'
        verbose_name_plural = 'Categorías de Inventario'
    
    def __str__(self):
        return self.nombre


class ItemInventario(models.Model):
    """Modelo para items del inventario"""
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(CategoriaInventario, on_delete=models.CASCADE)
    stock_actual = models.DecimalField(max_digits=10, decimal_places=2, help_text="Stock actual en unidades")
    stock_disponible = models.DecimalField(max_digits=10, decimal_places=2, help_text="Stock disponible para asignación", default=0)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, help_text="Stock mínimo recomendado", null=True, blank=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio por unidad", null=True, blank=True)
    unidad_medida = models.CharField(max_length=50, help_text="Unidad de medida (m², m³, kg, etc.)", null=True, blank=True)
    proveedor = models.CharField(max_length=200, blank=True)
    fecha_ultima_compra = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Item de Inventario'
        verbose_name_plural = 'Items de Inventario'
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo}) - {self.categoria.nombre}"
    
    def save(self, *args, **kwargs):
        # Si es un nuevo item, inicializar stock_disponible
        if not self.pk:
            self.stock_disponible = self.stock_actual
        super().save(*args, **kwargs)


class AsignacionInventario(models.Model):
    """Modelo para asignar items del inventario a proyectos"""
    item = models.ForeignKey(ItemInventario, on_delete=models.CASCADE, related_name='asignaciones')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='asignaciones_inventario')
    cantidad_asignada = models.PositiveIntegerField(default=1)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('asignado', 'Asignado'),
            ('en_uso', 'En Uso'),
            ('devuelto', 'Devuelto'),
            ('perdido', 'Perdido'),
            ('dañado', 'Dañado')
        ],
        default='asignado'
    )
    notas = models.TextField(blank=True)
    asignado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Asignación de Inventario'
        verbose_name_plural = 'Asignaciones de Inventario'
        ordering = ['-fecha_asignacion']
    
    def __str__(self):
        return f"{self.item.nombre} - {self.proyecto.nombre} ({self.cantidad_asignada})"
    
    def save(self, *args, **kwargs):
        # Actualizar stock disponible del item
        if self.pk:  # Si es una actualización
            old_instance = AsignacionInventario.objects.get(pk=self.pk)
            if old_instance.estado != self.estado:
                if self.estado == 'devuelto':
                    self.item.stock_disponible += self.cantidad_asignada
                elif old_instance.estado == 'devuelto' and self.estado != 'devuelto':
                    self.item.stock_disponible -= self.cantidad_asignada
        else:  # Si es una nueva asignación
            if self.estado != 'devuelto':
                self.item.stock_disponible -= self.cantidad_asignada
        
        self.item.save()
        super().save(*args, **kwargs)


class AnticipoProyecto(models.Model):
    """Modelo para anticipos por proyecto"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('liquidado', 'Liquidado'),
        ('procesado', 'Procesado'),
        ('cancelado', 'Cancelado'),
    ]
    
    TIPO_CHOICES = [
        ('masivo', 'Anticipo Masivo'),
        ('individual', 'Anticipo Individual'),
    ]
    
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='anticipos_proyecto')
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='anticipos_proyecto')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='individual')
    concepto = models.CharField(max_length=200, default="Anticipo por proyecto")
    fecha_anticipo = models.DateField(auto_now_add=True)
    fecha_liquidacion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True)
    liquidado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='anticipos_liquidados')
    
    class Meta:
        # Permitir múltiples anticipos por colaborador por proyecto
        # No hay restricción única para permitir flexibilidad
        ordering = ['-fecha_anticipo']
    
    def __str__(self):
        return f"Anticipo {self.colaborador.nombre} - {self.proyecto.nombre} - Q{self.monto}"
    
    @property
    def saldo_pendiente(self):
        """Retorna el saldo pendiente de liquidar"""
        if self.estado == 'pendiente':
            return self.monto
        return 0
    
    def liquidar_anticipo(self, usuario):
        """Liquida el anticipo"""
        self.estado = 'liquidado'
        self.fecha_liquidacion = timezone.now().date()
        self.liquidado_por = usuario
        self.save()


class ConfiguracionSistema(models.Model):
    """Modelo para configuraciones del sistema"""
    # Información de la Empresa
    nombre_empresa = models.CharField(max_length=200, default='Constructora XYZ')
    moneda = models.CharField(max_length=3, default='GTQ', choices=[
        ('GTQ', 'Quetzal (GTQ)'),
        ('USD', 'Dólar (USD)'),
        ('EUR', 'Euro (EUR)'),
    ])
    
    # Configuración Regional
    zona_horaria = models.CharField(max_length=50, default='America/Guatemala', choices=[
        ('America/Guatemala', 'Guatemala (GMT-6)'),
        ('America/New_York', 'Nueva York (GMT-5)'),
        ('Europe/Madrid', 'Madrid (GMT+1)'),
    ])
    idioma = models.CharField(max_length=5, default='es', choices=[
        ('es', 'Español'),
        ('en', 'English'),
    ])
    
    # Configuración del Sistema
    max_usuarios_simultaneos = models.PositiveIntegerField(default=5)
    tiempo_sesion = models.PositiveIntegerField(default=480, help_text="Tiempo en minutos")
    
    # Configuraciones Avanzadas
    respaldo_automatico = models.BooleanField(default=False)
    notificaciones_email = models.BooleanField(default=False)
    
    # Configuración de Email
    email_host = models.CharField(max_length=200, blank=True)
    email_port = models.PositiveIntegerField(default=587)
    email_username = models.CharField(max_length=200, blank=True)
    email_password = models.CharField(max_length=200, blank=True)
    email_use_tls = models.BooleanField(default=True)
    
    # Metadatos
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    actualizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Configuración del Sistema'
        verbose_name_plural = 'Configuraciones del Sistema'
    
    def __str__(self):
        return f"Configuración - {self.nombre_empresa}"
    
    @classmethod
    def get_config(cls):
        """Obtiene la configuración actual o crea una por defecto"""
        config, created = cls.objects.get_or_create(
            id=1,
            defaults={
                'nombre_empresa': 'Constructora XYZ',
                'moneda': 'GTQ',
                'zona_horaria': 'America/Guatemala',
                'idioma': 'es',
                'max_usuarios_simultaneos': 5,
                'tiempo_sesion': 480,
                'respaldo_automatico': False,
                'notificaciones_email': False,
            }
        )
        return config


class EventoCalendario(models.Model):
    """
    Modelo para eventos del calendario del dashboard
    """
    TIPO_CHOICES = [
        ('proyecto', 'Proyecto'),
        ('factura', 'Factura'),
        ('reunion', 'Reunión'),
        ('entrega', 'Entrega'),
        ('vencimiento', 'Vencimiento'),
        ('otro', 'Otro'),
    ]
    
    COLOR_CHOICES = [
        ('#667eea', 'Azul'),
        ('#28a745', 'Verde'),
        ('#dc3545', 'Rojo'),
        ('#ffc107', 'Amarillo'),
        ('#17a2b8', 'Cian'),
        ('#6f42c1', 'Púrpura'),
        ('#fd7e14', 'Naranja'),
        ('#20c997', 'Turquesa'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título del Evento")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(blank=True, null=True, verbose_name="Fecha de Fin")
    hora_inicio = models.TimeField(blank=True, null=True, verbose_name="Hora de Inicio")
    hora_fin = models.TimeField(blank=True, null=True, verbose_name="Hora de Fin")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='otro', verbose_name="Tipo de Evento")
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#667eea', verbose_name="Color")
    todo_el_dia = models.BooleanField(default=True, verbose_name="Todo el día")
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Creado por")
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name="Actualizado en")
    
    # Relaciones opcionales
    proyecto = models.ForeignKey('Proyecto', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Proyecto relacionado")
    factura = models.ForeignKey('Factura', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Factura relacionada")
    
    class Meta:
        verbose_name = 'Evento del Calendario'
        verbose_name_plural = 'Eventos del Calendario'
        ordering = ['fecha_inicio', 'hora_inicio']
    
    def __str__(self):
        return f"{self.titulo} - {self.fecha_inicio}"
    
    @property
    def fecha_completa_inicio(self):
        """Retorna la fecha y hora de inicio combinadas"""
        if self.hora_inicio:
            from django.utils import timezone
            return timezone.datetime.combine(self.fecha_inicio, self.hora_inicio)
        return self.fecha_inicio
    
    @property
    def fecha_completa_fin(self):
        """Retorna la fecha y hora de fin combinadas"""
        if self.fecha_fin and self.hora_fin:
            from django.utils import timezone
            return timezone.datetime.combine(self.fecha_fin, self.hora_fin)
        elif self.fecha_fin:
            return self.fecha_fin
        return None
    
    def to_calendar_event(self):
        """Convierte el evento a formato compatible con FullCalendar"""
        # Asegurar que las fechas sean objetos date/datetime
        if isinstance(self.fecha_inicio, str):
            from datetime import datetime
            fecha_inicio = datetime.strptime(self.fecha_inicio, '%Y-%m-%d').date()
        else:
            fecha_inicio = self.fecha_inicio
            
        if self.fecha_fin and isinstance(self.fecha_fin, str):
            from datetime import datetime
            fecha_fin = datetime.strptime(self.fecha_fin, '%Y-%m-%d').date()
        else:
            fecha_fin = self.fecha_fin
        
        event_data = {
            'id': self.id,
            'title': self.titulo,
            'start': fecha_inicio.isoformat(),
            'backgroundColor': self.color,
            'borderColor': self.color,
            'extendedProps': {
                'tipo': self.tipo,
                'descripcion': self.descripcion or '',
                'todo_el_dia': self.todo_el_dia,
                'proyecto_id': self.proyecto.id if self.proyecto else None,
                'factura_id': self.factura.id if self.factura else None,
            }
        }
        
        # Agregar fecha de fin si existe
        if fecha_fin:
            event_data['end'] = fecha_fin.isoformat()
        
        # Agregar hora si no es todo el día
        if not self.todo_el_dia and self.hora_inicio:
            event_data['start'] = f"{fecha_inicio.isoformat()}T{self.hora_inicio.isoformat()}"
            if self.hora_fin:
                event_data['end'] = f"{fecha_fin.isoformat() if fecha_fin else fecha_inicio.isoformat()}T{self.hora_fin.isoformat()}"
         
        return event_data


# ===== MODELOS PARA TRABAJADORES DIARIOS =====

class TrabajadorDiario(models.Model):
    """Modelo para trabajadores diarios de un proyecto"""
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='trabajadores_diarios', verbose_name="Proyecto")
    planilla = models.ForeignKey('PlanillaTrabajadoresDiarios', on_delete=models.CASCADE, related_name='trabajadores', null=True, blank=True, verbose_name="Planilla")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del trabajador")
    pago_diario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Pago diario (Q)")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Creado por")
    
    class Meta:
        verbose_name = 'Trabajador Diario'
        verbose_name_plural = 'Trabajadores Diarios'
        unique_together = ['planilla', 'nombre']
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.proyecto.nombre}"
    
    @property
    def total_dias_trabajados(self):
        """Calcula el total de días trabajados"""
        return self.registros_trabajo.aggregate(
            total=Sum('dias_trabajados')
        )['total'] or 0
    
    @property
    def total_a_pagar(self):
        """Calcula el total a pagar (considerando anticipos)"""
        total_bruto = self.total_dias_trabajados * self.pago_diario
        anticipos_aplicados = self.total_anticipos_aplicados
        return total_bruto - anticipos_aplicados
    
    @property
    def total_anticipos_aplicados(self):
        """Calcula el total de anticipos aplicados para este trabajador"""
        return sum(anticipo.monto_aplicado for anticipo in self.anticipos.filter(estado='aplicado'))
    
    @property
    def saldo_pendiente(self):
        """Saldo pendiente = total bruto menos anticipos aplicados (sin doble descuento)"""
        total_bruto = self.total_dias_trabajados * self.pago_diario
        return total_bruto - self.total_anticipos_aplicados


class RegistroTrabajo(models.Model):
    """Modelo para registrar los días trabajados por período"""
    trabajador = models.ForeignKey(TrabajadorDiario, on_delete=models.CASCADE, related_name='registros_trabajo', verbose_name="Trabajador")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio del período")
    fecha_fin = models.DateField(verbose_name="Fecha de fin del período")
    dias_trabajados = models.DecimalField(max_digits=5, decimal_places=1, verbose_name="Días trabajados", help_text="Número de días trabajados en este período (acepta medios días: 0.5, 1.5, etc.)")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    registrado_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Registrado por")
    
    class Meta:
        verbose_name = 'Registro de Trabajo'
        verbose_name_plural = 'Registros de Trabajo'
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.trabajador.nombre} - {self.fecha_inicio} a {self.fecha_fin}"
    
    @property
    def total_pagar(self):
        """Calcula el total a pagar"""
        return self.dias_trabajados * self.trabajador.pago_diario


class AnticipoTrabajadorDiario(models.Model):
    """Modelo para anticipos específicos de trabajadores diarios"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aplicado', 'Aplicado'),
        ('liquidado', 'Liquidado'),
        ('cancelado', 'Cancelado'),
    ]
    
    trabajador = models.ForeignKey(TrabajadorDiario, on_delete=models.CASCADE, related_name='anticipos', verbose_name="Trabajador")
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto del anticipo")
    fecha_anticipo = models.DateField(verbose_name="Fecha del anticipo", default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name="Estado")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Creado por")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = 'Anticipo de Trabajador Diario'
        verbose_name_plural = 'Anticipos de Trabajadores Diarios'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Anticipo {self.trabajador.nombre} - Q{self.monto}"
    
    @property
    def monto_aplicado(self):
        """Calcula cuánto del anticipo se ha aplicado"""
        if self.estado == 'aplicado':
            return self.monto
        return 0


class PlanillaTrabajadoresDiarios(models.Model):
    """Modelo para gestionar múltiples planillas de trabajadores diarios por proyecto"""
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('finalizada', 'Finalizada'),
        ('archivada', 'Archivada'),
    ]
    
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='planillas_trabajadores_diarios', verbose_name="Proyecto")
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la planilla", help_text="Ej: Planilla Semana 1, Planilla Enero 2025")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    fecha_inicio = models.DateField(null=True, blank=True, verbose_name="Fecha de inicio del período")
    fecha_fin = models.DateField(null=True, blank=True, verbose_name="Fecha de fin del período")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa', verbose_name="Estado")
    creada_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Creada por")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_finalizacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de finalización")
    finalizada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='planillas_finalizadas', verbose_name="Finalizada por")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    class Meta:
        verbose_name = 'Planilla de Trabajadores Diarios'
        verbose_name_plural = 'Planillas de Trabajadores Diarios'
        ordering = ['-fecha_creacion']
        unique_together = ['proyecto', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.proyecto.nombre}"
    
    @property
    def total_trabajadores(self):
        """Total de trabajadores en esta planilla"""
        return self.trabajadores.count()
    
    @property
    def total_a_pagar(self):
        """Total a pagar en esta planilla"""
        return sum(t.total_a_pagar for t in self.trabajadores.all())
    
    @property
    def total_anticipos(self):
        """Total de anticipos en esta planilla"""
        return sum(t.total_anticipos_aplicados for t in self.trabajadores.all())
    
    @property
    def saldo_pendiente(self):
        """Saldo pendiente = total bruto de la planilla menos anticipos (sin doble descuento)"""
        total_bruto = sum(
            t.total_dias_trabajados * t.pago_diario for t in self.trabajadores.all()
        )
        return total_bruto - self.total_anticipos


# ===== MÓDULO DE ASISTENCIAS =====

class Asistencia(models.Model):
    """Modelo para registrar asistencia del personal"""
    
    ESTADO_CHOICES = [
        ('presente', 'Presente'),
        ('ausente', 'Ausente'),
        ('tardanza', 'Tardanza'),
        ('permiso', 'Permiso'),
        ('vacaciones', 'Vacaciones'),
        ('feriado', 'Feriado'),
    ]
    
    TIPO_PERSONAL_CHOICES = [
        ('colaborador', 'Colaborador'),
        ('trabajador_diario', 'Trabajador Diario'),
    ]
    
    # Personal - puede ser colaborador o trabajador diario
    tipo_personal = models.CharField(max_length=20, choices=TIPO_PERSONAL_CHOICES, verbose_name="Tipo de Personal")
    colaborador = models.ForeignKey(
        'Colaborador', on_delete=models.CASCADE, null=True, blank=True,
        related_name='asistencias', verbose_name="Colaborador"
    )
    trabajador_diario = models.ForeignKey(
        'TrabajadorDiario', on_delete=models.CASCADE, null=True, blank=True,
        related_name='asistencias', verbose_name="Trabajador Diario"
    )
    
    # Proyecto al que pertenece (opcional)
    proyecto = models.ForeignKey(
        'Proyecto', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='asistencias', verbose_name="Proyecto"
    )
    
    # Datos de asistencia
    fecha = models.DateField(verbose_name="Fecha")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='presente', verbose_name="Estado")
    hora_entrada = models.TimeField(null=True, blank=True, verbose_name="Hora de Entrada")
    hora_salida_almuerzo = models.TimeField(null=True, blank=True, verbose_name="Salida a Almuerzo")
    hora_entrada_almuerzo = models.TimeField(null=True, blank=True, verbose_name="Retorno de Almuerzo")
    hora_salida = models.TimeField(null=True, blank=True, verbose_name="Hora de Salida")
    horas_laboradas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Horas Laboradas")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    # Auditoría
    registrado_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Registrado por")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    
    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['-fecha', '-fecha_registro']
    
    def __str__(self):
        nombre = self.get_nombre_personal()
        return f"{nombre} - {self.fecha} - {self.get_estado_display()}"
    
    def get_nombre_personal(self):
        """Retorna el nombre del personal según tipo"""
        if self.colaborador:
            return self.colaborador.nombre
        elif self.trabajador_diario:
            return self.trabajador_diario.nombre
        return "Sin nombre"
    
    @property
    def nombre_personal(self):
        return self.get_nombre_personal()
    
    @property
    def horas_trabajadas(self):
        """Calcula horas trabajadas descontando almuerzo si aplica"""
        if self.horas_laboradas is not None:
            return float(self.horas_laboradas)
        if self.hora_entrada and self.hora_salida:
            from datetime import datetime, date, timedelta
            hoy = date.today()
            entrada = datetime.combine(hoy, self.hora_entrada)
            salida = datetime.combine(hoy, self.hora_salida)
            total = salida - entrada
            # Descontar tiempo de almuerzo si ambos registros existen
            if self.hora_salida_almuerzo and self.hora_entrada_almuerzo:
                sal_alm = datetime.combine(hoy, self.hora_salida_almuerzo)
                ent_alm = datetime.combine(hoy, self.hora_entrada_almuerzo)
                almuerzo = ent_alm - sal_alm
                total -= almuerzo
            horas = total.total_seconds() / 3600
            return round(max(horas, 0), 2)
        return None

    @property
    def cronometraje_display(self):
        """Retorna el cronometraje formateado para mostrar"""
        h = self.horas_trabajadas
        if h is None:
            return "—"
        horas = int(h)
        minutos = int((h - horas) * 60)
        return f"{horas}h {minutos:02d}m"
    
    def get_estado_badge_class(self):
        """Retorna clase CSS para el badge del estado"""
        clases = {
            'presente': 'bg-success',
            'ausente': 'bg-danger',
            'tardanza': 'bg-warning text-dark',
            'permiso': 'bg-info',
            'vacaciones': 'bg-primary',
            'feriado': 'bg-secondary',
        }
        return clases.get(self.estado, 'bg-secondary')


class PlanillaLiquidada(models.Model):
    """Modelo para registrar planillas de personal liquidadas"""
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='planillas_liquidadas', verbose_name="Proyecto")
    fecha_liquidacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de liquidación")
    total_salarios = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total Salarios", default=0)
    total_anticipos = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total Anticipos Liquidados", default=0)
    total_planilla = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total de la Planilla", default=0)
    cantidad_personal = models.IntegerField(verbose_name="Cantidad de Personal", default=0)
    liquidada_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Liquidada por")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    class Meta:
        verbose_name = 'Planilla Liquidada'
        verbose_name_plural = 'Planillas Liquidadas'
        ordering = ['-fecha_liquidacion']
    
    def __str__(self):
        return f"Planilla {self.proyecto.nombre} - {self.fecha_liquidacion.strftime('%d/%m/%Y')} - Q{self.total_planilla}"


