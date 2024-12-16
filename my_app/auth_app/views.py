from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Admin
from .serializers import AdminLoginSerializer

class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                admin = Admin.objects.get(email=email)
                
                if admin.check_password(password):
                    return Response(
                        {"message": "Authentification réussie"}, 
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"error": "Mot de passe incorrect"}, 
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except Admin.DoesNotExist:
                return Response(
                    {"error": "Aucun utilisateur trouvé avec cet email"},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
