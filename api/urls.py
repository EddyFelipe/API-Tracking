
# django REST framework
from rest_framework.routers import DefaultRouter

# django
from django.urls import path, include

# views
from api.views import paquete, users,reporte

router = DefaultRouter()

router.register(r'paquetes', paquete.PaqueteViewSet, basename='paquete')
router.register(r'users', users.UserViewSet, basename='user')
router.register(
    r'cliente/paquetes', 
    reporte.ReporteClientViewSet, 
    basename='reportecliente'
)
router.register(
    r'admin/paquetes', 
    reporte.ReporteAdminntViewSet, 
    basename='reporteadmin'
)

urlpatterns = [
    path('', include(router.urls))
]