from django.db import models

class Planilla(models.Model):
    no = models.BigIntegerField(primary_key=True)
    nombre = models.TextField(blank=True, null=True)
    adscripcion = models.TextField(blank=True, null=True)
    departamento = models.TextField(blank=True, null=True)
    clave = models.BigIntegerField(blank=True, null=True)
    rfc = models.TextField(blank=True, null=True)
    curp = models.TextField(blank=True, null=True)
    puesto = models.TextField(blank=True, null=True)
    fecha_de_ingreso = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'planilla'
