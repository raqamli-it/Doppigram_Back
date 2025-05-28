from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .serializers import EmailSerializer, VerifyCodeSerializer, UserProfileSerializer
from .utils import send_verification_code, check_verification_code
from rest_framework_simplejwt.tokens import RefreshToken

class SendCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            send_verification_code(email)
            return Response({"message": "Kod emailingizga yuborildi"}, status=201)
        return Response(serializer.errors, status=400)

class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            if check_verification_code(email, code):
                user, created = User.objects.get_or_create(email=email)
                user.is_verified = True
                user.save()

                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Tasdiqlandi",
                    "user_id": user.id,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                })

            return Response({"error": "Kod noto‘g‘ri"}, status=400)
        return Response(serializer.errors, status=400)


class CompleteProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Agar foydalanuvchi profilini allaqachon to‘ldirgan bo‘lsa, xatolik qaytaramiz
        if user.first_name and user.last_name and user.phone:
            return Response({"detail": "Profil allaqachon to‘ldirilgan"}, status=status.HTTP_400_BAD_REQUEST)

        # Ma'lumotlarni foydalanuvchi bilan birga yangilaymiz
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profil yaratildi"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompleteProfileGetView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)


class ContactsListView(APIView):
    def get(self, request):
        users = User.objects.filter(is_verified=True)
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)
