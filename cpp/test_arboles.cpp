#include "arboles.hpp"
#include <iostream>
#include <memory>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>

using Arbol = std::unique_ptr<Nodo, void(*)(Nodo*)>;

std::string estructura(const Nodo* n) {
    if (!n) return "#";
    return std::to_string(n->valor)+"("+estructura(n->izq)+","+estructura(n->der)+")";
}

void direcciones(const Nodo* n, std::set<const Nodo*>& resultado) {
    if (!n) return;
    resultado.insert(n);
    direcciones(n->izq, resultado);
    direcciones(n->der, resultado);
}

void exigir(bool ok, const char* texto) {
    if (!ok) throw std::runtime_error(texto);
}

void comprobar(Nodo* original, const std::string& esperado) {
    Arbol a(original, liberar);
    auto antes=estructura(a.get());
    Arbol b(espejo(a.get()), liberar);
    exigir(estructura(b.get())==esperado,"forma o valores incorrectos");
    exigir(estructura(a.get())==antes,"original modificado");
    std::set<const Nodo*> idsA,idsB;
    direcciones(a.get(),idsA); direcciones(b.get(),idsB);
    for (auto p:idsA) exigir(!idsB.count(p),"comparte nodos");
    Arbol doble(espejo(b.get()), liberar);
    exigir(estructura(doble.get())==antes,"doble espejo");
}

void comprobarSimetria() {
    exigir(sonEspejo(nullptr,nullptr),"dos vacios deben ser espejo");
    exigir(esSimetrico(nullptr),"vacio simetrico");
    Arbol hoja(nodo(7),liberar);
    exigir(esSimetrico(hoja.get()),"hoja simetrica");
    exigir(!sonEspejo(hoja.get(),nullptr),"solo un vacio");
    exigir(!sonEspejo(nullptr,hoja.get()),"solo un vacio invertido");
    Arbol otraHoja(nodo(8),liberar);
    exigir(!sonEspejo(hoja.get(),otraHoja.get()),"valores de hojas distintos");

    Arbol a(nodo(1,nodo(2,nodo(4)),nodo(3)),liberar);
    Arbol b(nodo(1,nodo(3),nodo(2,nullptr,nodo(4))),liberar);
    const auto antesA=estructura(a.get()), antesB=estructura(b.get());
    exigir(sonEspejo(a.get(),b.get()),"dos arboles reflejados");
    exigir(sonEspejo(b.get(),a.get()),"relacion de espejo reciproca");
    exigir(!sonEspejo(a.get(),a.get()),"igualdad no implica reflejo");
    exigir(estructura(a.get())==antesA && estructura(b.get())==antesB,
           "sonEspejo modifica entrada");

    Arbol mariposa(nodo(1,nodo(2,nodo(4),nodo(5)),
                          nodo(2,nodo(5),nodo(4))),liberar);
    const auto antes=estructura(mariposa.get());
    std::set<const Nodo*> idsAntes,idsDespues;
    direcciones(mariposa.get(),idsAntes);
    exigir(esSimetrico(mariposa.get()),"mariposa de teoria");
    exigir(esSimetrico(mariposa.get()),"segunda llamada");
    direcciones(mariposa.get(),idsDespues);
    exigir(estructura(mariposa.get())==antes && idsAntes==idsDespues,
           "esSimetrico modifica el arbol");

    Arbol valores(nodo(1,nodo(2,nodo(4)),nodo(2,nullptr,nodo(9))),liberar);
    exigir(!esSimetrico(valores.get()),"estructura simetrica, valores distintos");
    Arbol forma(nodo(1,nodo(1,nullptr,nodo(1)),nodo(1,nullptr,nodo(1))),liberar);
    exigir(!esSimetrico(forma.get()),"inorden palindromo no basta");
    Arbol incompleto(nodo(0,nodo(-2,nullptr,nodo(3)),nodo(-2,nodo(3))),liberar);
    exigir(esSimetrico(incompleto.get()),"simetrico con hijos ausentes");
    Arbol soloIzquierdo(nodo(1,nodo(1)),liberar);
    exigir(!esSimetrico(soloIzquierdo.get()),"solo hijo izquierdo");
}

int main() {
    try {
        comprobar(nullptr,"#");
        comprobar(nodo(7),"7(#,#)");
        comprobar(nodo(1,nodo(2,nodo(4),nodo(5)),nodo(3)),
                  "1(3(#,#),2(5(#,#),4(#,#)))");
        comprobar(nodo(1,nodo(2,nullptr,nodo(3))),"1(#,2(3(#,#),#))");
        comprobar(nodo(2,nodo(2,nodo(-1)),nodo(2)),"2(2(#,#),2(#,-1(#,#)))");
        Arbol a(nodo(1,nodo(2,nodo(4),nodo(5)),nodo(3)),liberar);
        Arbol b(espejo(a.get()),liberar);
        std::vector<int> orden;
        imprimirInorden(b.get(),orden);
        exigir(orden==std::vector<int>({3,1,5,2,4}),"inorden espejo");
        b->der->izq->valor=99;
        exigir(a->izq->der->valor==5,"copia no independiente");
        std::cout << "PruebasEspejo: OK\n";
        comprobarSimetria();
        std::cout << "PruebasSimetria: OK\n";
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "PruebasEspejo: FALLO: " << e.what() << '\n';
        return 1;
    }
}
