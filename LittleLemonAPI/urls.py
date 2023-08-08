from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items/', views.menu_items),
    path('menu-items/<int:id>', views.single_item),
    path('secret/', views.secret),
    # following endpoint accepts only HTTP POST calls
    path('api-token-auth/', obtain_auth_token),
    path('manager-view/', views.manager_view),
    path('throttle-check/', views.throttle_check),
    path('throttle-check-auth/', views.throttle_check_auth),
    path('groups/manager/users/', views.managers),
    path('groups/manager/users/<int:user_id>', views.single_user),
    path('groups/delivery-crew/users', views.delivery_crew),
    path('groups/delivery-crew/users/<int:user_id>', views.single_delivery_crew),
    path('me/', views.me),
    path('cart/menu-items/', views.cart_items),
    path('orders/', views.order),
    path('orders/<int:order_id>', views.single_order),
]
