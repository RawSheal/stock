from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('receipt/', views.receipt, name='receipt'),
    path('issued/', views.issued, name='issued'),
    path('production_issued/', views.production_issued, name='production_issued'),
    path('production_return/', views.production_return, name='production_return'),
    path('production_report/', views.production_report, name='production_report'),
]
    
