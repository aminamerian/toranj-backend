from django.db.models import Window, F
from django.db.models.functions import Lag
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter

from .models import Category, Product, PriceChangeLog, Shop
from .serializers import CategorySerializer, ProductSerializer, PriceChangeLogSerializer
from .filter import ProductListFilterBackend


class ProductCreate(generics.CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                return Response({'uid': instance.uid}, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Shop.DoesNotExist:
            return Response({'error': 'shop does not exist'}, status=status.HTTP_404_NOT_FOUND)


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [ProductListFilterBackend, OrderingFilter]
    ordering_fields = ['price', 'date_updated']
    ordering = ['-date_updated']


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class PriceChangeList(generics.ListAPIView):
    serializer_class = PriceChangeLogSerializer
    queryset = PriceChangeLog.objects.all()

    def get_queryset(self):
        uid = self.request.query_params.get('uid')
        return PriceChangeLog.objects.filter(product__uid=uid).annotate(
            old_price=Window(expression=Lag('price'), order_by=F('date').asc()),
            old_availability=Window(expression=Lag('is_available'), order_by=F('date').asc()),
        ).order_by('-date')


class ProductRedirect(APIView):
    def get(self, request):
        uid = self.request.query_params.get('uid')
        if uid is not None:
            try:
                redirect_url = Product.objects.get(uid=uid).page_url
            except Product.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response({"product_url": redirect_url}, status=status.HTTP_200_OK)
        return Response({"error": "uid query is required"}, status=status.HTTP_400_BAD_REQUEST)
