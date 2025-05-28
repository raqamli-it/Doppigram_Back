from django.urls import path
from .views import SendCodeView, VerifyCodeView, CompleteProfileView, CompleteProfileGetView, ContactsListView

urlpatterns = [
    path('send/', SendCodeView.as_view()),
    path('verify/', VerifyCodeView.as_view()),
    path('complete/<int:user_id>/', CompleteProfileView.as_view()),
    path('complete_get/<int:user_id>/', CompleteProfileGetView.as_view()),
    path('contacts/', ContactsListView.as_view()),

]
