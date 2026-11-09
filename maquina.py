from dataclasses import dataclass, field

BLANCO = "B"


# Una funcion de transicion
@dataclass
class Transicion:
    estado: str
    leer: str
    cache: str
    nueva_cache: str
    escribir: str
    mover: str
    siguiente: str


# Descripcion formal de la Maquina de Turing de una cinta
@dataclass
class MaquinaTuring:
    estados: list
    alfabeto_entrada: list
    alfabeto_cinta: list
    estado_inicial: str
    estados_aceptacion: list
    transiciones: dict = field(default_factory=dict)
    entradas: list = field(default_factory=list)

    # Busca la transicion que corresponde al estado, al simbolo leido y a la cache
    def buscar(self, estado, simbolo, cache):
        return self.transiciones.get((estado, simbolo, cache))
