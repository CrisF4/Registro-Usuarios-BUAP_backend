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
from django.shortcuts import get_object_or_404
import json

class EventosAcademicosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        eventos = EventosAcademicos.objects.all().order_by("id")
        lista = EventoAcademicoSerializer(eventos, many=True).data
        for evento in lista:
            if isinstance(evento, dict) and 'publico_objetivo' in evento:
                try:
                    evento['publico_objetivo'] = json.loads(evento['publico_objetivo'])
                except Exception:
                    evento['publico_objetivo'] = []
        return Response(lista, 200)

class EventoAcademicoView(generics.CreateAPIView):
    # Permisos por método (sobrescribe el comportamiento default)
    # Verifica que el usuario esté autenticado para las peticiones GET, PUT y DELETE
    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return []  # POST no requiere autenticación
    
    #Obtener evento por ID
    #Verifica que el evento esté autenticado
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        evento = get_object_or_404(EventosAcademicos, id = request.GET.get("id"))
        evento = EventoAcademicoSerializer(evento, many=False).data
        # Si todo es correcto, regresamos la información
        return Response(evento, 200)
    
    #Registrar nuevo evento academico
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Serializamos los datos del evento para volverlo de nuevo JSON
        evento = EventoAcademicoSerializer(data=request.data)
        
        if evento.is_valid():
            #Grab event data
            tipo = request.data['tipo_evento']
            nombre = request.data['nombre_evento']
            fecha = request.data['fecha_realizacion']
            hora_inicio = request.data['hora_inicio']
            hora_fin = request.data['hora_fin']
            lugar = request.data['lugar']
            publico = json.dumps(request.data['publico_objetivo'])
            programa = request.data['programa_educativo']
            responsable = request.data['responsable']
            descripcion = request.data['descripcion']
            cupo_maximo = request.data['cupo_maximo']
            #Valida si existe el evento o bien el nombre registrado
            existing_evento = EventosAcademicos.objects.filter(nombre_evento=nombre).first()

            if existing_evento:
                return Response({"message":"Evento "+nombre+", is already taken"},400)
            evento = EventosAcademicos.objects.create( tipo_evento = tipo,
                                        nombre_evento = nombre,
                                        fecha_realizacion = fecha,
                                        hora_inicio = hora_inicio,
                                        hora_fin = hora_fin,
                                        lugar = lugar,
                                        publico_objetivo = publico,
                                        programa_educativo = programa,
                                        responsable = responsable,
                                        descripcion = descripcion,
                                        cupo_maximo = cupo_maximo)

            evento.save()

            # Asignar grupo al evento segun su tipo (OPCIONAL)
            # type_event, created = Group.objects.get_or_create(name=tipo)
            # type_event.user_set.add(evento)
            # evento.save()
            
            return Response({"evento_created_id": evento.id }, 201)

        return Response(evento.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Actualizar datos del evento academico
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        # Primero obtenemos el evento academico a actualizar
        evento = get_object_or_404(EventosAcademicos, id=request.data["id"])
        evento.nombre_evento = request.data["nombre_evento"]
        evento.tipo_evento = request.data["tipo_evento"]
        evento.fecha_realizacion = request.data["fecha_realizacion"]
        evento.hora_inicio = request.data["hora_inicio"]
        evento.hora_fin = request.data["hora_fin"]
        evento.lugar = request.data["lugar"]
        evento.publico_objetivo = json.dumps(request.data["publico_objetivo"])
        evento.programa_educativo = request.data["programa_educativo"]
        evento.responsable = request.data["responsable"]
        evento.descripcion = request.data["descripcion"]
        evento.cupo_maximo = request.data["cupo_maximo"]
        evento.save()
        
        return Response({"message": "Evento actualizado correctamente", "evento": EventoAcademicoSerializer(evento).data}, 200)
    
    # Eliminar evento academico con delete (Borrar realmente)
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        evento = get_object_or_404(EventosAcademicos, id=request.GET.get("id"))
        try:
            evento.delete()
            return Response({"details":"Evento eliminado"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)