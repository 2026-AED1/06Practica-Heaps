import argparse
import csv
import platform
import random
import statistics
import time

import heaps


def insertion_sort(datos):
    a = list(datos)
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x
    return a


def medir(funcion, esperado, repeticiones):
    if funcion() != esperado:
        raise AssertionError("Resultado incorrecto antes de medir")
    muestras = []
    for _ in range(repeticiones):
        inicio = time.perf_counter_ns()
        resultado = funcion()
        duracion = time.perf_counter_ns() - inicio
        if resultado != esperado:
            raise AssertionError("Resultado incorrecto durante el experimento")
        muestras.append(duracion / 1_000_000)
    return statistics.median(muestras)


def main():
    p = argparse.ArgumentParser(description="Practica 06")
    p.add_argument("--tamanos", type=int, nargs="+", default=[250, 500, 1000, 2000])
    p.add_argument("--repeticiones", type=int, default=3)
    p.add_argument("--salida", default="benchmark.csv")
    args = p.parse_args()
    if any(n < 1 for n in args.tamanos) or args.repeticiones < 1:
        p.error("Tamaños y repeticiones deben ser positivos")
    rng = random.Random(606)
    print(f"Python {platform.python_version()} | {platform.platform()}")
    print(f"Mediana de {args.repeticiones}; incluye producir resultado y sus copias; semilla 606")
    filas = []
    for n in args.tamanos:
        datos_por_tipo = {
            "aleatoria": [rng.randrange(-10*n, 10*n+1) for _ in range(n)],
            "ordenada": list(range(n)),
            "inversa": list(range(n, 0, -1)),
            "repetida": [rng.randrange(5) for _ in range(n)],
        }
        for tipo, datos in datos_por_tipo.items():
            asc = sorted(datos)
            for k in sorted({1, min(10, n), n//2, n}):
                esperado = asc[::-1][:k]
                for nombre, f in (("top_k", lambda: heaps.top_k(iter(datos), k)),
                                  ("ordenar_y_cortar", lambda: sorted(datos, reverse=True)[:k]),
                                  ("insertion_y_cortar", lambda: insertion_sort(datos)[::-1][:k])):
                    ms = medir(f, esperado, args.repeticiones)
                    filas.append([tipo, n, k, nombre, ms])
                    print(f"{tipo:10} n={n:6} k={k:4} {nombre:20} {ms:10.4f} ms")
    with open(args.salida, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["distribucion", "n", "k", "metodo", "mediana_ms"])
        escritor.writerows(filas)
    print(f"Guardado: {args.salida}")


if __name__ == "__main__":
    main()
