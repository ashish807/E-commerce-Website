from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('activate/<uidb64>/<token>/', views.activate , name='activate'),
    
    path('', views.dashboard, name='dashbord'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgetPassword/', views.forgetPassword, name = 'forgetPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate , name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name = 'resetPassword'),
    path('my_orders/', views.my_orders, name = 'my_orders'),
    path('edit_profile/', views.edit_profile, name = 'edit_profile'),
    path('change_password/', views.change_password, name = 'change_password'),
    path('order_detail/<int:order_id>/', views.order_detail, name = 'order_detail'),

    path('add_address/', views.add_address, name = 'add_address'),
    
    path('select_address/<int:number>/', views.select_address, name = 'select_address'),
    path('change_address/<int:address_id>/<int:number>/', views.change_address, name = 'change_address'),
    path('delete_address/<int:address_id>/<int:number>/', views.delete_address, name = 'delete_address'),
    path('feedback/', views.feedback, name='feedback'),
    path('enquiry/', views.enquiry, name='enquiry'),
]