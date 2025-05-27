import random
from django.core.mail import send_mail
from .models import VerificationCode

def send_verification_code(email):
    code = str(random.randint(10000, 99999))  # Tasodifiy 5 xonali kod yaratish
    VerificationCode.objects.create(email=email, code=code)
    send_mail(
        subject='Tasdiqlash kodi',
        message=f"Sizning tasdiqlash kodingiz: {code}",
        from_email='hamidullanishonboyev4@gmail.com',
        recipient_list=[email],
        fail_silently=False,
    )
    return code

def check_verification_code(email, code):
    return VerificationCode.objects.filter(email=email, code=code).exists()
