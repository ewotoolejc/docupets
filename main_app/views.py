from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
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
  vaccination_form = VaccinationForm()
  return render(request, 'vaccination/detail.html', {
    'vaccination_form': vaccination_form })


def PetAddVaccinationView(request,pet_id):
  form = VaccinationForm(request.POST)

  if form.is_valid():
    new_vaccine = form.save(commit=False)
    new_vaccine.pet_id = pet_id
    new_vaccine.save()
  
  return redirect('pet_detail', pk=pet_id)

class PetList(ListView):
  model = Pet

class PetDetailView(DetailView):
  model = Pet

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

#class PetAddVaccinationView(CreateView):
# model = Vaccination
#  fields = '__all__'
#  success_url = '/pets'

  # def form_valid(self, form):
  #  form.instance.user = self.request.user
  #  return super().form_valid(form)

class VetList(ListView):
  model = Vet

class VetDetailView(DetailView):
  model = Vet

class VetCreateView(CreateView):
  model = Vet
  fields = '__all__'

class VetUpdateView(UpdateView):
  model = Vet
  fields = '__all__'

class VetDeleteView(DeleteView):
  model = Vet
  success_url = '/vets'