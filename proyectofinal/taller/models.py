from django.db  import models
from pytest import MarkDecorator


    # Charfield
    # IntegerField
    # DateField
    # ForeingKeyField
    # TextField

class Vehiculo(models.Model):
    mark = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    patent = models.CharField(max_length=40)
    # text = models.CharField(
    #     max_length=50, null= True, blank=True)

class Propietario(models.Model):
    name = models.CharField(max_length=40)
    lastname = models.CharField(max_length=40)
    email = models.EmailField()
    
    def __str__(self) -> str:
        return f'{self.name} {self.lastname}'

class Taller(models.Model):
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    city=models.CharField(max_length=40)

class Messages(models.Model):
    user = models.CharField(max_length=40)
    mesg = models.CharField(max_length=10000)
    date = models.DateField()


