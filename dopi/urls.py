from django.urls import path
from .views import SendCodeView, VerifyCodeView, CompleteProfileView

urlpatterns = [
    path('send-code/', SendCodeView.as_view()),
    path('verify-code/', VerifyCodeView.as_view()),
    path('complete-profile/<int:user_id>/', CompleteProfileView.as_view()),
]
