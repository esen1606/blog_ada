from django.urls import path
from .views import FavoriteCreateView,FavoriteDeleteView

urlpatterns = [
    path('', FavoriteCreateView.as_view()),
    path('<int:id>/', FavoriteDeleteView.as_view()),
]