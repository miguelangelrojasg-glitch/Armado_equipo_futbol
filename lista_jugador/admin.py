from django.contrib import admin

from .models import ListaJugadores, Jugador, AtributoEspecial


@admin.register(ListaJugadores)
class ListaJugadoresAdmin(admin.ModelAdmin):
    list_display = ("nombre", "usuario", "cantidad_jugadores", "fecha_creacion")
    search_fields = ("nombre", "usuario__username")
    list_filter = ("cantidad_jugadores", "fecha_creacion")


@admin.register(AtributoEspecial)
class AtributoEspecialAdmin(admin.ModelAdmin):
    list_display = ("nombre", "posicion", "rubro", "modificador")
    search_fields = ("nombre", "descripcion")
    list_filter = ("posicion", "rubro")


@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "lista",
        "posicion_principal",
        "posicion_secundaria",
        "nivel_general",
        "fecha_creacion",
    )
    search_fields = ("nombre", "lista__nombre")
    list_filter = ("posicion_principal", "posicion_secundaria", "fecha_creacion")
    filter_horizontal = ("atributos_especiales",)