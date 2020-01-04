from django.urls import path,  re_path
from . import views


app_name = 'store'

urlpatterns = [
    path('', views.store, name='index'),
    path('book/<int:book_id>/', views.book_details, name='book_details'),

    path('add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),

    path('checkout/<str:processor>/', views.checkout, name='checkout'),
    path('process/<str:processor>/', views.process_order, name='process_order'),
    path('order_error/', views.order_error, name='order_error'),
    path('complete_order/<str:processor>/', views.complete_order, name='complete_order'),
]
