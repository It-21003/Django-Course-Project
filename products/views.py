from django.shortcuts import render
from django.http import HttpResponse , Http404
from rest_framework.views import APIView
from .serializers import ProductSerializers
from .models import Product,User
from rest_framework import status
from rest_framework.response import Response
from .permissions import IsAdmin, IsStaff

from rest_framework.permissions import IsAuthenticated , IsAdminUser

def index(request):
    return HttpResponse("Hello, world!")

class ProductView(APIView):
    permission_classes=[IsAuthenticated]


    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]    
        elif self.request.method in['PUT','PATCH','DELETE']:
            return [IsAdmin()]
        elif self.request.method == 'POST':
             return [IsStaff()]
        return super().get_permissions()
    

    def post(self,request):
        serializer = ProductSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



#get all products or single product
### 200 - ok , 401 - skip, 500 - skip
# 404 - Not found

    def get(self,request,id=None):
        if id:
            try:
                product = Product.objects.get(id=id)
            except Product.DoesNotExist:
                raise  Http404
            serializer = ProductSerializers(product)
            return Response(serializer.data)

        else:
            products = Product.objects.all() #list of python object
            serializer = ProductSerializers(products,many=True) #convert to JSON object
            return Response(serializer.data)
        

    def put(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
                raise  Http404
        serializer = ProductSerializers(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


    
    def delete(self,request,id):
       
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
                raise  Http404
        product.delete()
        serializer = ProductSerializers(product) 
        return Response(serializer.data)
        return Response({"message": "Product deleted successfully."}, status=status.HTTP_200_OK)
        

    def patch(self,request,id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
                raise  Http404
        serializer = ProductSerializers(product,data=request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    #create your view
    
    