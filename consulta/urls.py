from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('accounts/login/', views.logar_usuario, name="logar_usuario"),
    path('sair', views.logout_view, name="logout_view"),
    path('cadastrar_usuario', views.cadastrar_usuario, name="cadastrar_usuario"),
    path('', views.consulta_lista, name='consulta_lista'),
    path('addXML/', views.addXML, name='Adicionar_XML'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)