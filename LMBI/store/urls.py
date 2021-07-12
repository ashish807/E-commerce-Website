from django.urls import path
from . import views
urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>', views.store, name="product_by_category"),
    path('category/<slug:category_slug>/<slug:product_slug>', views.product_detail, name="product_detail"),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('appointments/', views.appointments, name='appointments'),

    path('make_appointments/', views.make_appointments, name='make_appointments'),
    path('remove_appointment/<str:appointment_number>', views.remove_appointment, name='remove_appointment'),
    path('payment_appoinment/', views.payment_appoinment, name='payment_appoinment'),
]