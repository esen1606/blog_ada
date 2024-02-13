from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistration, LoginView, LogoutView, UserListAPIView, UserViewSet

router = DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('register/', UserRegistration.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('list_users/', UserListAPIView.as_view()),
    path('', include(router.urls)),
]