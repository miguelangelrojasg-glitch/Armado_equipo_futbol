from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .models import AtributoEspecial, Jugador, ListaJugadores


# ------------------------
# UTILIDAD
# ------------------------

def to_int(value, default=1):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


# ------------------------
# HOME
# ------------------------

@login_required
def index(request):
    listas = ListaJugadores.objects.filter(usuario=request.user).order_by("-id")
    return render(
        request,
        "home.html",
        {
            "listas": listas,
        }
    )


# ------------------------
# REGISTRO
# ------------------------

def registro(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/registro.html",
        {"form": form}
    )


# ------------------------
# CREAR LISTA
# ------------------------

@login_required
def crear_lista(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")

        try:
            cantidad = int(request.POST.get("cantidad"))
        except (TypeError, ValueError):
            messages.error(request, "Ingresá un número válido de jugadores.")
            return redirect("crear_lista")

        lista = ListaJugadores.objects.create(
            usuario=request.user,
            nombre=nombre,
            cantidad_jugadores=cantidad
        )

        messages.success(request, "Lista creada correctamente.")
        return redirect("agregar_jugador", lista_id=lista.id)

    return render(request, "listas/crear_lista.html")

# ------------------------
# EDITAR LISTA
# ------------------------

@login_required
def editar_lista(request, lista_id):
    lista = get_object_or_404(
        ListaJugadores,
        id=lista_id,
        usuario=request.user
    )

    if request.method == "POST":
        nombre = request.POST.get("nombre")

        try:
            cantidad = int(request.POST.get("cantidad"))
        except (TypeError, ValueError):
            messages.error(request, "Ingresá una cantidad válida de jugadores.")
            return redirect("editar_lista", lista_id=lista.id)

        # No permitir que la nueva cantidad sea menor a los jugadores ya cargados
        jugadores_cargados = lista.jugadores.count()
        if cantidad < jugadores_cargados:
            messages.error(
                request,
                f"No podés establecer {cantidad} jugadores porque ya cargaste {jugadores_cargados}."
            )
            return redirect("editar_lista", lista_id=lista.id)

        lista.nombre = nombre
        lista.cantidad_jugadores = cantidad

        try:
            lista.full_clean()
            lista.save()
            messages.success(request, "Lista actualizada correctamente.")
            return redirect("resumen_lista", lista_id=lista.id)
        except Exception as e:
            messages.error(request, str(e))
            return redirect("editar_lista", lista_id=lista.id)

    return render(
        request,
        "listas/editar_lista.html",
        {
            "lista": lista,
        }
    )


# ------------------------
# ELIMINAR LISTA
# ------------------------

@login_required
def eliminar_lista(request, lista_id):
    lista = get_object_or_404(
        ListaJugadores,
        id=lista_id,
        usuario=request.user
    )

    if request.method == "POST":
        lista.delete()
        messages.success(request, "Lista eliminada correctamente.")
        return redirect("index")

    return render(
        request,
        "listas/eliminar_lista.html",
        {
            "lista": lista,
        }
    )

# ------------------------
# AGREGAR JUGADOR
# ------------------------

@login_required
def agregar_jugador(request, lista_id):
    lista = get_object_or_404(
        ListaJugadores,
        id=lista_id,
        usuario=request.user
    )

    # Si ya completó la cantidad, va al resumen
    if lista.jugadores.count() >= lista.cantidad_jugadores:
        return redirect("resumen_lista", lista_id=lista.id)

    # Campos por rubro para usar en el template
    campos_ataque = [
        "finalizacion",
        "remate_cabeza",
        "desmarque",
        "vision_juego",
        "tiros_lejanos",
        "penales",
        "saques_esquina",
        "tiros_libres",
    ]

    campos_defensa = [
        "entradas",
        "marcaje",
        "anticipacion",
        "colocacion",
        "intercepciones",
        "despeje",
    ]

    campos_tecnica = [
        "control_balon",
        "regate",
        "pases_cortos",
        "pases_largos",
        "centros",
        "efecto",
        "tecnica_disparo",
        "juego_espaldas",
    ]

    campos_fisico = [
        "velocidad",
        "aceleracion",
        "resistencia",
        "fuerza",
        "salto",
        "agilidad",
        "equilibrio",
        "potencia_salto",
    ]

    campos_arquero = [
        "reflejos",
        "estirada",
        "manejo_area",
        "blocaje",
        "saque_meta",
        "saque_mano",
        "uno_contra_uno",
        "comunicacion",
    ]

    if request.method == "POST":
        jugador = Jugador(
            lista=lista,
            nombre=request.POST.get("nombre"),
            posicion_principal=request.POST.get("posicion_principal"),
            posicion_secundaria=request.POST.get("posicion_secundaria") or None,

            # ATAQUE
            finalizacion=to_int(request.POST.get("finalizacion")),
            remate_cabeza=to_int(request.POST.get("remate_cabeza")),
            desmarque=to_int(request.POST.get("desmarque")),
            vision_juego=to_int(request.POST.get("vision_juego")),
            tiros_lejanos=to_int(request.POST.get("tiros_lejanos")),
            penales=to_int(request.POST.get("penales")),
            saques_esquina=to_int(request.POST.get("saques_esquina")),
            tiros_libres=to_int(request.POST.get("tiros_libres")),

            # DEFENSA
            entradas=to_int(request.POST.get("entradas")),
            marcaje=to_int(request.POST.get("marcaje")),
            anticipacion=to_int(request.POST.get("anticipacion")),
            colocacion=to_int(request.POST.get("colocacion")),
            intercepciones=to_int(request.POST.get("intercepciones")),
            despeje=to_int(request.POST.get("despeje")),

            # TECNICA
            control_balon=to_int(request.POST.get("control_balon")),
            regate=to_int(request.POST.get("regate")),
            pases_cortos=to_int(request.POST.get("pases_cortos")),
            pases_largos=to_int(request.POST.get("pases_largos")),
            centros=to_int(request.POST.get("centros")),
            efecto=to_int(request.POST.get("efecto")),
            tecnica_disparo=to_int(request.POST.get("tecnica_disparo")),
            juego_espaldas=to_int(request.POST.get("juego_espaldas")),

            # FISICO
            velocidad=to_int(request.POST.get("velocidad")),
            aceleracion=to_int(request.POST.get("aceleracion")),
            resistencia=to_int(request.POST.get("resistencia")),
            fuerza=to_int(request.POST.get("fuerza")),
            salto=to_int(request.POST.get("salto")),
            agilidad=to_int(request.POST.get("agilidad")),
            equilibrio=to_int(request.POST.get("equilibrio")),
            potencia_salto=to_int(request.POST.get("potencia_salto")),

            # ARQUERO
            reflejos=to_int(request.POST.get("reflejos")),
            estirada=to_int(request.POST.get("estirada")),
            manejo_area=to_int(request.POST.get("manejo_area")),
            blocaje=to_int(request.POST.get("blocaje")),
            saque_meta=to_int(request.POST.get("saque_meta")),
            saque_mano=to_int(request.POST.get("saque_mano")),
            uno_contra_uno=to_int(request.POST.get("uno_contra_uno")),
            comunicacion=to_int(request.POST.get("comunicacion")),
        )

        jugador.save()
        jugador.recalcular_nivel()

        messages.success(request, "Jugador creado correctamente.")
        return redirect("editar_jugador", jugador_id=jugador.id)

    return render(
        request,
        "jugadores/agregar_jugador.html",
        {
            "lista": lista,
            "campos_ataque": campos_ataque,
            "campos_defensa": campos_defensa,
            "campos_tecnica": campos_tecnica,
            "campos_fisico": campos_fisico,
            "campos_arquero": campos_arquero,
            "jugadores_actuales": lista.jugadores.count(),
            "cantidad_total": lista.cantidad_jugadores,
        }
    )


# ------------------------
# EDITAR JUGADOR
# ------------------------

@login_required
def editar_jugador(request, jugador_id):
    jugador = get_object_or_404(
        Jugador,
        id=jugador_id,
        lista__usuario=request.user
    )
    lista = jugador.lista

    # Solo atributos especiales de la posición principal
    atributos_especiales = AtributoEspecial.objects.filter(
        posicion=jugador.posicion_principal
    )

    if request.method == "POST":
        atributos_ids = request.POST.getlist("atributos_especiales")

        if len(atributos_ids) > 2:
            messages.error(request, "Podés seleccionar hasta 2 atributos especiales.")
            return redirect("editar_jugador", jugador_id=jugador.id)

        seleccionados = AtributoEspecial.objects.filter(
            id__in=atributos_ids,
            posicion=jugador.posicion_principal
        )

        jugador.atributos_especiales.set(seleccionados)
        jugador.recalcular_nivel()

        jugadores_actuales = Jugador.objects.filter(lista=lista).count()

        if jugadores_actuales >= lista.cantidad_jugadores:
            messages.success(request, "Lista completa. Pasando al resumen.")
            return redirect("resumen_lista", lista_id=lista.id)

        return redirect("agregar_jugador", lista_id=lista.id)

    return render(
        request,
        "jugadores/editar_jugador.html",
        {
            "jugador": jugador,
            "atributos_especiales": atributos_especiales,
        }
    )


# ------------------------
# RESUMEN DE LISTA
# ------------------------

@login_required
def resumen_lista(request, lista_id):
    lista = get_object_or_404(
        ListaJugadores,
        id=lista_id,
        usuario=request.user
    )

    if lista.jugadores.count() < lista.cantidad_jugadores:
        return redirect("agregar_jugador", lista_id=lista.id)

    jugadores = lista.jugadores.all().order_by("nombre")
    nivel_total = sum(j.nivel_general for j in jugadores)

    return render(
        request,
        "jugadores/resumen_lista.html",
        {
            "lista": lista,
            "jugadores": jugadores,
            "nivel_total": nivel_total,
        }
    )


# ------------------------
# ELIMINAR JUGADOR
# ------------------------

@login_required
def eliminar_jugador(request, jugador_id):
    jugador = get_object_or_404(
        Jugador,
        id=jugador_id,
        lista__usuario=request.user
    )
    lista = jugador.lista
    jugador.delete()

    messages.success(request, "Jugador eliminado correctamente.")
    return redirect("agregar_jugador", lista_id=lista.id)