from django.urls import path

from . import views

urlpatterns = [
    path('', views.cadastro_item, name='cadastro_item'),
    path('exibe_rotulo/<int:id_item>', views.exibe_rotulo, name='exibe_rotulo'),
    path('cadastro_medida_caseira/', views.cadastro_medida_caseira, name='cadastro_medida_caseira'),
]