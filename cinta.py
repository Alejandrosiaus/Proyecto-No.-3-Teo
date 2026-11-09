from maquina import BLANCO


class Cinta:
    def __init__(self, cadena):
        self.casillas = {i: s for i, s in enumerate(cadena)}
        self.cabeza = 0

    def leer(self):
        return self.casillas.get(self.cabeza, BLANCO)

    def escribir(self, simbolo):
        if simbolo == BLANCO:
            self.casillas.pop(self.cabeza, None)
        else:
            self.casillas[self.cabeza] = simbolo

    def mover(self, direccion):
        if direccion == "R":
            self.cabeza += 1
        elif direccion == "L":
            self.cabeza -= 1

    def rango(self):
        posiciones = list(self.casillas) + [self.cabeza]
        return min(posiciones), max(posiciones)

    def contenido(self):
        if not self.casillas:
            return ""
        inicio, fin = min(self.casillas), max(self.casillas)
        return "".join(self.casillas.get(i, BLANCO) for i in range(inicio, fin + 1))
