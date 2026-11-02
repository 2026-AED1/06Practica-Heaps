import random
import unittest
import heaps


CASOS = [[], [7], [4, 1, 7, 3, 8, 5], [2, 2, 2, 2],
         [-5, -1, -3, 0, -5], list(range(20)), list(range(20, -1, -1))]



class PruebasTopK(unittest.TestCase):
    def test_ejemplo_y_duplicados(self):
        self.assertEqual(heaps.top_k([5, 1, 8, 3, 9, 2, 7], 3), [9, 8, 7])
        self.assertEqual(heaps.top_k([4, 4, 2], 2), [4, 4])

    def test_limites_y_entrada_intacta(self):
        for original in CASOS:
            for k in (0, 1, 2, len(original), len(original) + 5):
                with self.subTest(datos=original, k=k):
                    a = original.copy()
                    self.assertEqual(heaps.top_k(a, k), sorted(a, reverse=True)[:k])
                    self.assertEqual(a, original)

    def test_negativo(self):
        with self.assertRaises(ValueError):
            heaps.top_k([], -1)

    def test_iterable_sin_len_una_pasada(self):
        class UnaPasada:
            def __init__(self):
                self.usado = False

            def __iter__(self):
                if self.usado:
                    raise AssertionError("Segunda pasada sobre la entrada")
                self.usado = True
                return iter([5, 1, 8, 3, 9, 2, 7])

        self.assertEqual(heaps.top_k(UnaPasada(), 3), [9, 8, 7])
        self.assertEqual(heaps.top_k((x for x in [-5, -1, -3]), 5), [-1, -3, -5])

    def test_cero_y_negativo_no_consumen(self):
        def prohibido():
            raise AssertionError("No debe consumir la entrada")
            yield 0
        self.assertEqual(heaps.top_k(prohibido(), 0), [])
        with self.assertRaises(ValueError):
            heaps.top_k(prohibido(), -1)

    def test_aleatorios(self):
        rng = random.Random(60)
        for n in range(70):
            a = [rng.randrange(-10, 11) for _ in range(n)]
            for k in (0, 1, 3, n // 2, n, n + 1):
                self.assertEqual(heaps.top_k(iter(a), k), sorted(a, reverse=True)[:k])


if __name__ == "__main__":
    unittest.main()
