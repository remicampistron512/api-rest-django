from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from shop.permissions import IsAdminAuthenticated, IsStaffAuthenticated

from shop.models import Category, Product, Article
from shop.serializers import CategoryDetailSerializer, CategoryListSerializer, ProductListSerializer, \
    ProductDetailSerializer, ArticleListSerializer, ArticleListSerializer


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProductViewset(ReadOnlyModelViewSet):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        # Nous récupérons tous les produits dans une variable nommée queryset
        queryset = Product.objects.filter(active=True)
        # Vérifions la présence du paramètre ‘category_id’ dans l’url et si oui alors appliquons notre filtre
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()


class ArticleViewset(ReadOnlyModelViewSet):
    serializer_class = ArticleListSerializer

    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset


class CategoryViewset(ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    # Ajoutons un attribut de classe qui nous permet de définir notre serializer de détail
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)

    def get_serializer_class(self):
        # Si l'action demandée est retrieve nous retournons le serializer de détail
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()



class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]

    def get_queryset(self):
        return Category.objects.all()


class AdminArticleViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ArticleListSerializer
    queryset = Article.objects.all()