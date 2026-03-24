from __future__ import annotations

from dataclasses import dataclass
import random
from typing import List, Tuple, Dict, Optional


ENFOQUES = ("EQUILIBRADO", "OFENSIVO", "DEFENSIVO")


# ------------------------
# PROMEDIOS POR RUBRO
# ------------------------

def promedio_ataque(j) -> float:
    return (
        j.finalizacion +
        j.remate_cabeza +
        j.desmarque +
        j.vision_juego +
        j.tiros_lejanos +
        j.penales +
        j.saques_esquina +
        j.tiros_libres
    ) / 8


def promedio_defensa(j) -> float:
    return (
        j.entradas +
        j.marcaje +
        j.anticipacion +
        j.colocacion +
        j.intercepciones +
        j.despeje
    ) / 6


def promedio_tecnica(j) -> float:
    return (
        j.control_balon +
        j.regate +
        j.pases_cortos +
        j.pases_largos +
        j.centros +
        j.efecto +
        j.tecnica_disparo +
        j.juego_espaldas
    ) / 8


def promedio_fisico(j) -> float:
    return (
        j.velocidad +
        j.aceleracion +
        j.resistencia +
        j.fuerza +
        j.salto +
        j.agilidad +
        j.equilibrio +
        j.potencia_salto
    ) / 8


def promedio_arquero(j) -> float:
    return (
        j.reflejos +
        j.estirada +
        j.manejo_area +
        j.blocaje +
        j.saque_meta +
        j.saque_mano +
        j.uno_contra_uno +
        j.comunicacion
    ) / 8


# ------------------------
# UTILIDADES
# ------------------------

def gk_score(j) -> float:
    return promedio_arquero(j)


def puede_jugar_en(jugador, posicion: str) -> bool:
    return (
        jugador.posicion_principal == posicion
        or jugador.posicion_secundaria == posicion
    )


def style_rating(j, enfoque: str) -> float:
    """
    Rating para repartir jugadores según enfoque del equipo.
    """
    base = float(j.nivel_general or 0)
    atk = promedio_ataque(j)
    deff = promedio_defensa(j)
    tec = promedio_tecnica(j)
    fis = promedio_fisico(j)

    if enfoque == "EQUILIBRADO":
        return base

    if enfoque == "OFENSIVO":
        return base + (
            (atk * 0.6) +
            (tec * 0.25) +
            (fis * 0.15) -
            (deff * 0.2)
        ) * 0.45

    if enfoque == "DEFENSIVO":
        return base + (
            (deff * 0.6) +
            (fis * 0.25) +
            (tec * 0.15) -
            (atk * 0.2)
        ) * 0.45

    return base


def role_score(j, rol: str) -> float:
    """
    Puntaje del jugador para una línea específica.
    Se usa principal y secundaria indirectamente.
    """
    if rol == "DEF":
        score = (promedio_defensa(j) * 0.6) + (promedio_fisico(j) * 0.4)
        if j.posicion_principal == "DEF":
            score += 1.0
        elif j.posicion_secundaria == "DEF":
            score += 0.5
        return score

    if rol == "MED":
        score = (
            (promedio_tecnica(j) * 0.45) +
            (promedio_fisico(j) * 0.25) +
            (promedio_ataque(j) * 0.15) +
            (promedio_defensa(j) * 0.15)
        )
        if j.posicion_principal == "MED":
            score += 1.0
        elif j.posicion_secundaria == "MED":
            score += 0.5
        return score

    if rol == "DEL":
        score = (promedio_ataque(j) * 0.65) + (promedio_tecnica(j) * 0.35)
        if j.posicion_principal == "DEL":
            score += 1.0
        elif j.posicion_secundaria == "DEL":
            score += 0.5
        return score

    return float(j.nivel_general or 0)


def suggest_formation(players_per_team: int) -> Tuple[int, int, int]:
    """
    Devuelve (DEF, MED, DEL) asumiendo 1 arquero.
    """
    campo = max(players_per_team - 1, 0)

    presets: Dict[int, Tuple[int, int, int]] = {
        1: (0, 0, 1),   # 2 vs 2
        2: (1, 0, 1),   # 3 vs 3
        3: (1, 1, 1),   # 4 vs 4
        4: (1, 2, 1),   # 5 vs 5
        5: (2, 2, 1),   # 6 vs 6
        6: (2, 2, 2),   # 7 vs 7
        7: (3, 2, 2),   # 8 vs 8
        8: (3, 3, 2),   # 9 vs 9
        9: (4, 3, 2),   # 10 vs 10
        10: (4, 4, 2),  # 11 vs 11
    }

    if campo in presets:
        return presets[campo]

    med = campo // 2
    resto = campo - med
    deff = resto // 2
    ataque = campo - med - deff
    return (deff, med, ataque)


# ------------------------
# RESULTADO
# ------------------------

@dataclass
class TeamResult:
    equipo_a: list
    equipo_b: list
    rating_a: float
    rating_b: float
    enfoque_a: str
    enfoque_b: str
    form_a: Tuple[int, int, int]
    form_b: Tuple[int, int, int]
    gk_a_id: Optional[int]
    gk_b_id: Optional[int]
    gk_a_is_improvised: bool
    gk_b_is_improvised: bool


# ------------------------
# ARMADO
# ------------------------

def armar_equipos(
    jugadores: List,
    players_per_team: int,
    enfoque_a: str = "EQUILIBRADO",
    enfoque_b: str = "EQUILIBRADO",
    seed: int = 1,
) -> TeamResult:
    if enfoque_a not in ENFOQUES:
        enfoque_a = "EQUILIBRADO"
    if enfoque_b not in ENFOQUES:
        enfoque_b = "EQUILIBRADO"

    rnd = random.Random(seed)
    jugadores = list(jugadores)

    # Re-armado moderado
    JITTER = 0.12

    def sort_key(j):
        nivel = float(j.nivel_general or 0)
        ruido = rnd.uniform(-JITTER, JITTER)
        return nivel + ruido

    jugadores.sort(key=sort_key, reverse=True)

    # ------------------------
    # FORMACIONES OBJETIVO
    # ------------------------

    form_a = suggest_formation(players_per_team)
    form_b = suggest_formation(players_per_team)

    objetivo_a = {"DEF": form_a[0], "MED": form_a[1], "DEL": form_a[2]}
    objetivo_b = {"DEF": form_b[0], "MED": form_b[1], "DEL": form_b[2]}

    # ------------------------
    # DETECTAR ARQUEROS
    # ------------------------

    reales_arq = [j for j in jugadores if j.posicion_principal == "ARQ"]
    no_arq = [j for j in jugadores if j.posicion_principal != "ARQ"]

    equipo_a: List = []
    equipo_b: List = []
    rating_a = 0.0
    rating_b = 0.0

    gk_a_id = None
    gk_b_id = None
    gk_a_is_improvised = False
    gk_b_is_improvised = False

    if len(reales_arq) >= 2:
        gk1, gk2 = reales_arq[0], reales_arq[1]

        equipo_a.append(gk1)
        rating_a += style_rating(gk1, enfoque_a)
        gk_a_id = gk1.id

        equipo_b.append(gk2)
        rating_b += style_rating(gk2, enfoque_b)
        gk_b_id = gk2.id

        restantes = [j for j in jugadores if j.id not in {gk1.id, gk2.id}]

    elif len(reales_arq) == 1:
        gk_real = reales_arq[0]

        equipo_a.append(gk_real)
        rating_a += style_rating(gk_real, enfoque_a)
        gk_a_id = gk_real.id

        if no_arq:
            supl = max(no_arq, key=gk_score)
            equipo_b.append(supl)
            rating_b += style_rating(supl, enfoque_b)
            gk_b_id = supl.id
            gk_b_is_improvised = True
            restantes = [j for j in jugadores if j.id not in {gk_real.id, supl.id}]
        else:
            restantes = [j for j in jugadores if j.id != gk_real.id]

    else:
        if len(no_arq) >= 2:
            orden = sorted(no_arq, key=gk_score, reverse=True)
            s1, s2 = orden[0], orden[1]

            equipo_a.append(s1)
            rating_a += style_rating(s1, enfoque_a)
            gk_a_id = s1.id
            gk_a_is_improvised = True

            equipo_b.append(s2)
            rating_b += style_rating(s2, enfoque_b)
            gk_b_id = s2.id
            gk_b_is_improvised = True

            restantes = [j for j in jugadores if j.id not in {s1.id, s2.id}]
        else:
            restantes = jugadores[:]

    # ------------------------
    # AYUDA PARA CONTAR LÍNEAS
    # ------------------------

    def contar_lineas(equipo):
        return {
            "DEF": len([j for j in equipo if puede_jugar_en(j, "DEF") and j.id not in {gk_a_id, gk_b_id}]),
            "MED": len([j for j in equipo if puede_jugar_en(j, "MED") and j.id not in {gk_a_id, gk_b_id}]),
            "DEL": len([j for j in equipo if puede_jugar_en(j, "DEL") and j.id not in {gk_a_id, gk_b_id}]),
        }

    # ------------------------
    # BALANCE DEL RESTO
    # ------------------------

    for j in restantes:
        if len(equipo_a) >= players_per_team:
            equipo_b.append(j)
            rating_b += style_rating(j, enfoque_b)
            continue

        if len(equipo_b) >= players_per_team:
            equipo_a.append(j)
            rating_a += style_rating(j, enfoque_a)
            continue

        lineas_a = contar_lineas(equipo_a)
        lineas_b = contar_lineas(equipo_b)

        # Detectar rol más natural del jugador
        rol_preferido = max(
            ["DEF", "MED", "DEL"],
            key=lambda rol: role_score(j, rol)
        )

        # Penalización si ese equipo ya está lleno en esa línea
        penal_a = 0
        penal_b = 0

        if lineas_a[rol_preferido] >= objetivo_a[rol_preferido]:
            penal_a = 1.5
        if lineas_b[rol_preferido] >= objetivo_b[rol_preferido]:
            penal_b = 1.5

        ra = style_rating(j, enfoque_a) + penal_a
        rb = style_rating(j, enfoque_b) + penal_b

        if (rating_a + ra) <= (rating_b + rb):
            equipo_a.append(j)
            rating_a += style_rating(j, enfoque_a)
        else:
            equipo_b.append(j)
            rating_b += style_rating(j, enfoque_b)

    equipo_a = equipo_a[:players_per_team]
    equipo_b = equipo_b[:players_per_team]

    return TeamResult(
        equipo_a=equipo_a,
        equipo_b=equipo_b,
        rating_a=rating_a,
        rating_b=rating_b,
        enfoque_a=enfoque_a,
        enfoque_b=enfoque_b,
        form_a=form_a,
        form_b=form_b,
        gk_a_id=gk_a_id,
        gk_b_id=gk_b_id,
        gk_a_is_improvised=gk_a_is_improvised,
        gk_b_is_improvised=gk_b_is_improvised,
    )