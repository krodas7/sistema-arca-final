# 📋 DOCUMENTACIÓN COMPLETA: MÓDULO DE TRABAJADORES DIARIOS

## 📌 ÍNDICE
1. [Descripción General](#descripción-general)
2. [Modelos de Base de Datos](#modelos-de-base-de-datos)
3. [Formularios](#formularios)
4. [Vistas y Lógica de Negocio](#vistas-y-lógica-de-negocio)
5. [Cálculos y Propiedades](#cálculos-y-propiedades)
6. [URLs y Rutas](#urls-y-rutas)
7. [Templates HTML](#templates-html)
8. [Flujo de Trabajo Completo](#flujo-de-trabajo-completo)
9. [Casos de Uso](#casos-de-uso)
10. [Puntos Importantes](#puntos-importantes)

---

## 🎯 DESCRIPCIÓN GENERAL

El módulo de **Trabajadores Diarios** permite gestionar trabajadores temporales que se pagan por día trabajado. Incluye:

- ✅ Gestión de trabajadores por proyecto
- ✅ Sistema de planillas (permite múltiples planillas por proyecto)
- ✅ Registro de días trabajados
- ✅ Sistema de anticipos
- ✅ Cálculo automático de salarios
- ✅ Finalización de planillas con generación de PDF
- ✅ Reapertura de planillas finalizadas
- ✅ Liquidación automática

**Relación principal**: Cada trabajador pertenece a un **proyecto** y opcionalmente a una **planilla** específica.

---

## 🗄️ MODELOS DE BASE DE DATOS

### 1. **TrabajadorDiario**

```python
# core/models.py

class TrabajadorDiario(models.Model):
    """Modelo para trabajadores diarios de un proyecto"""
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, 
                                related_name='trabajadores_diarios', 
                                verbose_name="Proyecto")
    planilla = models.ForeignKey('PlanillaTrabajadoresDiarios', 
                                on_delete=models.CASCADE, 
                                related_name='trabajadores', 
                                null=True, blank=True, 
                                verbose_name="Planilla")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del trabajador")
    pago_diario = models.DecimalField(max_digits=10, decimal_places=2, 
                                     verbose_name="Pago diario (Q)")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_registro = models.DateTimeField(auto_now_add=True, 
                                         verbose_name="Fecha de registro")
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, 
                                   verbose_name="Creado por")
    
    class Meta:
        verbose_name = 'Trabajador Diario'
        verbose_name_plural = 'Trabajadores Diarios'
        unique_together = ['planilla', 'nombre']  # No puede haber 2 trabajadores con el mismo nombre en la misma planilla
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.proyecto.nombre}"
    
    # PROPIEDADES CALCULADAS (ver sección de cálculos)
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
        return sum(anticipo.monto for anticipo in self.anticipos.filter(estado='aplicado'))
    
    @property
    def saldo_pendiente(self):
        """Calcula el saldo pendiente después de aplicar anticipos"""
        return self.total_a_pagar - self.total_anticipos_aplicados
```

**Campos importantes:**
- `planilla`: Puede ser `null` (trabajador sin planilla asignada)
- `activo`: `True` = activo, `False` = archivado (se marca inactivo al finalizar planilla)
- `unique_together`: Evita duplicados por nombre dentro de la misma planilla

---

### 2. **PlanillaTrabajadoresDiarios**

```python
# core/models.py

class PlanillaTrabajadoresDiarios(models.Model):
    """Modelo para gestionar múltiples planillas de trabajadores diarios por proyecto"""
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('finalizada', 'Finalizada'),
        ('archivada', 'Archivada'),
    ]
    
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, 
                                related_name='planillas_trabajadores_diarios', 
                                verbose_name="Proyecto")
    nombre = models.CharField(max_length=200, 
                             verbose_name="Nombre de la planilla", 
                             help_text="Ej: Planilla Semana 1, Planilla Enero 2025")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    fecha_inicio = models.DateField(null=True, blank=True, 
                                    verbose_name="Fecha de inicio del período")
    fecha_fin = models.DateField(null=True, blank=True, 
                                 verbose_name="Fecha de fin del período")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, 
                             default='activa', verbose_name="Estado")
    creada_por = models.ForeignKey(User, on_delete=models.CASCADE, 
                                   verbose_name="Creada por")
    fecha_creacion = models.DateTimeField(auto_now_add=True, 
                                         verbose_name="Fecha de creación")
    fecha_finalizacion = models.DateTimeField(null=True, blank=True, 
                                             verbose_name="Fecha de finalización")
    finalizada_por = models.ForeignKey(User, on_delete=models.SET_NULL, 
                                      null=True, blank=True, 
                                      related_name='planillas_finalizadas', 
                                      verbose_name="Finalizada por")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    class Meta:
        verbose_name = 'Planilla de Trabajadores Diarios'
        verbose_name_plural = 'Planillas de Trabajadores Diarios'
        ordering = ['-fecha_creacion']
        unique_together = ['proyecto', 'nombre']  # No puede haber 2 planillas con el mismo nombre en el mismo proyecto
    
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
        """Saldo pendiente en esta planilla"""
        return self.total_a_pagar - self.total_anticipos
```

**Estados de la planilla:**
- `activa`: Planilla en uso, se pueden agregar trabajadores y modificar
- `finalizada`: Planilla completada, trabajadores archivados, se puede reabrir
- `archivada`: Planilla archivada (solo lectura)

**Reglas importantes:**
- Un proyecto puede tener **múltiples planillas**
- Máximo 2 planillas activas visibles en el selector
- Al finalizar una planilla, los trabajadores se marcan como `activo=False`

---

### 3. **AnticipoTrabajadorDiario**

```python
# core/models.py

class AnticipoTrabajadorDiario(models.Model):
    """Modelo para anticipos específicos de trabajadores diarios"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aplicado', 'Aplicado'),
        ('liquidado', 'Liquidado'),
        ('cancelado', 'Cancelado'),
    ]
    
    trabajador = models.ForeignKey(TrabajadorDiario, 
                                  on_delete=models.CASCADE, 
                                  related_name='anticipos', 
                                  verbose_name="Trabajador")
    monto = models.DecimalField(max_digits=10, decimal_places=2, 
                               verbose_name="Monto del anticipo")
    fecha_anticipo = models.DateField(verbose_name="Fecha del anticipo", 
                                     default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, 
                             default='pendiente', verbose_name="Estado")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, 
                                   verbose_name="Creado por")
    fecha_creacion = models.DateTimeField(auto_now_add=True, 
                                         verbose_name="Fecha de creación")
    
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
```

**Estados del anticipo:**
- `pendiente`: Creado pero no aplicado
- `aplicado`: Aplicado al trabajador (se descuenta del salario)
- `liquidado`: Liquidado en la planilla finalizada
- `cancelado`: Cancelado (no se aplica)

**Comportamiento:**
- Los anticipos se crean con estado `'aplicado'` automáticamente
- Se pueden crear **múltiples anticipos** para el mismo trabajador
- Al finalizar la planilla, todos los anticipos aplicados se **eliminan** (ya fueron descontados)

---

### 4. **RegistroTrabajo**

```python
# core/models.py

class RegistroTrabajo(models.Model):
    """Modelo para registrar los días trabajados por período"""
    trabajador = models.ForeignKey(TrabajadorDiario, 
                                  on_delete=models.CASCADE, 
                                  related_name='registros_trabajo', 
                                  verbose_name="Trabajador")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio del período")
    fecha_fin = models.DateField(verbose_name="Fecha de fin del período")
    dias_trabajados = models.IntegerField(verbose_name="Días trabajados", 
                                         help_text="Número de días trabajados en este período")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    fecha_registro = models.DateTimeField(auto_now_add=True, 
                                         verbose_name="Fecha de registro")
    registrado_por = models.ForeignKey(User, on_delete=models.CASCADE, 
                                      verbose_name="Registrado por")
    
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
```

**Nota importante:**
- En la implementación actual, los días trabajados se registran directamente en la lista de trabajadores (sin crear registros `RegistroTrabajo`)
- Los registros se usan para histórico, pero el cálculo de `total_dias_trabajados` se hace sumando todos los registros
- Al finalizar una planilla, **todos los registros se eliminan** (días se resetean a 0)

---

### 5. **PlanillaLiquidada**

```python
# core/models.py

class PlanillaLiquidada(models.Model):
    """Modelo para registrar planillas de personal liquidadas"""
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, 
                                related_name='planillas_liquidadas', 
                                verbose_name="Proyecto")
    fecha_liquidacion = models.DateTimeField(auto_now_add=True, 
                                            verbose_name="Fecha de liquidación")
    total_salarios = models.DecimalField(max_digits=12, decimal_places=2, 
                                        verbose_name="Total Salarios", default=0)
    total_anticipos = models.DecimalField(max_digits=12, decimal_places=2, 
                                         verbose_name="Total Anticipos Liquidados", default=0)
    total_planilla = models.DecimalField(max_digits=12, decimal_places=2, 
                                        verbose_name="Total de la Planilla", default=0)
    cantidad_personal = models.IntegerField(verbose_name="Cantidad de Personal", default=0)
    liquidada_por = models.ForeignKey(User, on_delete=models.CASCADE, 
                                     verbose_name="Liquidada por")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    class Meta:
        verbose_name = 'Planilla Liquidada'
        verbose_name_plural = 'Planillas Liquidadas'
        ordering = ['-fecha_liquidacion']
    
    def __str__(self):
        return f"Planilla {self.proyecto.nombre} - {self.fecha_liquidacion.strftime('%d/%m/%Y')} - Q{self.total_planilla}"
```

**Propósito:**
- Registro histórico de planillas finalizadas
- Usado para el dashboard del proyecto (cálculo de costos totales)
- `total_planilla` = `total_salarios` (representa el costo total, los anticipos ya están incluidos en el concepto)

---

## 📝 FORMULARIOS

### 1. **TrabajadorDiarioForm**

```python
# core/forms_simple.py

class TrabajadorDiarioForm(forms.ModelForm):
    """Formulario para trabajadores diarios"""
    
    class Meta:
        model = TrabajadorDiario
        fields = ['planilla', 'nombre', 'pago_diario', 'activo']
        widgets = {
            'planilla': forms.Select(attrs={'class': 'form-control'}),
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
            self.fields['planilla'].queryset = PlanillaTrabajadoresDiarios.objects.filter(
                proyecto=proyecto
            )
            self.fields['planilla'].empty_label = "Selecciona una planilla"
        
        # Si se pasa una planilla específica, preseleccionarla
        if self.planilla:
            self.fields['planilla'].initial = self.planilla
```

**Características:**
- Filtra planillas por proyecto
- Preselecciona planilla si se pasa como parámetro
- Campos: `planilla`, `nombre`, `pago_diario`, `activo`

---

### 2. **AnticipoTrabajadorDiarioForm**

```python
# core/forms_simple.py

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
        fields = ['trabajador', 'monto', 'fecha_anticipo', 'observaciones']
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
```

**Características:**
- Filtra trabajadores por proyecto y estado activo
- Preselecciona trabajador si se pasa `trabajador_id` en la URL
- Validación: trabajador requerido, monto > 0

---

### 3. **PlanillaTrabajadoresDiariosForm**

```python
# core/forms_simple.py

class PlanillaTrabajadoresDiariosForm(forms.ModelForm):
    """Formulario para crear/editar planillas de trabajadores diarios"""
    
    class Meta:
        model = PlanillaTrabajadoresDiarios
        fields = ['nombre', 'descripcion', 'observaciones']
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
```

**Características:**
- Solo campos básicos: `nombre`, `descripcion`, `observaciones`
- El proyecto se asigna en la vista

---

## 🎯 VISTAS Y LÓGICA DE NEGOCIO

### 1. **Lista de Trabajadores Diarios**

```python
# core/views.py

@login_required
def trabajadores_diarios_list(request, proyecto_id):
    """Lista de trabajadores diarios de un proyecto"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    # IMPORTANTE: Obtener SOLO las planillas ACTIVAS para el selector (máximo 2)
    planillas_activas = PlanillaTrabajadoresDiarios.objects.filter(
        proyecto=proyecto,
        estado__in=['activa', 'pendiente']
    ).order_by('-fecha_creacion').distinct()[:2]
    
    # Obtener todas las planillas para histórico
    planillas_todas = PlanillaTrabajadoresDiarios.objects.filter(
        proyecto=proyecto
    ).order_by('-fecha_creacion')
    
    # Obtener planilla seleccionada desde la URL
    planilla_id = request.GET.get('planilla_id')
    planilla_seleccionada = None
    if planilla_id:
        try:
            planilla_seleccionada = PlanillaTrabajadoresDiarios.objects.get(
                id=planilla_id, 
                proyecto=proyecto
            )
        except PlanillaTrabajadoresDiarios.DoesNotExist:
            pass
    
    # Si no hay planilla seleccionada, usar la primera activa
    if not planilla_seleccionada:
        planilla_seleccionada = planillas_activas.first()
    
    # Filtrar trabajadores por planilla seleccionada
    if planilla_seleccionada:
        if planilla_seleccionada.estado == 'finalizada':
            # Si está finalizada, mostrar trabajadores archivados (para historial)
            trabajadores = TrabajadorDiario.objects.filter(
                proyecto=proyecto, 
                planilla=planilla_seleccionada
            ).order_by('nombre')
        else:
            # Si está activa, mostrar solo trabajadores activos
            trabajadores = TrabajadorDiario.objects.filter(
                proyecto=proyecto, 
                planilla=planilla_seleccionada, 
                activo=True
            ).order_by('nombre')
    else:
        # Mostrar trabajadores sin planilla asignada
        trabajadores = TrabajadorDiario.objects.filter(
            proyecto=proyecto, 
            planilla__isnull=True, 
            activo=True
        ).order_by('nombre')
    
    # Calcular anticipos aplicados para cada trabajador
    for trabajador in trabajadores:
        anticipos_qs = AnticipoTrabajadorDiario.objects.filter(
            trabajador=trabajador,
            estado='aplicado'
        )
        total_anticipos = sum(anticipo.monto for anticipo in anticipos_qs)
        trabajador.anticipos_monto = Decimal(str(total_anticipos))
        trabajador.anticipos_count = anticipos_qs.count()
    
    # Calcular totales generales
    total_bruto_general = sum(t.total_dias_trabajados * t.pago_diario for t in trabajadores)
    total_anticipos_general = sum(t.anticipos_monto for t in trabajadores)
    total_neto_general = total_bruto_general - total_anticipos_general
    
    context = {
        'proyecto': proyecto,
        'trabajadores': trabajadores,
        'planillas_activas': planillas_activas,
        'planillas_todas': planillas_todas,
        'planilla_seleccionada': planilla_seleccionada,
        'total_bruto_general': total_bruto_general,
        'total_anticipos_general': total_anticipos_general,
        'total_neto_general': total_neto_general,
    }
    
    return render(request, 'core/trabajadores_diarios/list.html', context)
```

**Puntos clave:**
- Solo muestra **2 planillas activas** en el selector
- Los trabajadores se filtran por planilla seleccionada
- Calcula anticipos aplicados en tiempo real
- Muestra totales: bruto, anticipos, neto

---

### 2. **Crear Trabajador Diario**

```python
# core/views.py

@login_required
def trabajador_diario_create(request, proyecto_id):
    """Crear trabajador diario"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    # Obtener planilla_id de la URL si existe
    planilla_id = request.GET.get('planilla_id')
    planilla_seleccionada = None
    if planilla_id:
        try:
            planilla_seleccionada = PlanillaTrabajadoresDiarios.objects.get(
                id=planilla_id, 
                proyecto=proyecto
            )
        except PlanillaTrabajadoresDiarios.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = TrabajadorDiarioForm(
            request.POST, 
            planilla=planilla_seleccionada, 
            proyecto=proyecto
        )
        if form.is_valid():
            # Validar que no exista el mismo nombre en otras planillas ACTIVAS
            nombre_trabajador = form.cleaned_data.get('nombre')
            trabajadores_duplicados = TrabajadorDiario.objects.filter(
                proyecto=proyecto,
                nombre__iexact=nombre_trabajador,
                activo=True,
                planilla__estado__in=['activa', 'pendiente']
            ).exclude(planilla=planilla_seleccionada)
            
            if trabajadores_duplicados.exists():
                planilla_duplicada = trabajadores_duplicados.first().planilla
                messages.error(
                    request,
                    f'❌ El trabajador "{nombre_trabajador}" ya existe en la planilla activa "{planilla_duplicada.nombre}". '
                    f'No se permiten trabajadores duplicados entre planillas activas.'
                )
            else:
                trabajador = form.save(commit=False)
                trabajador.proyecto = proyecto
                trabajador.planilla = planilla_seleccionada
                trabajador.creado_por = request.user
                trabajador.save()
                
                messages.success(request, 
                    f'✅ Trabajador "{nombre_trabajador}" agregado a la planilla "{planilla_seleccionada.nombre}".'
                )
                if planilla_id:
                    return redirect(
                        f'{reverse("trabajadores_diarios_list", args=[proyecto_id])}?planilla_id={planilla_id}'
                    )
                return redirect('trabajadores_diarios_list', proyecto_id=proyecto_id)
    else:
        form = TrabajadorDiarioForm(planilla=planilla_seleccionada, proyecto=proyecto)
    
    return render(request, 'core/trabajadores_diarios/create.html', {
        'form': form,
        'proyecto': proyecto
    })
```

**Validaciones:**
- No permite trabajadores duplicados en planillas activas
- Asigna automáticamente la planilla si viene en la URL
- Redirige manteniendo el `planilla_id` en la URL

---

### 3. **Editar Trabajador Diario**

```python
# core/views.py

@login_required
def trabajador_diario_edit(request, proyecto_id, trabajador_id):
    """Editar trabajador diario"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    trabajador = get_object_or_404(TrabajadorDiario, id=trabajador_id, proyecto=proyecto)
    
    planilla_id = request.GET.get('planilla_id')
    
    # IMPORTANTE: Preservar la planilla original
    planilla_original = trabajador.planilla
    
    if request.method == 'POST':
        form = TrabajadorDiarioForm(request.POST, instance=trabajador)
        if form.is_valid():
            trabajador_editado = form.save(commit=False)
            trabajador_editado.proyecto = proyecto
            
            # Preservar la planilla original (no debe cambiar)
            if planilla_original:
                trabajador_editado.planilla = planilla_original
            elif trabajador.planilla:
                trabajador_editado.planilla = trabajador.planilla
            
            trabajador_editado.save()
            
            messages.success(request, 
                f'✅ Trabajador "{trabajador_editado.nombre}" actualizado correctamente.'
            )
            
            planilla_redirect = planilla_id or (planilla_original.id if planilla_original else None)
            if planilla_redirect:
                return redirect(
                    f'{reverse("trabajadores_diarios_list", args=[proyecto_id])}?planilla_id={planilla_redirect}'
                )
            return redirect('trabajadores_diarios_list', proyecto_id=proyecto_id)
    else:
        form = TrabajadorDiarioForm(instance=trabajador)
    
    return render(request, 'core/trabajadores_diarios/edit.html', {
        'form': form,
        'proyecto': proyecto,
        'trabajador': trabajador,
        'planilla_id': planilla_id or (planilla_original.id if planilla_original else None)
    })
```

**Punto crítico:**
- **Preserva la planilla original** al editar (no permite cambiarla)
- Esto evita que trabajadores se muevan accidentalmente entre planillas

---

### 4. **Crear Anticipo**

```python
# core/views.py

@login_required
def anticipo_trabajador_diario_create(request, proyecto_id):
    """Crear anticipo de trabajador diario"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    planilla_id = request.GET.get('planilla_id') or request.POST.get('planilla_id')
    trabajador_id = request.GET.get('trabajador_id') or request.POST.get('trabajador_id')
    
    planilla_seleccionada = None
    if planilla_id:
        try:
            planilla_seleccionada = PlanillaTrabajadoresDiarios.objects.get(
                id=planilla_id, 
                proyecto=proyecto
            )
        except PlanillaTrabajadoresDiarios.DoesNotExist:
            planilla_seleccionada = None
    
    if request.method == 'POST':
        form = AnticipoTrabajadorDiarioForm(
            request.POST, 
            proyecto_id=proyecto_id,
            trabajador_id=trabajador_id
        )
        
        # Filtrar trabajadores por planilla seleccionada
        if planilla_seleccionada:
            form.fields['trabajador'].queryset = TrabajadorDiario.objects.filter(
                proyecto=proyecto,
                planilla=planilla_seleccionada,
                activo=True
            ).order_by('nombre')
        
        if form.is_valid():
            trabajador_seleccionado = form.cleaned_data.get('trabajador')
            monto_ingresado = form.cleaned_data.get('monto')
            
            # Crear el anticipo
            anticipo = form.save(commit=False)
            anticipo.creado_por = request.user
            # Los anticipos se aplican directamente (estado='aplicado')
            anticipo.estado = 'aplicado'
            anticipo.save()
            
            messages.success(request, 
                f'✅ Anticipo creado y aplicado exitosamente<br>'
                f'👤 Trabajador: <strong>{anticipo.trabajador.nombre}</strong><br>'
                f'💰 Monto: <strong>Q{anticipo.monto:,.2f}</strong>',
                extra_tags='html'
            )
            
            if planilla_id:
                return redirect(
                    f'{reverse("anticipo_trabajador_diario_list", args=[proyecto_id])}?planilla_id={planilla_id}'
                )
            return redirect('anticipo_trabajador_diario_list', proyecto_id=proyecto_id)
    else:
        form = AnticipoTrabajadorDiarioForm(
            proyecto_id=proyecto_id,
            trabajador_id=trabajador_id
        )
        
        # Filtrar trabajadores por planilla seleccionada
        if planilla_seleccionada:
            form.fields['trabajador'].queryset = TrabajadorDiario.objects.filter(
                proyecto=proyecto,
                planilla=planilla_seleccionada,
                activo=True
            ).order_by('nombre')
    
    return render(request, 'core/anticipos_trabajadores_diarios/create.html', {
        'form': form,
        'proyecto': proyecto,
        'planilla_seleccionada': planilla_seleccionada,
        'trabajador_id': trabajador_id
    })
```

**Características:**
- Preselecciona trabajador si viene `trabajador_id` en la URL
- Filtra trabajadores por planilla seleccionada
- Los anticipos se crean con estado `'aplicado'` automáticamente
- Se pueden crear **múltiples anticipos** para el mismo trabajador

---

### 5. **Actualizar Días Trabajados (AJAX)**

```python
# core/views.py

@login_required
def actualizar_dias_trabajados(request, proyecto_id, trabajador_id):
    """Actualizar días trabajados de un trabajador (AJAX)"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})
    
    trabajador = get_object_or_404(TrabajadorDiario, id=trabajador_id, proyecto_id=proyecto_id)
    
    try:
        dias_trabajados = int(request.POST.get('dias_trabajados', 0))
        
        if dias_trabajados < 0:
            return JsonResponse({'success': False, 'error': 'Los días no pueden ser negativos'})
        
        # Actualizar o crear registro de trabajo
        registro, created = RegistroTrabajo.objects.get_or_create(
            trabajador=trabajador,
            defaults={
                'fecha_inicio': timezone.now().date(),
                'fecha_fin': timezone.now().date(),
                'dias_trabajados': dias_trabajados,
                'registrado_por': request.user
            }
        )
        
        if not created:
            registro.dias_trabajados = dias_trabajados
            registro.fecha_fin = timezone.now().date()
            registro.save()
        
        # Calcular totales
        total_bruto = trabajador.total_dias_trabajados * trabajador.pago_diario
        total_anticipos = trabajador.total_anticipos_aplicados
        total_neto = total_bruto - total_anticipos
        
        return JsonResponse({
            'success': True,
            'total_bruto': float(total_bruto),
            'total_anticipos': float(total_anticipos),
            'total_neto': float(total_neto),
            'dias_trabajados': trabajador.total_dias_trabajados
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
```

**Funcionamiento:**
- Recibe días trabajados vía AJAX desde el template
- Crea o actualiza un `RegistroTrabajo`
- Retorna totales calculados en JSON

---

### 6. **Finalizar Planilla**

```python
# core/views.py

@login_required
def finalizar_planilla_trabajadores(request, proyecto_id):
    """Finalizar planilla de trabajadores diarios"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    planilla_id = request.POST.get('planilla_id')
    planilla = get_object_or_404(PlanillaTrabajadoresDiarios, id=planilla_id, proyecto=proyecto)
    
    # Obtener trabajadores de la planilla
    trabajadores = TrabajadorDiario.objects.filter(planilla=planilla)
    
    # Calcular totales
    total_bruto_general = Decimal('0.00')
    total_anticipos_general = Decimal('0.00')
    
    for trabajador in trabajadores:
        dias = trabajador.total_dias_trabajados
        pago_diario = trabajador.pago_diario
        total_bruto = Decimal(str(dias)) * Decimal(str(pago_diario))
        total_bruto_general += total_bruto
        
        anticipos_qs = AnticipoTrabajadorDiario.objects.filter(
            trabajador=trabajador,
            estado='aplicado'
        )
        total_anticipos = sum(anticipo.monto for anticipo in anticipos_qs)
        total_anticipos_general += Decimal(str(total_anticipos))
    
    total_neto_general = total_bruto_general - total_anticipos_general
    
    # 1. Generar PDF de la planilla
    # (código para generar PDF usando reportlab o similar)
    
    # 2. Guardar PDF en ArchivoProyecto
    # (código para guardar archivo)
    
    # 3. Crear registro de PlanillaLiquidada
    planilla_liquidada = PlanillaLiquidada.objects.create(
        proyecto=proyecto,
        total_salarios=total_bruto_general,
        total_anticipos=total_anticipos_general,
        total_planilla=total_bruto_general,  # Usar total bruto para dashboard
        cantidad_personal=trabajadores.count(),
        liquidada_por=request.user,
        observaciones=f'Planilla finalizada - Total Bruto: Q{total_bruto_general:.2f}, Anticipos: Q{total_anticipos_general:.2f}, Neto: Q{total_neto_general:.2f}'
    )
    
    # 4. Eliminar anticipos aplicados
    AnticipoTrabajadorDiario.objects.filter(
        trabajador__in=trabajadores,
        estado='aplicado'
    ).delete()
    
    # 5. Eliminar registros de días trabajados (resetear a 0)
    RegistroTrabajo.objects.filter(trabajador__in=trabajadores).delete()
    
    # 6. Marcar planilla como 'finalizada'
    planilla.estado = 'finalizada'
    planilla.fecha_finalizacion = timezone.now()
    planilla.finalizada_por = request.user
    planilla.save()
    
    # 7. Marcar trabajadores como inactivos (archivados)
    trabajadores.update(activo=False)
    
    messages.success(request, 
        f'✅ Planilla "{planilla.nombre}" finalizada exitosamente. '
        f'PDF guardado con {trabajadores.count()} trabajadores.'
    )
    
    return redirect('trabajadores_diarios_list', proyecto_id=proyecto_id)
```

**Proceso de finalización:**
1. ✅ Calcula totales (bruto, anticipos, neto)
2. ✅ Genera PDF de la planilla
3. ✅ Guarda PDF en `ArchivoProyecto`
4. ✅ Crea registro en `PlanillaLiquidada`
5. ✅ **Elimina** todos los anticipos aplicados
6. ✅ **Elimina** todos los registros de días trabajados
7. ✅ Marca planilla como `'finalizada'`
8. ✅ Marca trabajadores como `activo=False` (archivados)

**IMPORTANTE:** Los anticipos y registros se eliminan porque ya fueron liquidados. La planilla queda como registro histórico.

---

### 7. **Reabrir Planilla**

```python
# core/views.py

@login_required
def reabrir_planilla_trabajadores(request, proyecto_id, planilla_id):
    """Reabrir una planilla finalizada para continuar editando"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    planilla = get_object_or_404(PlanillaTrabajadoresDiarios, id=planilla_id, proyecto=proyecto)
    
    if request.method != 'POST':
        messages.error(request, 'Método no permitido.')
        return redirect(f'{reverse("trabajadores_diarios_list", args=[proyecto_id])}?planilla_id={planilla.id}')
    
    if planilla.estado != 'finalizada':
        messages.info(request, f'La planilla "{planilla.nombre}" ya está activa.')
        return redirect(f'{reverse("trabajadores_diarios_list", args=[proyecto_id])}?planilla_id={planilla.id}')
    
    # Reabrir planilla
    planilla.estado = 'activa'
    planilla.fecha_finalizacion = None
    planilla.finalizada_por = None
    planilla.save()
    
    # Reactivar trabajadores
    trabajadores_reactivados = planilla.trabajadores.update(activo=True)
    
    LogActividad.objects.create(
        usuario=request.user,
        accion='Reabrir Planilla',
        modulo='Trabajadores Diarios',
        descripcion=f'Planilla "{planilla.nombre}" reabierta. Trabajadores reactivados: {trabajadores_reactivados}',
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    messages.success(request, 
        f'✅ Planilla "{planilla.nombre}" reabierta. Puedes continuar editando y registrando días.'
    )
    
    return redirect(f'{reverse("trabajadores_diarios_list", args=[proyecto_id])}?planilla_id={planilla.id}')
```

**Funcionalidad:**
- Solo funciona con planillas `'finalizada'`
- Cambia estado a `'activa'`
- Reactiva todos los trabajadores (`activo=True`)
- Permite continuar editando días y agregar anticipos

---

## 🧮 CÁLCULOS Y PROPIEDADES

### Cálculo de Días Trabajados

```python
@property
def total_dias_trabajados(self):
    """Suma todos los registros de trabajo"""
    return self.registros_trabajo.aggregate(
        total=Sum('dias_trabajados')
    )['total'] or 0
```

**En la práctica:**
- En la lista, los días se actualizan vía AJAX creando/actualizando `RegistroTrabajo`
- Cada trabajador puede tener múltiples registros
- La suma de todos los registros = días totales trabajados

---

### Cálculo de Anticipos Aplicados

```python
@property
def total_anticipos_aplicados(self):
    """Suma todos los anticipos con estado='aplicado'"""
    anticipos_qs = AnticipoTrabajadorDiario.objects.filter(
        trabajador=self,
        estado='aplicado'
    )
    return sum(anticipo.monto for anticipo in anticipos_qs)
```

**Lógica:**
- Solo cuenta anticipos con `estado='aplicado'`
- Se puede crear múltiples anticipos para el mismo trabajador
- Todos se suman para calcular el total descontado

---

### Cálculo de Total a Pagar

```python
@property
def total_a_pagar(self):
    """Total a pagar = (días × pago_diario) - anticipos"""
    total_bruto = self.total_dias_trabajados * self.pago_diario
    anticipos_aplicados = self.total_anticipos_aplicados
    return total_bruto - anticipos_aplicados
```

**Fórmula:**
```
Total a Pagar = (Días Trabajados × Pago Diario) - Total Anticipos Aplicados
```

**Ejemplo:**
- Días trabajados: 15
- Pago diario: Q100.00
- Anticipos aplicados: Q300.00
- **Total bruto**: 15 × Q100 = Q1,500.00
- **Total a pagar**: Q1,500 - Q300 = Q1,200.00

---

### Totales de la Planilla

```python
@property
def total_a_pagar(self):
    """Suma de todos los totales a pagar de los trabajadores"""
    return sum(t.total_a_pagar for t in self.trabajadores.all())

@property
def total_anticipos(self):
    """Suma de todos los anticipos de los trabajadores"""
    return sum(t.total_anticipos_aplicados for t in self.trabajadores.all())

@property
def saldo_pendiente(self):
    """Saldo pendiente después de anticipos"""
    return self.total_a_pagar - self.total_anticipos
```

**En la vista:**
```python
total_bruto_general = sum(
    t.total_dias_trabajados * t.pago_diario 
    for t in trabajadores
)
total_anticipos_general = sum(
    t.anticipos_monto 
    for t in trabajadores
)
total_neto_general = total_bruto_general - total_anticipos_general
```

---

## 🔗 URLS Y RUTAS

### URLs Principales

```python
# core/urls.py

# Dashboard de trabajadores diarios
path('trabajadores-diarios/', views.trabajadores_diarios_dashboard, 
     name='trabajadores_diarios_dashboard'),

# Gestor de planillas
path('trabajadores-diarios/gestor-planillas/', 
     views.planillas_trabajadores_diarios_gestor, 
     name='planillas_trabajadores_diarios_gestor'),

# Lista de trabajadores por proyecto
path('proyectos/<int:proyecto_id>/trabajadores-diarios/', 
     views.trabajadores_diarios_list, 
     name='trabajadores_diarios_list'),

# Crear trabajador
path('proyectos/<int:proyecto_id>/trabajadores-diarios/crear/', 
     views.trabajador_diario_create, 
     name='trabajador_diario_create'),

# Editar trabajador
path('proyectos/<int:proyecto_id>/trabajadores-diarios/<int:trabajador_id>/editar/', 
     views.trabajador_diario_edit, 
     name='trabajador_diario_edit'),

# Actualizar días trabajados (AJAX)
path('proyectos/<int:proyecto_id>/trabajadores-diarios/<int:trabajador_id>/actualizar-dias/', 
     views.actualizar_dias_trabajados, 
     name='actualizar_dias_trabajados'),

# Finalizar planilla
path('proyectos/<int:proyecto_id>/trabajadores-diarios/finalizar/', 
     views.finalizar_planilla_trabajadores, 
     name='finalizar_planilla_trabajadores'),

# Reabrir planilla
path('proyectos/<int:proyecto_id>/trabajadores-diarios/planilla/<int:planilla_id>/reabrir/', 
     views.reabrir_planilla_trabajadores, 
     name='reabrir_planilla_trabajadores'),

# Crear anticipo
path('proyectos/<int:proyecto_id>/anticipos-trabajadores-diarios/crear/', 
     views.anticipo_trabajador_diario_create, 
     name='anticipo_trabajador_diario_create'),

# Lista de anticipos
path('proyectos/<int:proyecto_id>/anticipos-trabajadores-diarios/', 
     views.anticipo_trabajador_diario_list, 
     name='anticipo_trabajador_diario_list'),
```

**Parámetros de URL importantes:**
- `?planilla_id=X`: Filtra por planilla específica
- `?trabajador_id=X`: Preselecciona trabajador en formularios

---

## 🎨 TEMPLATES HTML

### 1. **Lista de Trabajadores (`list.html`)**

**Características principales:**
- Selector de planillas activas (máximo 2)
- Tabla de trabajadores con:
  - Nombre
  - Pago diario
  - Días trabajados (input editable)
  - Anticipos aplicados
  - Total bruto
  - Total a pagar
- Botones de acción:
  - Agregar anticipo (+)
  - Editar trabajador
  - Eliminar trabajador
- Totales generales al final
- Botón "Finalizar Planilla"

**Código JavaScript para actualizar días:**

```javascript
// Actualizar días trabajados vía AJAX
document.querySelectorAll('.input-days').forEach(input => {
    input.addEventListener('change', function() {
        const trabajadorId = this.dataset.trabajadorId;
        const dias = parseInt(this.value) || 0;
        
        fetch(`/proyectos/${proyectoId}/trabajadores-diarios/${trabajadorId}/actualizar-dias/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: `dias_trabajados=${dias}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Actualizar totales en la fila
                actualizarTotalesFila(trabajadorId, data);
                // Recalcular totales generales
                recalcularTotalesGenerales();
            }
        });
    });
});
```

---

### 2. **Crear Trabajador (`create.html`)**

**Elementos:**
- Formulario con campos: `planilla`, `nombre`, `pago_diario`, `activo`
- La planilla se preselecciona si viene `?planilla_id=X`
- Validación en el cliente y servidor

---

### 3. **Crear Anticipo (`anticipos_trabajadores_diarios/create.html`)**

**Elementos:**
- Formulario con: `trabajador` (preseleccionado si viene `?trabajador_id=X`), `monto`, `fecha_anticipo`, `observaciones`
- Filtrado de trabajadores por planilla seleccionada
- Validación: monto > 0, trabajador requerido

---

### 4. **Gestor de Planillas (`gestor_planillas.html`)**

**Elementos:**
- Lista de todas las planillas del sistema
- Filtros por estado y proyecto
- Botones:
  - Ver trabajadores
  - Editar planilla
  - **Reabrir** (si está finalizada)
  - Eliminar (si no está finalizada)
- Estadísticas: total planillas, activas, finalizadas

---

## 🔄 FLUJO DE TRABAJO COMPLETO

### Flujo 1: Crear Planilla y Agregar Trabajadores

1. **Crear Planilla:**
   - Ir a "Gestor de Planillas"
   - Click en "Crear Planilla"
   - Ingresar nombre (ej: "Planilla Semana 1")
   - Seleccionar proyecto
   - Guardar

2. **Agregar Trabajadores:**
   - Ir a "Trabajadores Diarios" del proyecto
   - Seleccionar la planilla en el selector
   - Click en "Agregar Trabajador"
   - Ingresar nombre y pago diario
   - Guardar

3. **Registrar Días Trabajados:**
   - En la lista, editar el campo "Días Trabajados"
   - El sistema calcula automáticamente: `Total Bruto = Días × Pago Diario`

4. **Agregar Anticipos (opcional):**
   - Click en el botón "+" junto al trabajador
   - Ingresar monto del anticipo
   - Guardar (se aplica automáticamente)
   - El sistema calcula: `Total a Pagar = Total Bruto - Anticipos`

5. **Finalizar Planilla:**
   - Verificar totales
   - Click en "Finalizar Planilla"
   - El sistema:
     - Genera PDF
     - Guarda PDF en archivos del proyecto
     - Crea registro en `PlanillaLiquidada`
     - Elimina anticipos aplicados
     - Elimina registros de días
     - Marca trabajadores como inactivos
     - Marca planilla como finalizada

6. **Reabrir Planilla (si es necesario):**
   - Ir a "Gestor de Planillas"
   - Click en "Reabrir" en la planilla finalizada
   - Los trabajadores se reactivan
   - Se puede continuar editando

---

### Flujo 2: Trabajo con Múltiples Planillas

1. **Proyecto tiene 2 planillas activas:**
   - "Planilla Semana 1"
   - "Planilla Semana 2"

2. **En el selector solo aparecen las 2 activas**
3. **Cada planilla tiene sus propios trabajadores**
4. **No se permiten trabajadores duplicados entre planillas activas**
5. **Al finalizar una planilla, desaparece del selector (queda solo la otra activa)**
6. **Se puede crear una nueva planilla para continuar el ciclo**

---

## 💡 CASOS DE USO

### Caso 1: Trabajador con Múltiples Anticipos

**Escenario:**
- Trabajador: Juan Pérez
- Pago diario: Q100.00
- Días trabajados: 20
- Anticipos:
  - Anticipo 1: Q200.00
  - Anticipo 2: Q300.00
  - Anticipo 3: Q100.00

**Cálculos:**
- Total bruto: 20 × Q100 = Q2,000.00
- Total anticipos: Q200 + Q300 + Q100 = Q600.00
- **Total a pagar: Q2,000 - Q600 = Q1,400.00**

**Implementación:**
- Se pueden crear múltiples anticipos desde la lista de anticipos
- Cada anticipo se suma automáticamente
- El total a pagar se recalcula en tiempo real

---

### Caso 2: Finalizar y Reabrir Planilla

**Escenario:**
- Planilla "Semana 1" finalizada
- Se necesita agregar un trabajador más o corregir días

**Solución:**
1. Ir a "Gestor de Planillas"
2. Buscar planilla "Semana 1"
3. Click en "Reabrir"
4. Los trabajadores se reactivan
5. Se puede editar días y agregar trabajadores
6. Al finalizar nuevamente, se genera un nuevo PDF

**Nota:** Los anticipos y registros de días se eliminan al finalizar, así que al reabrir empezará desde cero.

---

### Caso 3: Proyecto con 2 Planillas Activas

**Escenario:**
- Proyecto "Construcción Edificio A"
- Planilla "Quincenal" (15 días)
- Planilla "Mensual" (30 días)

**Reglas:**
- Solo aparecen 2 planillas activas en el selector
- No se permite duplicar trabajadores entre planillas activas
- Cada planilla se gestiona independientemente
- Al finalizar una, queda espacio para crear otra

---

## ⚠️ PUNTOS IMPORTANTES

### 1. **Preservación de Planilla al Editar**

**Problema:** Si se permite cambiar la planilla al editar, un trabajador podría moverse accidentalmente entre planillas.

**Solución:** La vista `trabajador_diario_edit` **preserva la planilla original** y no permite cambiarla.

```python
planilla_original = trabajador.planilla
# ... editar otros campos ...
trabajador_editado.planilla = planilla_original  # Preservar
```

---

### 2. **Selector de Planillas (Máximo 2 Activas)**

**Problema:** Si hay muchas planillas activas, el selector se vuelve confuso.

**Solución:** Solo se muestran las **2 planillas más recientes** con estado `'activa'` o `'pendiente'`.

```python
planillas_activas = PlanillaTrabajadoresDiarios.objects.filter(
    proyecto=proyecto,
    estado__in=['activa', 'pendiente']
).order_by('-fecha_creacion').distinct()[:2]
```

---

### 3. **Eliminación de Anticipos al Finalizar**

**Problema:** Si no se eliminan, los anticipos se acumulan indefinidamente.

**Solución:** Al finalizar la planilla, **todos los anticipos aplicados se eliminan** (ya fueron descontados del salario).

```python
AnticipoTrabajadorDiario.objects.filter(
    trabajador__in=trabajadores,
    estado='aplicado'
).delete()
```

---

### 4. **Cálculo de Totales en Tiempo Real**

**Problema:** Los totales deben actualizarse cuando se cambian los días trabajados.

**Solución:** Se usa **AJAX** para actualizar días sin recargar la página.

```javascript
// Actualizar días vía AJAX
fetch('/actualizar-dias/', {
    method: 'POST',
    body: `dias_trabajados=${dias}`
})
.then(response => response.json())
.then(data => {
    // Actualizar totales en la interfaz
    actualizarTotales(data);
});
```

---

### 5. **Validación de Duplicados**

**Problema:** Un trabajador no debería aparecer en múltiples planillas activas al mismo tiempo.

**Solución:** Validación en la vista de crear trabajador:

```python
trabajadores_duplicados = TrabajadorDiario.objects.filter(
    proyecto=proyecto,
    nombre__iexact=nombre_trabajador,
    activo=True,
    planilla__estado__in=['activa', 'pendiente']
).exclude(planilla=planilla_seleccionada)

if trabajadores_duplicados.exists():
    # Mostrar error
```

---

### 6. **Uso de Decimal para Cálculos Financieros**

**Problema:** `float` puede causar errores de precisión en cálculos financieros.

**Solución:** Usar `Decimal` para todos los cálculos:

```python
from decimal import Decimal

total_bruto = Decimal(str(dias)) * Decimal(str(pago_diario))
```

---

### 7. **Estado de Trabajadores al Finalizar**

**Problema:** ¿Qué hacer con los trabajadores al finalizar una planilla?

**Solución:**
- Marcar como `activo=False` (archivados)
- Permanecen asociados a la planilla finalizada
- No aparecen en listas de trabajadores activos
- Se pueden reactivar al reabrir la planilla

```python
trabajadores.update(activo=False)  # Al finalizar
planilla.trabajadores.update(activo=True)  # Al reabrir
```

---

## 📚 DEPENDENCIAS NECESARIAS

### Modelos Requeridos (de otros módulos)

- `Proyecto`: Cada trabajador pertenece a un proyecto
- `User`: Para tracking de creado_por, liquidada_por, etc.
- `ArchivoProyecto`: Para guardar PDFs de planillas finalizadas
- `LogActividad`: Para registrar acciones del sistema

### Paquetes Python

```python
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q
from decimal import Decimal
from django.utils import timezone
```

### Templates Base

- Base template con menú de navegación
- Bootstrap para estilos
- Font Awesome para iconos
- JavaScript para AJAX

---

## 🎯 RESUMEN DE CONCEPTOS CLAVE

1. **Planillas:** Permiten organizar trabajadores por períodos (semanal, quincenal, mensual)
2. **Anticipos:** Se aplican automáticamente y se descuentan del salario
3. **Finalización:** Genera PDF, elimina anticipos y registros, archiva trabajadores
4. **Reapertura:** Permite reactivar planillas finalizadas para continuar editando
5. **Cálculos:** Usar `Decimal` para precisión financiera
6. **Validaciones:** No permitir duplicados en planillas activas
7. **Preservación:** No cambiar planilla al editar trabajador

---

## 📝 NOTAS FINALES

- El módulo está diseñado para **proyectos de construcción** con trabajadores temporales
- Los trabajadores se pagan por **día trabajado**, no por horas
- Las planillas se pueden **reabrir** si es necesario corregir o agregar trabajadores
- Los anticipos se **eliminan** al finalizar (ya fueron descontados)
- Los días trabajados se **resetean** al finalizar (para el próximo ciclo)

---

**Fecha de creación:** Noviembre 2025
**Versión:** 1.0
**Autor:** Sistema ARCA

