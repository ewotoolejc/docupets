from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('pets/', views.PetList.as_view(), name='pet_index'),
    path('pets/<int:pk>', views.PetDetailView.as_view(), name='detail'),
    path('pets/create', views.PetCreateView.as_view(), name='pet_create'),
]

