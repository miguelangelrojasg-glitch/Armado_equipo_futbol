from django.urls import path
from django.contrib.auth import views as auth_views # Importamos las vistas nativas de login/logout
from . import views

urlpatterns = [
    # -----------------------------------------
    # NAVEGACIÓN PRINCIPAL
    # -----------------------------------------
    path("", views.index, name="index"),

    # -----------------------------------------
    # AUTENTICACIÓN Y USUARIOS
    # -----------------------------------------
    path("accounts/registro/", views.registro, name="registro"),
    
    # ¡ACÁ ESTÁ EL AJUSTE! Agregamos "registration/" a la ruta del template
    path(
        "accounts/login/", 
        auth_views.LoginView.as_view(template_name="registration/login.html"), 
        name="login"
    ),
    
    # Logout nativo (te redirige al home o login según tu settings.py)
    path(
        "accounts/logout/", 
        auth_views.LogoutView.as_view(), 
        name="logout"
    ),

    # -----------------------------------------
    # GESTIÓN DE LISTAS
    # -----------------------------------------
    path("listas/crear/", views.crear_lista, name="crear_lista"),
    
    path("listas/<int:lista_id>/editar/", views.editar_lista, name="editar_lista"),
    
    path("listas/<int:lista_id>/eliminar/", views.eliminar_lista, name="eliminar_lista"),
    
    path("listas/<int:lista_id>/resumen/", views.resumen_lista, name="resumen_lista"),

    # -----------------------------------------
    # GESTIÓN DE JUGADORES
    # -----------------------------------------
    path(
        "listas/<int:lista_id>/jugadores/agregar/",
        views.agregar_jugador,
        name="agregar_jugador"
    ),

    path(
        "jugadores/<int:jugador_id>/editar/",
        views.editar_jugador,
        name="editar_jugador"
    ),

    path(
        "jugadores/<int:jugador_id>/eliminar/",
        views.eliminar_jugador,
        name="eliminar_jugador"
    ),
# -----------------------------------------
    # ARMADO DE EQUIPOS
    # -----------------------------------------
    path(
        "listas/<int:lista_id>/configurar-equipos/",
        views.configurar_equipos,
        name="configurar_equipos"
    ),

    path(
        "listas/<int:lista_id>/ver-equipos/",
        views.ver_equipos,
        name="ver_equipos"
    ),
]