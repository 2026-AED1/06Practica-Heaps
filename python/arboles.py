

class Nodo:
    def __init__(self, valor, izq=None, der=None):
        self.valor = valor
        self.izq = izq
        self.der = der


def espejo(raiz):
    raise NotImplementedError("TODO espejo")


def son_espejo(a, b):
    raise NotImplementedError("TODO son_espejo")


def es_simetrico(raiz):
    raise NotImplementedError("TODO es_simetrico")


def inorden(raiz):
    salida = []
    def visitar(nodo):
        if nodo is not None:
            visitar(nodo.izq)
            salida.append(nodo.valor)
            visitar(nodo.der)
    visitar(raiz)
    return salida
