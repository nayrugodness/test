from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from djsniper.sniper.models import NFTProject
from .serializers import NFTProjectSerializer, CategorySerializer


class ProjectViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = NFTProjectSerializer
    queryset = NFTProject.objects.all()
    lookup_field = "name"


class CategoryViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = CategorySerializer
    queryset = CategorySerializer.objects.all()
    lookup_field = "name"
