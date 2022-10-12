from django.urls import path

from . import views

urlpatterns = [
    path('', views.cadastro, name='cadastro'),
    path('cadastro_composto', views.cadastro_composto, name='cadastro_composto'),
    path('cadastro_medida_caseira/', views.cadastro_medida_caseira, name='cadastro_medida_caseira'),
]