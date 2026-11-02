import unittest
from arboles import Nodo, espejo, inorden, son_espejo, es_simetrico


def estructura(n):
    return None if n is None else (n.valor, estructura(n.izq), estructura(n.der))


def identidades(n):
    return set() if n is None else {id(n)} | identidades(n.izq) | identidades(n.der)


class PruebasEspejo(unittest.TestCase):
    def test_vacio_y_hoja(self):
        self.assertIsNone(espejo(None))
        a = Nodo(7)
        b = espejo(a)
        self.assertEqual(estructura(b), (7, None, None))
        self.assertIsNot(a, b)

    def test_ejemplo_de_teoria(self):
        a = Nodo(1, Nodo(2, Nodo(4), Nodo(5)), Nodo(3))
        antes = estructura(a)
        b = espejo(a)
        self.assertEqual(estructura(b), (1, (3, None, None), (2, (5, None, None), (4, None, None))))
        self.assertEqual(estructura(a), antes)
        self.assertEqual(inorden(b), [3, 1, 5, 2, 4])
        self.assertTrue(identidades(a).isdisjoint(identidades(b)))

    def test_cadena_con_hijos_ausentes(self):
        a = Nodo(1, Nodo(2, None, Nodo(3)))
        b = espejo(a)
        self.assertEqual(estructura(b), (1, None, (2, (3, None, None), None)))
        self.assertEqual(estructura(espejo(b)), estructura(a))

    def test_duplicados_y_copia_independiente(self):
        a = Nodo(2, Nodo(2, Nodo(-1)), Nodo(2))
        b = espejo(a)
        self.assertTrue(identidades(a).isdisjoint(identidades(b)))
        b.der.der.valor = 99
        self.assertEqual(a.izq.izq.valor, -1)
        self.assertEqual(estructura(espejo(espejo(a))), estructura(a))


class PruebasSimetria(unittest.TestCase):
    def test_vacios_y_hojas(self):
        self.assertIs(son_espejo(None, None), True)
        self.assertIs(son_espejo(Nodo(1), None), False)
        self.assertIs(son_espejo(None, Nodo(1)), False)
        self.assertIs(son_espejo(Nodo(1), Nodo(1)), True)
        self.assertIs(son_espejo(Nodo(1), Nodo(2)), False)
        self.assertIs(es_simetrico(None), True)
        self.assertIs(es_simetrico(Nodo(7)), True)

    def test_dos_arboles_reflejados_no_son_iguales(self):
        a = Nodo(1, Nodo(2, Nodo(4)), Nodo(3))
        b = Nodo(1, Nodo(3), Nodo(2, None, Nodo(4)))
        antes_a, antes_b = estructura(a), estructura(b)
        self.assertIs(son_espejo(a, b), True)
        self.assertIs(son_espejo(b, a), True)
        self.assertIs(son_espejo(a, a), False)
        self.assertEqual(estructura(a), antes_a)
        self.assertEqual(estructura(b), antes_b)

    def test_mariposa_de_teoria_sin_modificar(self):
        a = Nodo(1, Nodo(2, Nodo(4), Nodo(5)), Nodo(2, Nodo(5), Nodo(4)))
        antes = estructura(a)
        ids = identidades(a)
        self.assertIs(es_simetrico(a), True)
        self.assertIs(es_simetrico(a), True)
        self.assertEqual(estructura(a), antes)
        self.assertEqual(identidades(a), ids)

    def test_misma_forma_pero_valores_distintos(self):
        a = Nodo(1, Nodo(2, Nodo(4)), Nodo(2, None, Nodo(9)))
        self.assertIs(es_simetrico(a), False)

    def test_mismos_valores_pero_forma_no_reflejada(self):
        a = Nodo(1, Nodo(1, None, Nodo(1)), Nodo(1, None, Nodo(1)))
        self.assertIs(es_simetrico(a), False)
        self.assertIs(es_simetrico(Nodo(1, Nodo(1))), False)

    def test_subarboles_incompletos_si_reflejados(self):
        a = Nodo(0, Nodo(-2, None, Nodo(3)), Nodo(-2, Nodo(3)))
        self.assertIs(es_simetrico(a), True)


if __name__ == "__main__":
    unittest.main()
