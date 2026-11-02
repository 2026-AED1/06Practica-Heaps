#pragma once
#include <stdexcept>
#include <vector>

struct Nodo {
    int valor;
    Nodo* izq = nullptr;
    Nodo* der = nullptr;
};

inline Nodo* nodo(int v, Nodo* izq=nullptr, Nodo* der=nullptr) {
    return new Nodo{v, izq, der};
}

inline Nodo* espejo(const Nodo* raiz) {
    (void)raiz;
    throw std::logic_error("TODO espejo");
}

inline bool sonEspejo(const Nodo* a, const Nodo* b) {
    (void)a; (void)b;
    throw std::logic_error("TODO sonEspejo");
}

inline bool esSimetrico(const Nodo* raiz) {
    (void)raiz;
    throw std::logic_error("TODO esSimetrico");
}

inline void liberar(Nodo* raiz) {
    if (!raiz) return;
    liberar(raiz->izq);
    liberar(raiz->der);
    delete raiz;
}

inline void imprimirInorden(const Nodo* raiz, std::vector<int>& salida) {
    if (!raiz) return;
    imprimirInorden(raiz->izq, salida);
    salida.push_back(raiz->valor);
    imprimirInorden(raiz->der, salida);
}
