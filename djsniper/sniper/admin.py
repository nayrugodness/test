from django.contrib import admin
from .models import NFTProject, NFT, NFTTrait, NFTAttribute, Category


class NFTAdmin(admin.ModelAdmin):
    model = NFT
    list_display = ["nft_id", "rank", "rarity_score", "image"]
    search_fields = ["nft_id__exact", "rank", "rarity_score"]
    list_filter = ["rank", "rarity_score"]
    list_per_page = 15
    search_help_text = "Buscar por ranking o score"


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ["id", "name", "image", "created", "edited"]
    search_fields = ["id", "name"]
    list_filter = ["name", "edited"]
    list_per_page = 15
    search_help_text = "Buscar por nombre o última fecha de edición"


class NFTAttributeAdmin(admin.ModelAdmin):
    model = NFTAttribute
    list_display = ["value"]
    list_per_page = 15


class NFTProjectAdmin(admin.ModelAdmin):
    model = NFTProject
    list_display = ["id", "name", "image", "supply", "price", "chain"]
    list_filter = ["id", "name", "supply", "price", "chain"]
    list_per_page = 15
    search_fields = ["id", "name", "supply", "price", "chain"]
    search_help_text = ["Buscar por ID, nombre, cantidad de bonos, precio individual de los bonos o cadena de bloques"]


class NFTTraitAdmin(admin.ModelAdmin):
    model = NFTTrait
    list_display = ["rarity_score"]
    list_filter = ["rarity_score"]
    list_per_page = 15
    search_fields = ["rarity_score"]
    search_help_text = "Buscar por score"


admin.site.register(NFTProject, NFTProjectAdmin)
admin.site.register(NFTTrait, NFTTraitAdmin)
admin.site.register(NFT, NFTAdmin)
admin.site.register(NFTAttribute, NFTAttributeAdmin)
admin.site.register(Category, CategoryAdmin)
