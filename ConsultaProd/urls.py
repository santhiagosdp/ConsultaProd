from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from consulta import views as consulta_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('consulta.urls')),
]
