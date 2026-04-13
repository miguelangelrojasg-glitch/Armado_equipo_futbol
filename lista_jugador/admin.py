from django.contrib import admin
from .models import AtributoEspecial, Jugador, ListaJugadores

@admin.register(AtributoEspecial)
class AtributoEspecialAdmin(admin.ModelAdmin):
    # Qué columnas mostrar en la lista
    list_display = ('nombre', 'posicion')
    # Por qué campos se puede buscar
    search_fields = ('nombre', 'posicion')
    # Filtros laterales
    list_filter = ('posicion',)

@admin.register(ListaJugadores)
class ListaJugadoresAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'cantidad_jugadores')
    search_fields = ('nombre', 'usuario__username')
    list_filter = ('usuario',)

@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'posicion_principal', 'lista', 'nivel_general')
    search_fields = ('nombre', 'lista__nombre')
    list_filter = ('posicion_principal', 'lista')
    # Mostrar el nivel como solo lectura ya que se calcula automáticamente
    readonly_fields = ('nivel_general',)