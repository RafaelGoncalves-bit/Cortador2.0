from django.urls import path
from . import views
from . views import chrome_devtools


urlpatterns = [
    path('', views.index, name='index'),
    path('processar/', views.processar_dados, name='processar_dados'),
    path('.well-known/appspecific/com.chrome.devtools.json', chrome_devtools),
    path('login-google/', views.login_google),
    path('oauth2callback/', views.oauth2callback),
]