import contextlib
import importlib.util
import io
from pathlib import Path
import unittest
from unittest.mock import patch


class PruebasSumarCaso(unittest.TestCase):
    def test_lista_ya_leida_sin_mutacion_ni_entrada_salida(self):
        base = Path(__file__).resolve().parent / "python"
        for ruta in (base/"utilidades.py",):
            spec = importlib.util.spec_from_file_location("utilidades_probadas", ruta)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            for valores, esperado in [([], 0), ([0, -3, 3], 0), ([4, 4], 8),
                                      ([3_000_000_000, 7], 3_000_000_007)]:
                with self.subTest(ruta=ruta, valores=valores):
                    antes = valores.copy()
                    salida = io.StringIO()
                    with patch("builtins.input", side_effect=AssertionError("No debe leer")):
                        with contextlib.redirect_stdout(salida):
                            self.assertEqual(modulo.sumar_caso(valores), esperado)
                            self.assertEqual(modulo.sumar_caso(valores), esperado)
                    self.assertEqual(valores, antes)
                    self.assertEqual(salida.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
