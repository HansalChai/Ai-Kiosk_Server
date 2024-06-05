from django.urls import path
# from django.conf import settings
# from django.conf.urls.static import static

from .views import CategoryListAddView, CategoryUpdateView, CategoryDeleteView, OptionsListAddView, OptionUpdateView, OptionDeleteView, MenuListCreateView, MenuDetailView, OrderCreateView, OrderAmountView

urlpatterns = [
    # 카테고리 관련 API path
    path('categories/', CategoryListAddView.as_view(), name='category-list-add'),
    path('categories/<int:category_id>/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:category_id>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    
    # 옵션 관련 API path
    path('categories/<int:category_id>/options/', OptionsListAddView.as_view(), name='option-list-add'),
    path('categories/<int:category_id>/options/<int:option_id>/', OptionUpdateView.as_view(), name='option-update'),
    path('categories/<int:category_id>/options/<int:option_id>/delete/', OptionDeleteView.as_view(), name='option-delete'),
    
    # 메뉴, 주문 관련 API path
    path('categories/<int:category_id>/menus/', MenuListCreateView.as_view(), name='menu-list-create'),
    path('categories/<int:category_id>/menus/<int:pk>/', MenuDetailView.as_view(), name='menu-detail'),
    path('order/order_amount/', OrderAmountView.as_view(), name='order-amount'),
    path('orders/', OrderCreateView.as_view(), name='order-create'),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
