from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_principal, name='menu_principal'),
    path('gerar-tabela/', views.gerar_tabela_consumo_view, name='gerar_tabela_consumo'),
    path('gerar-tabela/process/', views.gerar_tabela_consumo_process, name='gerar_tabela_consumo_process'),
    path('exportar-xlsx/', views.exportar_xlsx, name='exportar_xlsx'),
    path('teste-bombeamento/', views.teste_bombeamento_view, name='teste_bombeamento'),
    path('teste-bombeamento/process/', views.teste_bombeamento_process, name='teste_bombeamento_process'),
    path('teste-bombeamento/exportar-xlsx/', views.exportar_teste_xlsx, name='exportar_teste_xlsx'),
]
