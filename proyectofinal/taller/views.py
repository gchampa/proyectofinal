import email
from multiprocessing import context
from re import S, template
from unicodedata import name
from attr import field
from django import forms
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render, redirect
from pkg_resources import require
from requests import request
from proyectofinal.taller.models import Propietario, Taller, Vehiculo, Messages
from .forms import PropietarioForms, VehiculoForms, TallerForms, MessagesForms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView 
from proyectofinal.users.models import User, Avatar
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django import forms
from datetime import *

class UserChangeFormCustom(UserChangeForm):
    username = forms.CharField(required=False)

    class Meta:
        model = User
        fields = "__all__"

class UserView(LoginRequiredMixin, TemplateView):
    template_name = "users/user_update.html"

    def get(self, request):
        context = {
            'form': UserChangeFormCustom(
            initial={
                #'username': request.user.username,
                'name': request.user.name,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'user_image': request.user.user_image,
                }
            )
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = UserChangeFormCustom(request.POST)
        if form.is_valid():
            user_update_info = form.cleaned_data
            user = request.user
            user.name = user_update_info.get('name')
            user.email = user_update_info.get('email')
            user.password1 = user_update_info.get('password1')
            user.password2 = user_update_info.get('password2')
            user.first_name = user_update_info.get('first_name')
            user.last_name = user_update_info.get('last_name')
            user.user_image = user_update_info.get('user_image')
            user.save()

            context = {
            'form': UserChangeFormCustom(
            initial={
                #'username': request.user.username,
                'name': request.user.name,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'avatar': request.user.avatar_user,
                #'image': Avatar.objects.filter(user=request.user)[0].image.url,
                }
            )
            }
            #return redirect("/taller/user_update_pass/")
            return render(request, self.template_name, context)


# Registrarse-----------------------------------------------
class UserCreationFormCustom(UserCreationForm):
    def save(self, commit: bool = True) -> User:
        self.data
        user = User.objects.create(
            username = self.data['username'],
            password = self.data['password1'],
        )
        return user


class RegisterView(TemplateView):
    template_name = 'crud/register.html'

    def get(self, request):
        context = {
            'form': UserCreationFormCustom()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationFormCustom(request.POST)
        if form:
            form.save()
            return render(request, self.template_name, context={'message': 'Te has registrado correctamente'})
        else:
            return render(request, self.template_name, context={'message': 'Error'})
#----------------------------------------------------------------------------------------------------------------

class LoginView(TemplateView):
    template_name = 'crud/login.html'

    def get(self, request):
        context = {
            'form': AuthenticationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form:
            user = request.POST.get('username')
            password = request.POST.get('password')
            user_auth = authenticate(username=user, password=password)
            if user_auth:
                login(request, user_auth)
                return redirect('http://127.0.0.1:8000')
                #return render(request, self.template_name, context={'message': f'Bienvenido {user}'})
            else:
                return render(request, self.template_name, context={'message': 'Error de Usuario o Password'})
        else:
            print('Error de formulario')
            return render(request, self.template_name, context={'message': 'Error de formulario'})


class PropietarioView(LoginRequiredMixin, TemplateView):
    template_name = 'crud/propietario.html'

    def get(self, request):
        context = {
            'propietarios': Propietario.objects.all()
        }
        return render(request,self.template_name, context)

class PropietarioDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'crud/propietario.html'

    def get(self, request, propietario_id):

        propietario = Propietario.objects.get(id=propietario_id)
        propietario.delete()

        
        context = {
            'propietarios': Propietario.objects.all()
        }

        return render(request,self.template_name, context)


class PropietarioCreateUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'crud/crear-propietario.html'

    def get(self, request, propietario_id=None):
        propietario = None
        if propietario_id:
            propietario = Propietario.objects.get(id=propietario_id)

        if propietario:
            # Update
            context = {
                'form': PropietarioForms(
                    initial={
                        'name': propietario.name,
                        'lastname': propietario.lastname,
                        'email': propietario.email,
                        
                    }
                )
            }
        else:
            # Create
            context = {
                'form': PropietarioForms()
            }

        return render(request,self.template_name, context)

    def post(self, request, propietario_id=None):
        obj_post = request.POST

        # Forma avanzada
        Propietario.objects.update_or_create(
            email=obj_post.get('email'), # -> filter
            defaults={
                'name': obj_post.get('name'),
                'lastname': obj_post.get('lastname'),
            }
        )

        context = {
            'form': PropietarioForms()
        }

        return render(request,self.template_name, context)


class VehiculoView(LoginRequiredMixin, TemplateView):
    template_name = 'crud/vehiculo.html'

    def get(self, request):
        context = {
            'vehiculos': Vehiculo.objects.all()
        }
        return render(request,self.template_name, context)

class VehiculoDeleteView(TemplateView):
    template_name = 'crud/vehiculo.html'

    def get(self, request, vehiculo_id):

        vehiculo = Vehiculo.objects.get(id=vehiculo_id)
        vehiculo.delete()

        
        context = {
            'vehiculos': Vehiculo.objects.all()
        }

        return render(request,self.template_name, context)


class VehiculoCreateUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'crud/crear-vehiculo.html'

    def get(self, request, vehiculo_id=None):
        vehiculo = None
        if vehiculo_id:
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)

        if vehiculo:
            # Update
            context = {
                'form': VehiculoForms(
                    initial={
                        'mark': vehiculo.mark,
                        'model': vehiculo.model,
                        'patent': vehiculo.patent,
                        
                    }
                )
            }
        else:
            # Create
            context = {
                'form': VehiculoForms()
            }

        return render(request,self.template_name, context)

    def post(self, request, vehiculo_id=None):
        obj_post = request.POST

        # Forma avanzada
        Vehiculo.objects.update_or_create(
            patent=obj_post.get('patent'), # -> filter
            defaults={
                'mark': obj_post.get('mark'),
                'model': obj_post.get('model'),
            }
        )

        context = {
            'form': VehiculoForms()
        }

        return render(request,self.template_name, context)

class TallerView(LoginRequiredMixin, TemplateView):
    template_name = 'crud/taller.html'

    def get(self, request):
        context = {
            'talleres': Taller.objects.all()
        }
        return render(request,self.template_name, context)

class TallerDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'crud/taller.html'

    def get(self, request, taller_id):

        taller = Taller.objects.get(id=taller_id)
        taller.delete()

        
        context = {
            'talleres': Taller.objects.all()
        }

        return render(request,self.template_name, context)


class TallerCreateUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'crud/crear-taller.html'

    def get(self, request, taller_id=None):
        taller = None
        if taller_id:
            taller = Taller.objects.get(id=taller_id)

        if taller:
            # Update
            context = {
                'form': TallerForms(
                    initial={
                        'name': taller.name,
                        'address': taller.address,
                        'city': taller.city,
                        
                    }
                )
            }
        else:
            # Create
            context = {
                'form': TallerForms()
            }

        return render(request,self.template_name, context)

    def post(self, request, taller_id=None):
        obj_post = request.POST

        # Forma avanzada
        Taller.objects.update_or_create(
            address=obj_post.get('address'), # -> filter
            defaults={
                'name': obj_post.get('name'),
                'city': obj_post.get('city'),
            }
        )

        context = {
            'form': TallerForms()
        }

        return render(request,self.template_name, context)

    
class SearchView(LoginRequiredMixin, TemplateView):
    template_name = 'forms/search.html'

    def post(self, request):
        
        #print('taller')
        print(request.POST.get('email'))
        context = {
            "elements": Propietario.objects.filter(
                email__icontains=request.POST.get('email')
            )
        }


        return render(request, self.template_name, context)

class AboutusView(LoginRequiredMixin, TemplateView):
    template_name = 'crud/aboutus.html'

    def get(self, request):
        context = {
            'image': Avatar.objects.filter(user=request.user).last().image.url,
        }
        return render(request, self.template_name, context)

class MessagesView(LoginRequiredMixin, TemplateView):
    template_name = 'crud/messages.html'

    def get(self, request):
        context = {
            'messages': Messages.objects.all(),
            'form': MessagesForms()
        }
        return render(request,self.template_name, context)
        

    def post(self, request):
        obj_post = request.POST
        date_now = date.today()
        message = Messages (user = obj_post.get('user'), mesg = obj_post.get('mesg'), date = date_now)
        message.save()

        context = {
            'messages': Messages.objects.all(),
            'form': MessagesForms()
        }
        return render(request,self.template_name, context)