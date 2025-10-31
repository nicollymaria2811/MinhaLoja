from django.urls import path
from django.shortcuts import redirect
from . import views

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('', redirect_to_login, name='conta_home'),
    path('registrar/', views.registrar, name='registrar'),
    path('minha-conta/', views.minha_conta, name='minha_conta'),
    path('excluir-conta/', views.excluir_conta, name='excluir_conta'),
]