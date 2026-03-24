from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


# ------------------------
# CONSTANTES
# ------------------------

POSICIONES = [
    ("ARQ", "Arquero"),
    ("DEF", "Defensor"),
    ("MED", "Mediocampista"),
    ("DEL", "Delantero"),
]

RUBROS = [
    ("ATAQUE", "Ataque"),
    ("DEFENSA", "Defensa"),
    ("TECNICA", "Técnica"),
    ("FISICO", "Físico"),
    ("ARQUERO", "Arquero"),
]

CANTIDADES_VALIDAS = [10, 12, 14, 16, 18, 20, 22]


# ------------------------
# LISTA
# ------------------------

class ListaJugadores(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listas"
    )
    nombre = models.CharField(max_length=100)
    cantidad_jugadores = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.cantidad_jugadores not in CANTIDADES_VALIDAS:
            raise ValidationError("Cantidad inválida de jugadores.")

    def __str__(self):
        return self.nombre


# ------------------------
# ATRIBUTOS ESPECIALES
# ------------------------

class AtributoEspecial(models.Model):
    nombre = models.CharField(max_length=100)
    posicion = models.CharField(max_length=3, choices=POSICIONES)
    rubro = models.CharField(max_length=10, choices=RUBROS)
    descripcion = models.TextField()
    modificador = models.FloatField(help_text="Porcentaje (ej: 5 = 5%)")

    def __str__(self):
        return f"{self.nombre} ({self.get_posicion_display()})"


# ------------------------
# JUGADOR
# ------------------------

class Jugador(models.Model):
    lista = models.ForeignKey(
        ListaJugadores,
        on_delete=models.CASCADE,
        related_name="jugadores"
    )

    nombre = models.CharField(max_length=100)

    posicion_principal = models.CharField(max_length=3, choices=POSICIONES)
    posicion_secundaria = models.CharField(
        max_length=3,
        choices=POSICIONES,
        blank=True,
        null=True
    )

    # ------------------------
    # ATAQUE
    # ------------------------
    finalizacion = models.PositiveIntegerField()
    remate_cabeza = models.PositiveIntegerField()
    desmarque = models.PositiveIntegerField()
    vision_juego = models.PositiveIntegerField()
    tiros_lejanos = models.PositiveIntegerField()
    penales = models.PositiveIntegerField()
    saques_esquina = models.PositiveIntegerField()
    tiros_libres = models.PositiveIntegerField()

    # ------------------------
    # DEFENSA
    # ------------------------
    entradas = models.PositiveIntegerField()
    marcaje = models.PositiveIntegerField()
    anticipacion = models.PositiveIntegerField()
    colocacion = models.PositiveIntegerField()
    intercepciones = models.PositiveIntegerField()
    despeje = models.PositiveIntegerField()

    # ------------------------
    # TECNICA
    # ------------------------
    control_balon = models.PositiveIntegerField()
    regate = models.PositiveIntegerField()
    pases_cortos = models.PositiveIntegerField()
    pases_largos = models.PositiveIntegerField()
    centros = models.PositiveIntegerField()
    efecto = models.PositiveIntegerField()
    tecnica_disparo = models.PositiveIntegerField()
    juego_espaldas = models.PositiveIntegerField()

    # ------------------------
    # FISICO
    # ------------------------
    velocidad = models.PositiveIntegerField()
    aceleracion = models.PositiveIntegerField()
    resistencia = models.PositiveIntegerField()
    fuerza = models.PositiveIntegerField()
    salto = models.PositiveIntegerField()
    agilidad = models.PositiveIntegerField()
    equilibrio = models.PositiveIntegerField()
    potencia_salto = models.PositiveIntegerField()

    # ------------------------
    # ARQUERO
    # ------------------------
    reflejos = models.PositiveIntegerField(default=1)
    estirada = models.PositiveIntegerField(default=1)
    manejo_area = models.PositiveIntegerField(default=1)
    blocaje = models.PositiveIntegerField(default=1)
    saque_meta = models.PositiveIntegerField(default=1)
    saque_mano = models.PositiveIntegerField(default=1)
    uno_contra_uno = models.PositiveIntegerField(default=1)
    comunicacion = models.PositiveIntegerField(default=1)

    # ------------------------
    # ESPECIALES
    # ------------------------
    atributos_especiales = models.ManyToManyField(
        AtributoEspecial,
        blank=True
    )

    nivel_general = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # ------------------------
    # VALIDACIONES
    # ------------------------

    def clean(self):
        if self.posicion_secundaria == self.posicion_principal:
            raise ValidationError("Posición secundaria inválida.")

    # ------------------------
    # CALCULO
    # ------------------------

    def calcular_promedios(self):
        ataque = [
            self.finalizacion, self.remate_cabeza, self.desmarque,
            self.vision_juego, self.tiros_lejanos, self.penales,
            self.saques_esquina, self.tiros_libres
        ]

        defensa = [
            self.entradas, self.marcaje, self.anticipacion,
            self.colocacion, self.intercepciones, self.despeje
        ]

        tecnica = [
            self.control_balon, self.regate, self.pases_cortos,
            self.pases_largos, self.centros, self.efecto,
            self.tecnica_disparo, self.juego_espaldas
        ]

        fisico = [
            self.velocidad, self.aceleracion, self.resistencia,
            self.fuerza, self.salto, self.agilidad,
            self.equilibrio, self.potencia_salto
        ]

        arquero = [
            self.reflejos, self.estirada, self.manejo_area,
            self.blocaje, self.saque_meta, self.saque_mano,
            self.uno_contra_uno, self.comunicacion
        ]

        return {
            "ATAQUE": sum(ataque) / len(ataque),
            "DEFENSA": sum(defensa) / len(defensa),
            "TECNICA": sum(tecnica) / len(tecnica),
            "FISICO": sum(fisico) / len(fisico),
            "ARQUERO": sum(arquero) / len(arquero),
        }

    def calcular_nivel_general(self):
        promedios = self.calcular_promedios()

        # BASE SEGÚN POSICIÓN
        if self.posicion_principal == "ARQ":
            nivel = (
                promedios["ARQUERO"] * 0.7 +
                promedios["TECNICA"] * 0.1 +
                promedios["FISICO"] * 0.2
            )

        elif self.posicion_principal == "DEF":
            nivel = (
                promedios["DEFENSA"] * 0.4 +
                promedios["FISICO"] * 0.3 +
                promedios["TECNICA"] * 0.2 +
                promedios["ATAQUE"] * 0.1
            )

        elif self.posicion_principal == "MED":
            nivel = (
                promedios["TECNICA"] * 0.35 +
                promedios["FISICO"] * 0.25 +
                promedios["ATAQUE"] * 0.2 +
                promedios["DEFENSA"] * 0.2
            )

        else:  # DEL
            nivel = (
                promedios["ATAQUE"] * 0.4 +
                promedios["TECNICA"] * 0.3 +
                promedios["FISICO"] * 0.2 +
                promedios["DEFENSA"] * 0.1
            )

        # APLICAR ATRIBUTOS ESPECIALES (POR RUBRO)
        for atributo in self.atributos_especiales.all():
            rubro = atributo.rubro
            bonus = promedios[rubro] * (atributo.modificador / 100)
            nivel += bonus

        return Decimal(str(round(nivel, 2)))

    def recalcular_nivel(self):
        self.nivel_general = self.calcular_nivel_general()
        self.save(update_fields=["nivel_general"])

    def __str__(self):
        return self.nombre