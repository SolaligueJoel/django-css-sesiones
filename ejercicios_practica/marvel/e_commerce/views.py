# Importo vistas genericas
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView

# Importo los modelos 
from .models import Comic, WishList, Profile, PurchaseOrder
from django.contrib.auth.models import User


# Formulario de registro
from .forms import FormularioRegistro 
from django.shortcuts import render, redirect

from django.db import transaction
from django.contrib.auth.decorators import login_required


# Utilidades
from marvel.settings import VERDE, AMARILLO
from django.urls import reverse_lazy, reverse

# Tarea template-lenguaje
class PruebaView(TemplateView):
    template_name = 'e-commerce/base.html'


class LoginView(TemplateView):
	template_name = 'e-commerce/login.html'


def register(request):
    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            form.save()
            # Con todo terminado, redirigimos a la página de inicio de sesión,
            # porque por defecto, registrar un usuario no es iniciar una sesión.
            return redirect('update')
    else:
        # Si el método no es de tipo POST, se crea un objeto de tipo formulario
        # Y luego se envía al contexto de renderización. 
        form = FormularioRegistro()
    # Si los datos del POST son invalidos o si el método es distinto a POST
    # retornamos el render de la página de registro, con el formulario de registro en el contexto.
    return render(request, 'e-commerce/signup.html', {'form': form})


class IndexView(ListView):
    '''
    Página principal del sitio.
    Utilizamos `ListView` para poder aprovechar sus funciones de paginado.
    Para ello tenemos que utilizar sus atributos:
    \n
    '''
    queryset = Comic.objects.all().order_by('-id')
    # NOTE: Este queryset incorporará una lista de elementos a la que le asignará
    # Automáticamente el nombre de comic_list
    template_name = 'e-commerce/index.html'
    paginate_by = 10

    # NOTE: Examinamos qué incluye nuestro contexto:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        [print(AMARILLO+f'{element}\n') for element in context.items()]
        return context


class DetailsView(TemplateView):
    template_name = 'e-commerce/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            comic_obj = Comic.objects.get(
                marvel_id=self.request.GET.get('marvel_id'))
            context["comic"] = comic_obj
            context['comic_picture_full'] = str(
                comic_obj.picture).replace('/standard_xlarge', '')
            context['comic_desc'] = str(
                comic_obj.description).replace('<br>', '\n')
            username = self.request.user
            if username != None:
                user_obj = User.objects.filter(username=username)
                if user_obj.first() != None:
                    wish_obj = WishList.objects.filter(
                        user_id=user_obj[0].id, comic_id=comic_obj)
                    if wish_obj.first() != None:
                        context["favorite"] = wish_obj.first().favorite
                        context["cart"] = wish_obj.first().cart
                        context["wished_qty"] = wish_obj.first().wished_qty
                    else:
                        context["favorite"] = False
                        context["cart"] = False
                        context["wished_qty"] = 0
        except:
            return context
        return context

def check_button(request):
    '''
    Esta función tiene como objetivo el cambio de estado de los botones de favoritos y carrito.
    '''
    if request.method == 'POST':
        print(request.path)
        # NOTE: Obtenemos los datos necesarios:
        username = request.POST.get('username')
        marvel_id = request.POST.get('marvel_id')
        user_authenticated = request.POST.get('user_authenticated')
        type_button = request.POST.get('type_button')
        actual_value = request.POST.get('actual_value')
        path = request.POST.get('path')

        # Validamos los datos y les damos formato:
        username = username if username != '' else None
        marvel_id = marvel_id if marvel_id != '' else None
        user_authenticated = True if user_authenticated == 'True' else False
        type_button = type_button if type_button != '' else None
        actual_value = True if actual_value == 'True' else False
        path = path if path != None else 'index'

        if user_authenticated and username != None:
            # Si el usuario está autenticado, traemos su "wishlist"
            user_obj = User.objects.get(username=username)
            comic_obj = Comic.objects.get(marvel_id=marvel_id)
            wish_obj = WishList.objects.filter(
                user_id=user_obj, comic_id=comic_obj).first()
            if not wish_obj:
                # Si no tiene "wishlist" creamos una
                wish_obj = WishList.objects.create(
                    user_id=user_obj, comic_id=comic_obj)

            # Remplazamos el estado del botón seleccionado:
            if type_button == "cart":
                wish_obj.cart = not actual_value
                wish_obj.save()
                print('wish_obj.cart :', wish_obj.cart)
            elif type_button == "favorite":
                wish_obj.favorite = not actual_value
                print('wish_obj.favorite :', wish_obj.favorite)
                wish_obj.save()
            else:
                pass
            # Componemos los endpoints segun la página:
            if 'detail' in path:
                path += f'?marvel_id={marvel_id}'
            
            # Una vez terminada la modificación, volvemos a la misma página.
            return redirect(path)
        else:
            # Si el usuario no está autenticado, lo redirigimos a la página de logueo.
            return redirect('login')
    else:
        # Si por error quisieron acceder al recurso con otro método que no sea POST, lo redirigimos al index
        return redirect('index')

class ThanksView(TemplateView):
    '''
    Retorna detalle de la compra del usuario.
    Cambia el estado de cart = False y wished_qty = 0
    '''
    template_name = 'e-commerce/thanks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        username = self.request.user
        user_obj = User.objects.get(username=username)
        comic_obj = Comic.objects.get(id=user_obj.id)
        wish_obj = WishList.objects.filter(user_id=user_obj, cart=True)
        cart_items = [obj.comic_id for obj in wish_obj]

        
        wished_qty = wish_obj[0].wished_qty

        context['wished_qty'] = wished_qty


        for estado in wish_obj:
            estado.cart = False
            estado.wished_qty = 0

            estado.save()

        purchase_order = PurchaseOrder(user=user_obj,title=wish_obj[0].comic_id.title,
                         qty_comic=context['wished_qty'])
        purchase_order.save()


        context['user_order'] = purchase_order.user
        context['title_order'] = purchase_order.title
        context['buied_qty'] = purchase_order.qty_comic
        context['total_price'] = cart_items[0].price * wished_qty

        return context


class UserView(TemplateView):
	template_name = 'e-commerce/user.html'
	

class WishView(TemplateView):
	template_name = 'e-commerce/wish.html'


# Obtener los comics del usuario
class CartView(TemplateView):
    '''
    Vista de carrito de compras.
    Aquí se listará el total de elementos del carrito del usuario, 
    luego en el template se colocará un formulario en cada elemento del carrito
    para darlo de baja, y un boton general para concretar el pedido.
    '''
    template_name = 'e-commerce/cart.html'

    def get_context_data(self, **kwargs):
        '''
        En el contexto, devolvemos la lista total de elementos en el carrito de compras, 
        y el precio total calculado para la compra.
        '''
        context = super().get_context_data(**kwargs)
        try:
            username = self.request.user
            user_obj = User.objects.get(username=username)
            wish_obj = WishList.objects.filter(user_id=user_obj, cart=True)
            cart_items = [obj.comic_id for obj in wish_obj]

            context['wish_obj'] = wish_obj

            wished_qty = wish_obj[0].wished_qty

            context['wished_qty'] = wished_qty
            context['cart_items'] = cart_items
            context['total_price'] = cart_items[0].price * wished_qty

            # id del perfil
            context['wish_id'] = wish_obj[0].id

            print('El id del perfil es: ', wish_id)
            print('La cantidad de comics son: ',context['wished_qty'])
            print('El precio del comic es de: ',context['cart_items'][0].price)
            print('El precio total es de: ', context['total_price'])

            return context

        except:
            return context


class WishedQtyView(UpdateView):
    '''
    Formulario para incrementar wished_qty
    del modelo WishList
    '''
    model = WishList
    fields = ['wished_qty']
    template_name = 'e-commerce/update-carro.html'


class WishView(TemplateView):
    '''
    En esta vista vamos a traer todos los comics favoritos de un usuario en particular.
    Luego en el Template vamos a colocar un formulario por cada favorito, 
    para eliminarlo de la lista de favoritos.
    '''
    template_name = 'e-commerce/wish.html'

    def get_context_data(self, **kwargs):
        '''
        Preparamos en nuestro contexto la lista de comics del usuario registrado.
        '''
        context = super().get_context_data(**kwargs)
        username = self.request.user
        user_obj = User.objects.get(username=username)
        wish_obj = WishList.objects.filter(user_id=user_obj, favorite=True)
        cart_items = [obj.comic_id for obj in wish_obj]
        context['fav_items'] = cart_items
        print(context['fav_items'])
        return context


class UpdateUserView(UpdateView):
    '''
    Esta vista tiene como objetivo, proporcionar un formulario de actualización de los campos de usuario.
    '''
    model = Profile
    template_name = 'e-commerce/update-user.html'
    fields = ['country','province','postal_code','phone_number']



class UserView(TemplateView):
    '''Vista con el detalle de los datos personales del usuario'''
    template_name = 'e-commerce/user.html'

    def get_context_data(self, **kwargs):
        # TODO: Realizar la lógica que lista los datos del usuario, 
        # incluyendo los datos de la tabla de datos adicionales de usuario.
        context = super().get_context_data(**kwargs)

        user = User.objects.get(id=self.request.user.id)
        context['user_data'] = user

        return context



# NOTE: Vistas con Bootstrap:

class BootstrapLoginUserView(TemplateView):
    '''
    Vista para Template de login con estilo de bootstrap.
    '''
    template_name = 'e-commerce/bootstrap-login.html'

class BootstrapSignupView(TemplateView):
    '''
    Vista para Template de registro de usuario con estilo de bootstrap.
    '''
    template_name = 'e-commerce/bootstrap-signup.html'
		