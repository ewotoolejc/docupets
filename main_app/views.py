from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import *

# Create your views here.

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('pet_index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


def home(request):
  return render(request, 'home.html')

def PetVaccinationDetail(request, pet_id):
  pet = Pet.objects.get(id=pet_id)
  vaccination_form = VaccinationForm()
  return render(request, 'vaccination/detail.html', { 'pet': pet,
  'vaccination_form': vaccination_form })


def pet_addvaccination(request, pet_id):
  form = VaccinationForm(request.POST)

  if form.is_valid():
    new_vaccine = form.save(commit=False)
    new_vaccine.pet_id = pet_id
    new_vaccine.save()
  return redirect('pet_detail', pk=pet_id)

class PetList(ListView):
  model = Pet

class PetDetailView(FormMixin, DetailView):
  model = Pet
  form_class = GroomingForm
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['availvets'] = Vet.objects.exclude(pet=self.object)
    return context

def assoc_vet(request, pet_id, vet_id):
  Pet.objects.get(id=pet_id).vet_doctors.add(vet_id)
  return redirect('pet_detail', pk=pet_id)

def unassoc_vet(request, pet_id, vet_id):
  Pet.objects.get(id=pet_id).vet_doctors.remove(vet_id)
  return redirect('pet_detail', pk=pet_id)

def add_grooming(request, pet_id):
  form = GroomingForm(request.POST)
  if form.is_valid():
    new_grooming = form.save(commit=False)
    new_grooming.pet_id = pet_id
    new_grooming.save()
    return redirect('pet_detail', pk=pet_id)

class GroomingDeleteView(DeleteView):
  model = Grooming
  success_url = '/pets'

class PetCreateView(CreateView):
  model = Pet
  fields = ['name', 'species', 'breed', 'birth_date']

  def form_valid(self, form):
   form.instance.user = self.request.user
   return super().form_valid(form)

class PetUpdateView(UpdateView):
  model = Pet
  fields = ['name', 'species', 'breed', 'birth_date']

class PetDeleteView(DeleteView):
  model = Pet
  success_url = '/pets'

class VetList(ListView):
  model = Vet

class VetDetailView(DetailView):
  model = Vet

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['patients'] = Pet.objects.filter(vet_doctors=self.object)
    context['availpets'] = Pet.objects.exclude(vet_doctors=self.object)
    return context

class VetCreateView(CreateView):
  model = Vet
  fields = '__all__'

class VetUpdateView(UpdateView):
  model = Vet
  fields = '__all__'

class VetDeleteView(DeleteView):
  model = Vet
  success_url = '/vets'