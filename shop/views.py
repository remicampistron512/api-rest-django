from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from shop.models import Category, Product
from shop.serializers import CategorySerializer, ProductSerializer


class ProductViewset(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()


class CategoryViewset(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()
