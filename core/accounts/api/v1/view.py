from rest_framework import generics
from rest_framework.response import Response
from .serializer import *
from rest_framework import status


class RegestrationsApiView(generics.GenericAPIView):
    serializer_class = RegestrationsSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegestrationsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            username = serializer.validated_data['username']
            data= {'username': username}
            return Response(data , status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)