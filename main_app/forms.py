from django.forms import ModelForm
from .models import *

class VaccinationForm(ModelForm):
  class Meta:
    model = Vaccination
    fields = ['name', 'date', 'admin_by', 'visit']

    def __init__(self, *args, **kwargs):
        super(VaccinationForm, self).__init__(*args, **kwargs)
        self.fields['date'].required = False

class GroomingForm(ModelForm):
  class Meta:
    model = Grooming
    fields = ['location', 'date', 'duration', 'nail_trim', 'hair_trim', 'teeth_brush', 'bath', 'shampoo', 'conditioner']