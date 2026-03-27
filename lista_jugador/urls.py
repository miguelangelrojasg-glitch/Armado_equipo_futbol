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
    
    # Conectamos el login nativo de Django con tu plantilla personalizada
    path(
        "accounts/login/", 
        auth_views.LoginView.as_view(template_name="login.html"), 
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
    # Detalle menor: unifiqué a plural ("jugadores/agregar") para que quede más 
    # prolijo con el resto, pero el 'name' sigue siendo el mismo.
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
]