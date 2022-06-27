from django.urls import path
from e_commerce.api.marvel_api_views import *
from e_commerce.api.api_views import PostComicAPIView

# Importamos las API_VIEWS:
from e_commerce.views import *

# Login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


INDEX_LIST = ['index/', 'index/#', '']
INDEX_PATTERNS = [path(x, IndexView.as_view()) for x in INDEX_LIST]

urlpatterns = [
    # NOTE: e_commerce base:
    path('base', PruebaView.as_view(), name='base'),
    
    #TODO: Paginas del sitio 
    path('detail', DetailsView.as_view(), name='detail'),
    path('index', IndexView.as_view(), name='index'),
    path('user', UserView.as_view(), name='user'),

    # Editar perfil
    path('update-user/<int:pk>', UpdateUserView.as_view(), name= 'update'),

    # Implementar cantidad de comics
    path('update-carro/<int:pk>', WishedQtyView.as_view(), name= 'update-carro'),

    path('thanks/<int:pk>', ThanksView.as_view(), name='thanks'),
    path('cart', CartView.as_view(), name='cart'),
    path('wish', WishView.as_view(), name='wish'),

    # Sesiones
    path('login',auth_views.LoginView.as_view(template_name='e-commerce/login.html',
     redirect_authenticated_user=True, redirect_field_name='index'), name='login' ),
    path('registro', register, name='registro'),

    path('logout',auth_views.LogoutView.as_view(next_page='/e-commerce/index',
     redirect_field_name='index')),

    # NOTE: Formularios ocultos
    path('checkbutton', check_button, name='checkbutton'),
    
        # NOTE: Ejemplos de Bootstrap HTML:
    path('bootstrap-login', BootstrapLoginUserView.as_view(), name='loginbootstrap'),
    path('bootstrap-signup', BootstrapSignupView.as_view(), name='signupbootstrap'),
]
urlpatterns += INDEX_PATTERNS
    