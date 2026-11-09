import sys

from lector_yaml import ErrorMT, leer_mt
from simulador import simular


# Muestra la descripcion formal de la MT que se leyo
def mostrar_mt(mt):
    print("Estados:", ", ".join(mt.estados))
    print("Alfabeto de entrada:", ", ".join(mt.alfabeto_entrada))
    print("Alfabeto de la cinta:", ", ".join(mt.alfabeto_cinta))
    print("Estado inicial:", mt.estado_inicial)
    print("Estados de aceptacion:", ", ".join(mt.estados_aceptacion))
    print("Funciones de transicion:")
    for t in mt.transiciones.values():
        print(f"  d([{t.estado}, {t.cache}], {t.leer}) = ([{t.siguiente}, {t.nueva_cache}], {t.escribir}, {t.mover})")


# Muestra todas las descripciones instantaneas y el resultado de una cadena
def mostrar_resultado(cadena, resultado):
    print()
    print("=" * 60)
    print(f'Cadena: "{cadena}"')
    print("=" * 60)
    for paso, id_ in enumerate(resultado.ids):
        prefijo = "    " if paso == 0 else "|-  "
        print(f"{paso:>4} {prefijo}{id_}")
    print(f"Cinta final: {resultado.cinta_final if resultado.cinta_final else '(vacia)'}")
    print("Resultado:", "ACEPTADA" if resultado.aceptada else "RECHAZADA")
    print("Motivo:", resultado.motivo)


def main():
    if len(sys.argv) != 2:
        print("Uso: py main.py archivo.yaml")
        sys.exit(1)

    try:
        mt = leer_mt(sys.argv[1])
    except (ErrorMT, OSError) as error:
        print("Error en la configuracion de la MT:", error)
        sys.exit(1)

    mostrar_mt(mt)
    for cadena in mt.entradas:
        mostrar_resultado(cadena, simular(mt, cadena))


if __name__ == "__main__":
    main()
