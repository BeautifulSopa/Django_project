from django.urls import path
from .views import (
    lista_produtos,
    user_login,
    user_signup,
    user_logout,
    add_to_cart,
    view_cart,
    remove_from_cart,
    product_detail  # Import the product_detail view here
)

urlpatterns = [
    path('', lista_produtos, name='lista_produtos'),
    path('login/', user_login, name='user_login'),
    path('signup/', user_signup, name='user_signup'),
    path('logout/', user_logout, name='logout'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),  # Use product_detail directly
]
