from django.urls import path, include
from .views import CategoryDetaiView, CategoryCreateListView

urlpatterns = [
    path('create/', CategoryCreateListView.as_view()),
    path('detail/<int:id>/', CategoryDetaiView.as_view()),
]