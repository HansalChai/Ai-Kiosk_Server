from django.urls import path
from .views import CategoryListView, CategoryDetailView, CategoryUpdateView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<int:category_id>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:category_id>/update/', CategoryUpdateView.as_view(), name='category-update'),
]