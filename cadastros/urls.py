from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_item, name='lista_item'),
    path('cadastro_item/', views.cadastro_item, name='cadastro_item'),
    path('lista_item/', views.lista_item, name='lista_item'),
    path('edita_item/<int:id_item>', views.edita_item, name='edita_item'),
    path('exibe_rotulo/<int:id_item>', views.exibe_rotulo, name='exibe_rotulo'),
    path('exclui_item/<int:id_item>/', views.exclui_item, name='exclui_item'),
    path('cadastro_medida_caseira/', views.cadastro_medida_caseira, name='cadastro_medida_caseira'),
]