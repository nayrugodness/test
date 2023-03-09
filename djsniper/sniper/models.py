from django.db import models
from django.db.models import CharField
import uuid
Coins = (
    ('USD', 'USD')
)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    image = models.ImageField(null=True)
    created = models.DateField(auto_now_add=True)
    edited = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.name}"

class NFTProject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract_address = models.CharField(max_length=100)
    contract_abi = models.TextField()
    name = models.CharField(max_length=50)  # e.g BAYC
    number_of_nfts = models.PositiveIntegerField(default=10)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    supply = models.IntegerField(blank=True)
    price = models.CharField(max_length=200, null=True)
    chain = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=500, null=True)
    coin = CharField(max_length=20, choices=Coins, default="USD", blank=False, editable=False)

    def __str__(self):
        return self.name


class NFT(models.Model):
    project = models.ForeignKey(
        NFTProject, on_delete=models.CASCADE, related_name="nfts"
    )
    rarity_score = models.FloatField(null=True)
    nft_id = models.PositiveIntegerField()
    image = models.ImageField(null=True)
    rank = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.project.name}: {self.nft_id}"


class NFTAttribute(models.Model):
    project = models.ForeignKey(
        NFTProject, on_delete=models.CASCADE, related_name="attributes"
    )
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name}: {self.value}"


class NFTTrait(models.Model):
    nft = models.ForeignKey(
        NFT, on_delete=models.CASCADE, related_name="nft_attributes"
    )
    attribute = models.ForeignKey(
        NFTAttribute, on_delete=models.CASCADE, related_name="traits"
    )
    rarity_score = models.FloatField(null=True)

    def __str__(self) -> str:
        return f"{self.attribute.name}: {self.attribute}"


