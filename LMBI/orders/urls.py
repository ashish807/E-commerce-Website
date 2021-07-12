from django.urls import path
from . import views
urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payment/', views.payment, name='payment'),
    path('makePayment/<int:order_number>/<str:email>/', views.makePayment, name='makePayment'),
    path('place_order_details/', views.place_order_existed_address, name='place_order_details'),
    path('buy_makePayment/<int:order_number>/<str:email>/', views.buy_makePayment, name='buy_makePayment'),
    path('buy_place_order/', views.buy_place_order, name='buy_place_order'),
    path('buy_place_order_existed_address/', views.buy_place_order_existed_address, name='buy_place_order_existed_address'),

    
]