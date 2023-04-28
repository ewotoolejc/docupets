from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView


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