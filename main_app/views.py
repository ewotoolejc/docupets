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

@login_required
def PetVaccinationDetail(request, pet_id):
  pet = Pet.objects.get(id=pet_id)
  vaccination_form = VaccinationForm()
  return render(request, 'vaccination/detail.html', { 'pet': pet,
  'vaccination_form': vaccination_form })

@login_required
def pet_addvaccination(request, pet_id):
  form = VaccinationForm(request.POST)

  if form.is_valid():
    new_vaccine = form.save(commit=False)
    new_vaccine.pet_id = pet_id
    new_vaccine.save()
  return redirect('pet_detail', pk=pet_id)

class PetList(LoginRequiredMixin, ListView):
  model = Pet

  def get_queryset(self):
    return self.model.objects.filter(user=self.request.user)

class PetDetailView(LoginRequiredMixin, FormMixin, DetailView):
  model = Pet
  form_class = GroomingForm
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['availvets'] = Vet.objects.exclude(pet=self.object)
#    context['groomings'] = Grooming.objects.all()
    context['today'] = date.today()
    return context


@login_required
def assoc_vet(request, pet_id, vet_id):
  Pet.objects.get(id=pet_id).vet_doctors.add(vet_id)
  return redirect('pet_detail', pk=pet_id)

@login_required
def unassoc_vet(request, pet_id, vet_id):
  Pet.objects.get(id=pet_id).vet_doctors.remove(vet_id)
  return redirect('pet_detail', pk=pet_id)

@login_required
def add_grooming(request, pet_id):
  form = GroomingForm(request.POST)
  if form.is_valid():
    new_grooming = form.save(commit=False)
    new_grooming.pet_id = pet_id
    new_grooming.save()
    return redirect('pet_detail', pk=pet_id)

@login_required
def GroomingDeleteView(request,pet_id,grooming_id):
  pet = Pet.objects.get(id=pet_id)
  grooming = Grooming.objects.get(id=grooming_id)
  return render(request, 'grooming/grooming_confirm_delete.html', { 
    'pet': pet,
    'grooming': grooming
  })

@login_required
def GroomingDelete(request,pet_id,grooming_id):
 Grooming.objects.filter(id=grooming_id).delete()
 return redirect('pet_detail', pk=pet_id)


class PetCreateView(LoginRequiredMixin, CreateView):
  model = Pet
  fields = ['name', 'species', 'breed', 'birth_date']

  def form_valid(self, form):
   form.instance.user = self.request.user
   return super().form_valid(form)

class PetUpdateView(LoginRequiredMixin, UpdateView):
  model = Pet
  fields = ['name', 'species', 'breed', 'birth_date']

class PetDeleteView(LoginRequiredMixin, DeleteView):
  model = Pet
  success_url = '/pets'

class VetList(LoginRequiredMixin, ListView):
  model = Vet

class VetDetailView(LoginRequiredMixin, DetailView):
  model = Vet

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['patients'] = Pet.objects.filter(vet_doctors=self.object)
    context['availpets'] = Pet.objects.exclude(vet_doctors=self.object)
    return context

class VetCreateView(LoginRequiredMixin, CreateView):
  model = Vet
  fields = '__all__'

class VetUpdateView(LoginRequiredMixin, UpdateView):
  model = Vet
  fields = '__all__'

class VetDeleteView(LoginRequiredMixin, DeleteView):
  model = Vet
  success_url = '/vets'

class VisitList(LoginRequiredMixin, ListView):
  model = Visit

  def get_queryset(self):
   return self.model.objects.filter(user=self.request.user)

class VisitDetailView(LoginRequiredMixin, DetailView):
  model = Visit


  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['vaccines'] = Vaccination.objects.filter(visit=self.object)
    return context

class VisitCreateView(LoginRequiredMixin, CreateView):
  model = Visit
  fields = ['name', 'date', 'pet', 'vet', 'notes']

  # def __init__(self, *args, **kwargs):
  #  super(VisitCreateView, self).__init__(*args, **kwargs)
  #  self.fields['pet'].queryset = Pet.objects.filter(name='Obi')

  def form_valid(self, form):
   form.instance.user = self.request.user
   return super().form_valid(form)

class VisitUpdateView(LoginRequiredMixin, UpdateView):
  model = Visit
  fields = ['name', 'date', 'pet', 'vet', 'notes']

class VisitDeleteView(LoginRequiredMixin, DeleteView):
  model = Visit
  success_url = '/visits'

