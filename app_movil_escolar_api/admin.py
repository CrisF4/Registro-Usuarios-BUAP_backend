from django.contrib import admin
from django.utils.html import format_html
from app_movil_escolar_api.models import *

@admin.register(Administradores)
@admin.register(Alumnos)
@admin.register(Maestros)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "creation", "update")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")

@admin.register(EventosAcademicos)
class EventosAcademicosAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_evento", "tipo_evento", "fecha_realizacion", "responsable", "creation")
    search_fields = ("nombre_evento", "tipo_evento", "lugar")
    list_filter = ("tipo_evento", "fecha_realizacion")

