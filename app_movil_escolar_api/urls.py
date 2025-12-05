from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.bootstrap import VersionView
from app_movil_escolar_api.views import bootstrap
from app_movil_escolar_api.views import auth
from app_movil_escolar_api.views import admins
from app_movil_escolar_api.views import alumnos
from app_movil_escolar_api.views import maestros
from app_movil_escolar_api.views import eventos

urlpatterns = [
    # Django Admin Panel
        path('django-admin/', admin.site.urls),
    #Create Admin
        path('admin/', admins.AdminView.as_view()),
    #Admin Data
        path('lista-admins/', admins.AdminAll.as_view()),
    #Edit Admin
        #path('admins-edit/', admins.AdminsViewEdit.as_view())
    #Create Alumno
        path('alumno/', alumnos.AlumnoView.as_view()),
    #Alumno data
        path('lista-alumnos/', alumnos.AlumnosAll.as_view()),
    #Create Maestro
        path('maestro/', maestros.MaestroView.as_view()),
    #Maestro data
        path('lista-maestros/', maestros.MaestrosAll.as_view()),
    #Crear evento academico
        path('evento-academico/', eventos.EventoAcademicoView.as_view()),
    #Listar eventos academicos
        path('eventos-academicos/', eventos.EventosAcademicosAll.as_view()),
    #Obtener total de eventos academicos
        path('total-eventos/', admins.TotalEventos.as_view()),
    #Obtener total de usuarios
        path('total-usuarios/', admins.TotalUsers.as_view()),
    #Login
        path('login/', auth.CustomAuthToken.as_view()),
    #Logout
        path('logout/', auth.Logout.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
