from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('accounts/login/', views.logar_usuario, name="logar_usuario"),
    path('sair', views.logout_view, name="logout_view"),
    path('cadastrar_usuario/', views.cadastrar_usuario, name="cadastrar_usuario"),
    path('', views.consulta_lista, name='consulta_lista'),
    path('mercado/<int:id>', views.consulta_lista_mercado),
    path('add1/', views.addXML, name='Adicionar_XML'),
    path('add1/', views.addXML, name='Adicionar_XML'),
    path('sudo apt-get install python3-pip/', views.addFotoNFC, name='Adicionar_FotoNFC'),
    
    path('qrcode/', views.addqrcode, name='adicionar_qrcode'),
    path('addlote/', views.addLote, name='adicionar_Lote'),
    path('uploadlote/', views.uploadlote, name='Upload_Lote_Do_PC'),
    path('acessos/', views.acessos, name='acessos'),
    path('teste/', views.teste, name='teste'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)