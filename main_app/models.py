from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User



# Create your models here.
class Vet(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    specialty = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('vet_detail', args=[str(self.id)])
    


class Pet(models.Model):
    name = models.CharField(max_length=50)
    species = models.CharField(max_length=30)
    breed = models.CharField(max_length=50)
    birth_date = models.DateField('Birth Date')
    vet_doctors = models.ManyToManyField(Vet)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('pet_detail', args=[str(self.id)])

class Vaccination(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField('Vaccination Date')
    admin_by = models.ForeignKey(Vet, on_delete=models.CASCADE)
    pet  = models.ManyToManyField(Pet)

    def __str__(self):
        return f'{self.name} ({self.id})'
    


