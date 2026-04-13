from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('processar/', views.processar_dados, name='processar_dados'),
]