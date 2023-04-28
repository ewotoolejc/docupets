from django.forms import ModelForm
from .models import *

class VaccinationForm(ModelForm):
  class Meta:
    model = Vaccination
    fields = ['name', 'date', 'admin_by']