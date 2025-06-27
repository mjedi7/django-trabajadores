from django.db import models

class Planilla(models.Model):
    no = models.BigAutoField(primary_key=True)
    nombre = models.TextField(blank=True, null=True)
    adscripcion = models.TextField(blank=True, null=True)
    departamento = models.TextField(blank=True, null=True)
    clave = models.TextField(blank=True, null=True)
    rfc = models.TextField(blank=True, null=True)
    curp = models.TextField(blank=True, null=True)
    puesto = models.TextField(blank=True, null=True)
    sindicato = models.TextField(blank=True, null=True)  # ← AGREGA ESTA LÍNEA
    fecha_de_ingreso = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # primero guarda y que la BD asigne el no
        if self.no is None:
            raise ValueError("El campo 'no' no puede ser None")    

    class Meta:
        db_table = 'planilla'  # Le indica a Django que use la tabla 'planilla'

class Adscripcion(models.Model):
    nombre = models.CharField(max_length=100)
    clave_adscripcion = models.CharField(max_length=20, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)
    zona = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    activo = models.CharField(max_length=100, default='1')  # o el valor que prefieras
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'adscripcion'  # Esta apunta a tabla 'adscripcion'

class Plazas(models.Model):
    codigo = models.CharField(max_length=20)
    denominacion = models.CharField(max_length=255)
    zona_economica = models.CharField(max_length=10)
    nivel_salarial = models.CharField(max_length=10)
    plazas = models.IntegerField()
    horas = models.IntegerField()
    
    class Meta:
        db_table = 'plazas'  # Esta apunta a tabla 'plazas'

class Directorio(models.Model):
    cct = models.TextField(blank=True, null=True)
    clave_adscripcion = models.TextField(blank=True, null=True)
    nombre = models.TextField(blank=True, null=True)
    nombre_departamento_corto = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    calle_numero = models.TextField(blank=True, null=True)
    colonia_zona = models.TextField(blank=True, null=True)
    codigo_postal = models.TextField(blank=True, null=True)
    ciudad_estado = models.TextField(blank=True, null=True)
    telefono_plantel = models.TextField(blank=True, null=True)
    telefono_plantel2 = models.TextField(blank=True, null=True)
    extension_depto = models.TextField(blank=True, null=True)
    extensiones_aux = models.TextField(blank=True, null=True)
    director = models.TextField(blank=True, null=True)
    coordinador_administrativo = models.TextField(blank=True, null=True)
    coordinador_academico = models.TextField(blank=True, null=True)
    municipio = models.CharField(max_length=255, blank=True, null=True)
    zona = models.CharField(max_length=255, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    activo = models.CharField(max_length=255, blank=True, null=True)
    fecha_creacion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adscripcion'

    def __str__(self):
        return self.nombre