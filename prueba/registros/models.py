from django.db import models
from ckeditor.fields import RichTextField

class Alumnos(models.Model): # Define la estructura de nuestra tabla
    matricula = models.CharField(max_length=12,verbose_name="Mat") #Texto corto    
    nombre = models.TextField()  #Texto largo 
    carrera = models.TextField()
    turno= models.CharField(max_length=10)
    imagen = models.ImageField(upload_to='fotos', null=True, verbose_name="Fotografía") #Campo para subir imagenes
    created = models.DateTimeField(auto_now_add=True) #Fecha y tiempo
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"
        ordering = ["-created"]
        #el menos indica que se ordenada de mas reciente al mas viejo
    
    def _str_(self):
        return self.nombre

class Comentario(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Clave")
    alumno = models.ForeignKey(Alumnos, on_delete=models.CASCADE, verbose_name="Alumno")
    created = models.DateTimeField(auto_now_add=True,verbose_name="Registrado")
    coment = RichTextField(verbose_name="Comentario")

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ["-created"]

    def _str_(self):
        return self.coment
    
class ComentarioContacto(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Clave")
    usuario = models.TextField(verbose_name="Usuario")
    mensaje = models.TextField(verbose_name="Mensaje")
    created = models.DateTimeField(auto_now_add=True,verbose_name="Registrado")

    class Meta:
        verbose_name = "Comentario Contactos"
        verbose_name_plural = "Comentarios Contactos"
        ordering = ["-created"]

    def _str_(self):
        return self.mensaje
    #Indica que se mostrára el mensaje como valor en la tabla

class Archivos(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, verbose_name="Título")
    descripcion = models.TextField(null=True, blank=True)
    archivo = models.FileField(upload_to='archivos', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Archivo"
        verbose_name_plural = "Archivos"
        ordering = ["-created"]

    def _str_(self):
        return self.titulo