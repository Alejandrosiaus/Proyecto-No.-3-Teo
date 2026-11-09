import yaml

from maquina import BLANCO, MaquinaTuring, Transicion


class ErrorMT(Exception):
    pass


# Lee el archivo YAML y construye la MT
def leer_mt(ruta):
    with open(ruta, encoding="utf-8") as archivo:
        datos = yaml.load(archivo, Loader=yaml.BaseLoader)

    if not isinstance(datos, dict) or "mt" not in datos:
        raise ErrorMT("el archivo debe tener la clave 'mt'")
    mt = datos["mt"]

    for clave in ["states", "input_alphabet", "tape_alphabet", "initial_state", "accept_states", "transitions"]:
        if clave not in mt:
            raise ErrorMT(f"falta la clave '{clave}'")

    maquina = MaquinaTuring(
        estados=lista(mt, "states"),
        alfabeto_entrada=lista(mt, "input_alphabet"),
        alfabeto_cinta=lista(mt, "tape_alphabet"),
        estado_inicial=mt["initial_state"],
        estados_aceptacion=lista(mt, "accept_states"),
        entradas=lista(mt, "inputs") if "inputs" in mt else [],
    )

    validar_definicion(maquina)

    for numero, t in enumerate(mt["transitions"], start=1):
        transicion = leer_transicion(t, numero, maquina)
        clave = (transicion.estado, transicion.leer, transicion.cache)
        if clave in maquina.transiciones:
            raise ErrorMT(f"transicion {numero}: ya existe una transicion para {clave}, la MT debe ser determinista")
        maquina.transiciones[clave] = transicion

    return maquina


def lista(mt, clave):
    valor = mt[clave]
    if not isinstance(valor, list):
        raise ErrorMT(f"'{clave}' debe ser una lista")
    return valor


# Revisa que estados y alfabetos sean consistentes entre si
def validar_definicion(m):
    if m.estado_inicial not in m.estados:
        raise ErrorMT(f"el estado inicial '{m.estado_inicial}' no esta en states")
    for q in m.estados_aceptacion:
        if q not in m.estados:
            raise ErrorMT(f"el estado de aceptacion '{q}' no esta en states")
    if BLANCO not in m.alfabeto_cinta:
        raise ErrorMT(f"el blanco '{BLANCO}' debe estar en tape_alphabet")
    if BLANCO in m.alfabeto_entrada:
        raise ErrorMT(f"el blanco '{BLANCO}' no puede estar en input_alphabet")
    for s in m.alfabeto_entrada:
        if s not in m.alfabeto_cinta:
            raise ErrorMT(f"el simbolo '{s}' de input_alphabet no esta en tape_alphabet")


# Convierte una transicion del YAML: read = [simbolo, cache], write = [nueva cache, simbolo a escribir]
def leer_transicion(t, numero, m):
    for clave in ["state", "read", "write", "move", "next"]:
        if clave not in t:
            raise ErrorMT(f"transicion {numero}: falta '{clave}'")

    leer, escribir = t["read"], t["write"]
    if not (isinstance(leer, list) and len(leer) == 2):
        raise ErrorMT(f"transicion {numero}: 'read' debe ser [simbolo, cache]")
    if not (isinstance(escribir, list) and len(escribir) == 2):
        raise ErrorMT(f"transicion {numero}: 'write' debe ser [cache, simbolo]")

    transicion = Transicion(
        estado=t["state"],
        leer=leer[0],
        cache=leer[1],
        nueva_cache=escribir[0],
        escribir=escribir[1],
        mover=t["move"],
        siguiente=t["next"],
    )

    for q in [transicion.estado, transicion.siguiente]:
        if q not in m.estados:
            raise ErrorMT(f"transicion {numero}: el estado '{q}' no esta en states")
    for s in [transicion.leer, transicion.cache, transicion.nueva_cache, transicion.escribir]:
        if s not in m.alfabeto_cinta:
            raise ErrorMT(f"transicion {numero}: el simbolo '{s}' no esta en tape_alphabet")
    if transicion.mover not in ["L", "R", "S"]:
        raise ErrorMT(f"transicion {numero}: 'move' debe ser L, R o S")

    return transicion
