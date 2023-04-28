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
        return reverse('detail', kwargs={'vet_id': self.id})
    
class Vaccination(models.Model):
    name = models.CharField(max_length=50)
    admin_by = models.ForeignKey(Vet, on_delete=models.CASCADE)
    date = models.DateField('Vaccination Date')

    def __str__(self):
        return f'{self.name} ({self.id})'

class Pet(models.Model):
    name = models.CharField(max_length=50)
    species = models.CharField(max_length=30)
    breed = models.CharField(max_length=50)
    birth_date = models.DateField('Birth Date')
    vaccinations = models.ManyToManyField(Vaccination)
    vet_doctors = models.ManyToManyField(Vet)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])
    


