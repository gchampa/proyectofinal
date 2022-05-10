from unicodedata import name
from django import views    
from django.urls import path
#from django.contrib.auth.views import LoginView 

from proyectofinal.taller.views import (PropietarioView, PropietarioCreateUpdateView, PropietarioDeleteView,
                                        VehiculoView, VehiculoCreateUpdateView, VehiculoDeleteView,
                                        TallerView, TallerCreateUpdateView, TallerDeleteView,
                                        SearchView, LoginView, RegisterView, UserView, AboutusView, MessagesView)
from django.views.generic import TemplateView

app_name = "taller"
urlpatterns = [

    path('propietario-view/', PropietarioView.as_view(), name='propietario-view'),
    path('propietario-delete/<int:propietario_id>/', PropietarioDeleteView.as_view(), name='propietario-delete'),
    path('propietario-create/', PropietarioCreateUpdateView.as_view(), name='propietario-create'),
    path('propietario-update/<int:propietario_id>/', PropietarioCreateUpdateView.as_view(), name='propietario-update'),
    
    path('vehiculo-view/', VehiculoView.as_view(), name='vehiculo-view'),
    path('vehiculo-delete/<int:vehiculo_id>/', VehiculoDeleteView.as_view(), name='vehiculo-delete'),
    path('vehiculo-create/', VehiculoCreateUpdateView.as_view(), name='vehiculo-create'),
    path('vehiculo-update/<int:vehiculo_id>/', VehiculoCreateUpdateView.as_view(), name='vehiculo-update'),

    path('taller-view/', TallerView.as_view(), name='taller-view'),
    path('taller-delete/<int:taller_id>/', TallerDeleteView.as_view(), name='taller-delete'),
    path('taller-create/', TallerCreateUpdateView.as_view(), name='taller-create'),
    path('taller-update/<int:taller_id>/', TallerCreateUpdateView.as_view(), name='taller-update'),

    path('search/', SearchView.as_view(), name='search'),
    path('login/', LoginView.as_view(), name='login'),
    #path('register/', RegisterView.as_view(), name='register'),
    path('user_update/', UserView.as_view(), name='user_update'),
    path('aboutus/', AboutusView.as_view(), name='aboutus'),
    path ('messages/', MessagesView.as_view(), name='messages'),
]