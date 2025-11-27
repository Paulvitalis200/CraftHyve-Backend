from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(APIView):
    """
    Custom view for obtaining JWT tokens that checks user verification
    """
    permission_classes = []

    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

