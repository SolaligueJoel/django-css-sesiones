from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile

class FormularioRegistro(forms.ModelForm):
	password1 = forms.CharField(label='Contraseña',widget=forms.PasswordInput(
		attrs = {
		'class': 'form-control',
		'placeholder': 'Ingrese contraseña',
		'id':'password1',		'requiered': 'requiered',
		}
		))

	password2 = forms.CharField(label='contraseña de confirmacion', widget= forms.PasswordInput(
		attrs = {
		'class': 'form-control',
		'placeholder': 'Ingrese nuevamente la contraseña',
		'id':'password2',
		'requiered': 'requiered',
		}
		)
		)

	class Meta:
		model = User
		fields = ('first_name','last_name','username',
			'email','password1','password2')


# class ProfileForm(forms.ModelForm):
#     class Meta:
#     	model = Profile
#     	fields = ['user','country','phone_number']