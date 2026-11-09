from cinta import Cinta
from maquina import BLANCO

MAX_PASOS = 10000


class Resultado:
    def __init__(self):
        self.ids = []
        self.aceptada = False
        self.motivo = ""
        self.cinta_final = ""


def descripcion_instantanea(cinta, estado, cache):
    inicio, fin = cinta.rango()
    izquierda = [cinta.casillas.get(i, BLANCO) for i in range(inicio, cinta.cabeza)]
    derecha = [cinta.casillas.get(i, BLANCO) for i in range(cinta.cabeza, fin + 1)]
    return " ".join(izquierda + [f"[{estado}, {cache}]"] + derecha)


def validar_cadena(mt, cadena):
    for simbolo in cadena:
        if simbolo not in mt.alfabeto_entrada:
            return simbolo
    return None


def simular(mt, cadena):
    resultado = Resultado()

    invalido = validar_cadena(mt, cadena)
    if invalido is not None:
        resultado.motivo = f"el simbolo '{invalido}' no pertenece al alfabeto de entrada"
        resultado.cinta_final = cadena
        return resultado

    cinta = Cinta(cadena)
    estado, cache = mt.estado_inicial, BLANCO
    resultado.ids.append(descripcion_instantanea(cinta, estado, cache))

    pasos = 0
    while True:
        simbolo = cinta.leer()
        t = mt.buscar(estado, simbolo, cache)

        if t is None:
            resultado.aceptada = estado in mt.estados_aceptacion
            if resultado.aceptada:
                resultado.motivo = f"la MT se detuvo en el estado de aceptacion {estado}"
            else:
                resultado.motivo = f"no hay transicion para ([{estado}, {cache}], {simbolo}) y {estado} no es de aceptacion"
            break

        if pasos == MAX_PASOS:
            resultado.motivo = f"la MT no se detuvo despues de {MAX_PASOS} pasos"
            break

        cinta.escribir(t.escribir)
        cinta.mover(t.mover)
        estado, cache = t.siguiente, t.nueva_cache
        pasos += 1
        resultado.ids.append(descripcion_instantanea(cinta, estado, cache))

    resultado.cinta_final = cinta.contenido()
    return resultado
