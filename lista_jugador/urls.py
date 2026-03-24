from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.index, name="index"),

    # Registro
    path("accounts/registro/", views.registro, name="registro"),

    # Crear lista
    path("listas/crear/", views.crear_lista, name="crear_lista"),

    # Editar lista
    path("listas/<int:lista_id>/editar/", views.editar_lista, name="editar_lista"),

    # Eliminar lista
    path("listas/<int:lista_id>/eliminar/", views.eliminar_lista, name="eliminar_lista"),

    # Agregar jugador a una lista
    path(
        "listas/<int:lista_id>/jugadores/agregar/",
        views.agregar_jugador,
        name="agregar_jugador"
    ),

    # Editar jugador
    path(
        "jugadores/<int:jugador_id>/editar/",
        views.editar_jugador,
        name="editar_jugador"
    ),

    # Resumen de la lista
    path(
        "listas/<int:lista_id>/resumen/",
        views.resumen_lista,
        name="resumen_lista"
    ),

    # Eliminar jugador
    path(
        "jugadores/<int:jugador_id>/eliminar/",
        views.eliminar_jugador,
        name="eliminar_jugador"
    ),
]