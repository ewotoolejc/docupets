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
        return f'{self.name}'
    
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
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('pet_detail', args=[str(self.id)])


class Grooming(models.Model):
    location = models.CharField(max_length=50)
    date = models.DateField('Grooming Date')
    duration = models.IntegerField()
    nail_trim = models.BooleanField(blank=False)
    hair_trim = models.BooleanField(blank=False)
    teeth_brush = models.BooleanField(blank=False)
    bath = models.BooleanField(blank=False)
    shampoo = models.BooleanField(blank=False)
    conditioner = models.BooleanField(blank=False)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.location} {self.date} ({self.id})'

class Visit(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField('Visit Date')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    vet = models.ForeignKey(Vet, on_delete=models.CASCADE)
    notes = models.CharField()
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.date})'
    
    def get_absolute_url(self):
        return reverse('visit_detail', args=[str(self.id)])

class Vaccination(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField('Vaccination Date', null=True)
    admin_by = models.ForeignKey(Vet, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('pet_addvaccination', args=[str(self.id)])