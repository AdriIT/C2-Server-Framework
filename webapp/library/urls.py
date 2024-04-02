from django.urls import path
from . import views
from .views import DeviceListView

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('devices', DeviceListView.as_view(), name='devices'),
    path('devices/<str:device_username>', views.reverse_shell, name='reverse_shell')
]