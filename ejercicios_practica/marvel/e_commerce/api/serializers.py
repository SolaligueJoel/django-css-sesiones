  
# Primero importamos los modelos que queremos serializar:
from e_commerce.models import Comic,WishList
from django.contrib.auth.models import User


# Luego importamos todos los serializadores de django rest framework.
from rest_framework import serializers

class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = ('marvel_id','title','description','price','stock_qty','picture',)


        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ("__all__")

# TODO: Realizar el serializador para el modelo de WishList

class WishListSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(write_only=True,
                queryset= User.objects.all())
    comic_id = serializers.PrimaryKeyRelatedField(write_only=True,
        queryset=Comic.objects.all())


    class Meta:
        model = WishList
        fields = '__all__'


class GetUserFavsSerializer(serializers.ModelSerializer):
    comic_id = ComicSerializer()
    class Meta:
        model = WishList
        fields = '__all__'


    def to_representation(self, instance):
        return {
        'marvel_id':instance.comic_id.marvel_id,
        'title':instance.comic_id.title,
        'description':instance.comic_id.description,
        'price':instance.comic_id.stock_qty,
        'picture':instance.comic_id.picture
        }





