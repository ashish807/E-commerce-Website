from django.urls import path
from . import views

urlpatterns = [

    path('', views.landing, name='site-landing'),
    # path('', views.landing, name='home'),
    path('about/', views.about, name='site-about'),
    path('test/', views.test, name='TESTER'),

    path('bloodTest/home', views.btInfo, name='btMain'),
    path('bloodTest/covid19', views.cvoid19, name='btCovid'),
    path('bloodTest/cbc', views.cbc, name='btCBC'),
    path('bloodTest/cholestrol', views.cholestrol, name='btCholestrol')
]