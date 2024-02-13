from django.urls import path
from .views import LikeCreateView, LikeDeleteView

urlpatterns = [
    path('', LikeCreateView.as_view()),
    path('<int:id>/', LikeDeleteView.as_view()),
]