from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import CategoryViewSet, OptionViewSet, MenuListCreateView, MenuDetailView, OrderAmountView, OrderCreateView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

category_router = NestedDefaultRouter(router, r'categories', lookup='category')
category_router.register(r'options', OptionViewSet, basename='category-options')


urlpatterns = [
    # 라우터 설정, GenericViewSet적용 (카테고리, 옵션)
    path('', include(router.urls)),
    path('', include(category_router.urls)),
\
    path('categories/<int:category_id>/menus/', MenuListCreateView.as_view(), name='menu-list-create'),
    path('categories/<int:category_id>/menus/<int:pk>/', MenuDetailView.as_view(), name='menu-detail'),
    path('order/order_amount/', OrderAmountView.as_view(), name='order-amount'),
    path('orders/', OrderCreateView.as_view(), name='order-create'),
]