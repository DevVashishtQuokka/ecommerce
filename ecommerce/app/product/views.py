from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import ProductCategory, Item
from .serializers import ProductCategorySerializer, ItemSerializer
from .permissions import ReadOnlyOrAdmin, SellerOnly, IsOwnerOrReadOnly
from utils.responder import Responder
from utils.helper import get_object_or_none

class ProductCategoryView(APIView):
    permission_classes = [ReadOnlyOrAdmin]

    def get(self, request):
        categories = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(categories, many=True)
        return Responder.success_response(150, data=serializer.data)

    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Responder.success_response(151, data=serializer.data, status_code=201)
        return Responder.error_response(400, errors=serializer.errors)

class ItemListCreateView(APIView):
    permission_classes = [SellerOnly]

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Responder.success_response(152, data=serializer.data)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Responder.success_response(153, data=serializer.data, status_code=201)
        return Responder.error_response(400, errors=serializer.errors)

class ItemDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, pk):
        return get_object_or_none(Item, pk=pk)

    def get(self, request, pk):
        item = self.get_object(pk)
        self.check_object_permissions(request, item)
        serializer = ItemSerializer(item)
        return Responder.success_response(154, data=serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        self.check_object_permissions(request, item)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Responder.success_response(155, data=serializer.data)
        return Responder.error_response(400, errors=serializer.errors)

    def delete(self, request, pk):
        item = self.get_object(pk)
        self.check_object_permissions(request, item)
        item.delete()
        return Responder.success_response(116)

