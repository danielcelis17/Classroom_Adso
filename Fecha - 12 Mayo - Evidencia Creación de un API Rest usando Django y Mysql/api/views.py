from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ClienteSerializer
from .models import Cliente
from rest_framework import status


class Cliente_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        cliente = Cliente.objects.all()
        serializer = ClienteSerializer(cliente, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
