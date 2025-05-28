from django.urls import path
from .views import SendCodeView, VerifyCodeView, CompleteProfileView, CompleteProfileGetView, ContactsListView

urlpatterns = [
    path('email/', SendCodeView.as_view()),
    path('verify/', VerifyCodeView.as_view()),
    path('profil/', CompleteProfileView.as_view()),
    path('profil_get/', CompleteProfileGetView.as_view()),
    path('contacts/', ContactsListView.as_view()),
]
