from djsniper.sniper.models import NFT, NFTAttribute, NFTProject, NFTTrait, Category
from djsniper.users.models import Order
from rest_framework import fields, filters, serializers


class NFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFT

        fields = '__all__'
        filters = ('rank', 'rarity_score')
        list_per_page = 15
        search_help_text = "Buscar por ranking o por score"

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        filters = 'name'
        list_per_page = 15
        search_help_text = "Buscar por nombre"

class NFTAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = NFTAttribute
        fields = '__all__'
        filters = 'name'
        list_per_page = 15
        search_help_text = "Buscar por nombre"


class NFTProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTProject
        fields = '__all__'
        filters = ("name", "number_of_nfts")
        list_per_page = 15
        search_help_text = "Buscar por nombre o por cantidad de bonos"


class NFTTraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTTrait
        fields = '__all__'
        filters = ["rarity_score"]
        list_per_page = 15
        search_help_text = ["Buscar por score"]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        #filters = ("name", "number_of_nfts")
        list_per_page = 10
        #search_help_text = "Buscar por nombre o por cantidad de bonos"
