from django.db.models import *
from django.db import transaction
from app_movil_escolar_api.serializers import UserSerializer
from app_movil_escolar_api.serializers import *
from app_movil_escolar_api.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
import json
from django.shortcuts import get_object_or_404

# Se pueden hacer las cuatro operaciones HTTP (GET, POST, PUT, DELETE), pero solamente una por cada operacion (contenida en las clases).
# Django trabaja con RMO (Relational Model Object) a comparacion de MySQL que trabaja con tablas y consultas SQL.

class AdminAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        admins = Administradores.objects.filter(user__is_active=1).order_by("id")
        lista = AdminSerializer(admins, many=True).data
        return Response(lista, 200)

class AdminView(generics.CreateAPIView):
    # Permisos por método (sobrescribe el comportamiento default)
    # Verifica que el usuario esté autenticado para las peticiones GET, PUT y DELETE
    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return []  # POST no requiere autenticación
    
    # Obtener usuario por ID
    # Verifica que el usuario esté autenticado
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        admin = get_object_or_404(Administradores, id = request.GET.get("id"))
        admin = AdminSerializer(admin, many=False).data
        # Si todo es correcto, regresamos la información
        return Response(admin, 200)
    
    #Registrar nuevo usuario
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Serializamos los datos del administrador para volverlo de nuevo JSON
        user = UserSerializer(data=request.data)
        
        if user.is_valid():
            #Grab user data
            role = request.data['rol']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']
            #Valida si existe el usuario o bien el email registrado
            existing_user = User.objects.filter(email=email).first()

            if existing_user:
                return Response({"message":"Username "+email+", is already taken"},400)

            # Crear usuario
            user = User.objects.create( username = email,
                                        email = email,
                                        first_name = first_name,
                                        last_name = last_name,
                                        is_active = 1)


            user.save()
            #Cifrar la contraseña
            user.set_password(password)
            user.save()

            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            user.save()

            #Almacenar los datos adicionales del administrador
            admin = Administradores.objects.create(user=user,
                                            clave_admin= request.data["clave_admin"],
                                            telefono= request.data["telefono"],
                                            rfc= request.data["rfc"].upper(),
                                            edad= request.data["edad"],
                                            ocupacion= request.data["ocupacion"])
            admin.save()

            return Response({"admin_created_id": admin.id }, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Actualizar datos del administrador
    # TODO: Preguntar si se pueden actualizar email y contraseña.
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        # Primero obtenemos el administrador a actualizar
        admin = get_object_or_404(Administradores, id=request.data["id"])
        admin.clave_admin = request.data["clave_admin"]
        admin.telefono = request.data["telefono"]
        admin.rfc = request.data["rfc"]
        admin.edad = request.data["edad"]
        admin.ocupacion = request.data["ocupacion"]
        admin.save()
        # Actualizamos los datos del usuario asociado (tabla auth_user de Django)
        user = admin.user
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()
        
        return Response({"message": "Administrador actualizado correctamente", "admin": AdminSerializer(admin).data}, 200)
        # return Response(user,200)

    # Eliminar administrador con delete (Borrar realmente)
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        admin = get_object_or_404(Administradores, id=request.GET.get("id"))
        try:
            admin.user.delete()
            return Response({"details":"Administrador eliminado"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)
        
class TotalUsers(generics.CreateAPIView):
    #Contar el total de cada tipo de usuarios
    def get(self, request, *args, **kwargs):
        # TOTAL ADMINISTRADORES
        admin_qs = Administradores.objects.filter(user__is_active=True)
        total_admins = admin_qs.count()

        # TOTAL MAESTROS
        maestros_qs = Maestros.objects.filter(user__is_active=True)
        lista_maestros = MaestroSerializer(maestros_qs, many=True).data

        # Convertir materias_json solo si existen maestros
        for maestro in lista_maestros:
            try:
                maestro["materias_json"] = json.loads(maestro["materias_json"])
            except Exception:
                maestro["materias_json"] = []  # fallback seguro

        total_maestros = maestros_qs.count()

        # TOTAL ALUMNOS
        alumnos_qs = Alumnos.objects.filter(user__is_active=True)
        total_alumnos = alumnos_qs.count()

        # Respuesta final SIEMPRE válida
        return Response(
            {
                "admins": total_admins,
                "maestros": total_maestros,
                "alumnos": total_alumnos
            },
            status=200
        )

# TODO: Rectificar si es necesario que todos los usuarios tengan esta funcionalidad       
# Contar el total de eventos academicos (se deberia de agregar a los demas tipos de usuarios?)
class TotalEventos(generics.CreateAPIView):
    #Contar el total de eventos academicos
    def get(self, request, *args, **kwargs):
        # TOTAL EVENTOS ACADEMICOS
        eventos_qs = EventosAcademicos.objects.all()
        lista_eventos = EventoAcademicoSerializer(eventos_qs, many=True).data
        
        for evento in lista_eventos:
            try:
                evento["publico_objetivo"] = json.loads(evento["publico_objetivo"])
            except Exception:
                evento["publico_objetivo"] = []  # fallback seguro
                
        total_eventos = eventos_qs.count()

        # Respuesta final SIEMPRE válida
        return Response(
            {
                "eventos_academicos": total_eventos
            },
            status=200
        )