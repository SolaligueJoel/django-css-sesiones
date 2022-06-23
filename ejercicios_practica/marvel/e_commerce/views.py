from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.models import User


from .models import Comic, WishList
# Create your views here.
# Tarea template-lenguaje
class PruebaView(TemplateView):
    template_name = 'e-commerce/base.html'


class LoginView(TemplateView):
	template_name = 'e-commerce/login.html'


class ThanksView(TemplateView):
	template_name = 'e-commerce/thanks.html'


class UserView(TemplateView):
	template_name = 'e-commerce/user.html'
	

class WishView(TemplateView):
	template_name = 'e-commerce/wish.html'


# Obtener los comics del usuario
class CartView(TemplateView):
	template_name = 'e-commerce/cart.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.filter(username=self.request.user.username)
		comics_user = WishList.objects.filter(user_id=user.first(), cart=True)

		context['comics'] = comics_user

		return context


class WishView(TemplateView):
	template_name = 'e-commerce/wish.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.filter(username=self.request.user.username)
		favs_comics = WishList.objects.filter(user_id=user.first(), favorite=True)

		context['comics'] = favs_comics

		return context