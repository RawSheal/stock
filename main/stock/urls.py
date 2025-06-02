from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('receipt/', views.receipt, name='receipt'),
    path('issued/', views.issued, name='issued'),
    path('production_issued/', views.production_issued, name='production_issued'),
    path('production_return/', views.production_return, name='production_return'),
    path('production_report/', views.production_report, name='production_report'),
    path('receipt_edit/<int:pk>/', views.receipt_edit, name='receipt_edit'),
    path('issued_edit/<int:pk>/', views.issued_edit, name='issued_edit'),
    path('production_issued_edit/<int:pk>/', views.production_issued_edit, name='production_issued_edit'),
    path('production_return_edit/<int:pk>/', views.production_return_edit, name='production_return_edit'),
]
    
