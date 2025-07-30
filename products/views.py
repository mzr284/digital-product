from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from subscriptions.models import Subscription



from .models import Category, Product, File
from .serializers import CategorySerializer, ProductSerializer, FileSerializer

# Categories:
class CategoryListView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={"request": request})
        return Response(serializer.data)


class CategoryDetailView(APIView):

    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, context={"request": request})
        return Response(serializer.data)


# Products:
class ProductListView(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductDetailView(APIView):

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, context={"request": request})
        return Response(serializer.data)


# Files:
class FileListView(APIView):

    def get(self, request, product_pk):
        files = File.objects.filter(parent=product_pk)
        serializer = FileSerializer(files, many=True, context={"request": request})
        return Response(serializer.data)


class FileDetailView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, product_pk, file_pk):

        if not Subscription.objects.filter(user=request.user, expire_time__gt=timezone.now()).exists():
            return Response({'message': "You don't have a subscription right now"},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            file = File.objects.get(pk=file_pk, parent=product_pk)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FileSerializer(file, context={"request": request})
        return Response(serializer.data)

