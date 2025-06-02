from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .admin import admin_site as custom_admin_site

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('client/login/', views.client_login, name='client_login'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('membres/', include(('gestion_membres.urls', 'membres'), namespace='membres')),
    path('activites/', include(('gestion_activites.urls', 'activites'), namespace='activites')),
    path('coachs/', include(('gestion_coachs.urls', 'coachs'), namespace='coachs')),
    path('salles/', include(('gestion_salles.urls', 'salles'), namespace='salles')),
    path('reservations/', include(('gestion_reservations.urls', 'reservations'), namespace='reservations')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)