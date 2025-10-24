from django.urls import path
from . import views

urlpatterns = [
#TESTING
    path('spms/performancemanagement', views.performance_management, name='performance-mgt'),
    path('spms/performancedetails', views.performance_details, name='performance-details'),
    path('spms/performancemodal', views.performance_modal, name='performance-modal'),
    
    path('spms/monitoringtool', views.monitoringtool, name='monitoringtool'),
]