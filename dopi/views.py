from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import EmailSerializer, VerifyCodeSerializer, UserProfileSerializer, ContactSerializer
from .utils import send_verification_code, check_verification_code

class SendCodeView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            send_verification_code(email)
            return Response({"message": "Kod emailingizga yuborildi"}, status=201)
        return Response(serializer.errors, status=400)

class VerifyCodeView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            if check_verification_code(email, code):
                user, created = User.objects.get_or_create(email=email)
                user.is_verified = True
                user.save()
                return Response({"message": "Tasdiqlandi", "user_id": user.id})
            return Response({"error": "Kod noto‘g‘ri"}, status=400)
        return Response(serializer.errors, status=400)

class CompleteProfileView(APIView):
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserProfileSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Profil to‘ldirildi"})
            return Response(serializer.errors, status=400)
        except User.DoesNotExist:
            return Response({"error": "Foydalanuvchi topilmadi"}, status=404)


class CompleteProfileGetView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "Foydalanuvchi topilmadi"}, status=404)

class ContactsListView(APIView):
    def get(self, request):
        users = User.objects.filter(is_verified=True)
        serializer = ContactSerializer(users, many=True)
        return Response(serializer.data)