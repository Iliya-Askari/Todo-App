from rest_framework import generics , views , permissions
from rest_framework.response import Response
from .serializer import *
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.models import Token
class RegestrationsApiView(generics.GenericAPIView):
    serializer_class = RegestrationsSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegestrationsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            data= {'email': email}
            return Response(data , status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
class CustomCreateTokenApiView(TokenObtainPairView):
    serializer_class = CustomLoginTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    
class CustomDiscardTokenApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
