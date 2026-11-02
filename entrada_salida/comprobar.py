import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def casos(base, nombre):
    yield "ejemplo", (base/"data"/(nombre+".in")).read_text(), (base/"data"/(nombre+".ans")).read_text()
    if nombre == "01_con_T":
        yield "cero casos", "0\n", ""
        yield "espacios y negativos", "2\n4\n1  2\t-3 0\n1\n8", "0\n8\n"
    elif nombre == "02_centinela":
        yield "solo centinela", "0\n", ""
        yield "negativos y cero como dato", "4\n1 2 -3 0\n1\n8\n0", "0\n8\n"
        yield "centinela no es caso", "1\n7\n0\n", "7\n"
    else:
        yield "vacio", "", ""
        yield "sin salto final", "4\n1 2 -3 0\n1\n8", "0\n8\n"
        yield "lineas vacias entre casos", "\n1\n7\n\n1\n0\n\n", "7\n0\n"


def main():
    p = argparse.ArgumentParser(description="Practica 06")
    p.add_argument("--lenguaje", choices=["python", "cpp"], required=True)
    args = p.parse_args()
    base = Path(__file__).resolve().parent
    carpeta = base / args.lenguaje
    fallos = 0
    total = 0
    with tempfile.TemporaryDirectory(prefix="aed06_io_") as tmp:
        for nombre in ["01_con_T", "02_centinela", "03_hasta_EOF"]:
            if args.lenguaje == "python":
                comando = [sys.executable, str(carpeta/(nombre+".py"))]
            else:
                ejecutable = Path(tmp)/(nombre+(".exe" if os.name=="nt" else ""))
                subprocess.run(["g++", "-std=c++17", "-Wall", "-Wextra", "-pedantic",
                                str(carpeta/(nombre+".cpp")), "-o", str(ejecutable)], check=True)
                comando = [str(ejecutable)]
            for etiqueta, entrada, salida in casos(base, nombre):
                total += 1
                proceso = subprocess.run(comando, input=entrada, text=True,
                                         capture_output=True, timeout=5)
                if proceso.returncode != 0 or proceso.stdout != salida:
                    fallos += 1
                    print(f"FALLO {nombre}: {etiqueta}")
                    print(f"Esperado {salida!r}; recibido {proceso.stdout!r}; retorno {proceso.returncode}")
                    if proceso.stderr:
                        print(proceso.stderr)
                else:
                    print(f"OK {nombre}: {etiqueta}")
    print(f"{total-fallos}/{total} casos correctos ({args.lenguaje})")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
