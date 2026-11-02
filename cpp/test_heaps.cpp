#include "heaps.hpp"
#include <climits>
#include <iostream>
#include <random>
#include <string>

void exigir(bool condicion, const std::string& mensaje) {
    if (!condicion) throw std::runtime_error(mensaje);
}

std::vector<int> ascendente(std::vector<int> a) {
    std::sort(a.begin(), a.end());
    return a;
}

const std::vector<std::vector<int>> casos = {
    {}, {7}, {4, 1, 7, 3, 8, 5}, {2, 2, 2, 2}, {-5, -1, -3, 0, -5},
    {1, 2, 3, 4, 5}, {5, 4, 3, 2, 1}, {INT_MIN, 0, INT_MAX, INT_MIN}
};

void comprobar_top(const std::vector<int>& original) {
    for (int k : {0, 1, 2, 3, static_cast<int>(original.size()/2),
                  static_cast<int>(original.size()), static_cast<int>(original.size())+5}) {
        auto a = original;
        auto esperado = ascendente(a);
        std::reverse(esperado.begin(), esperado.end());
        esperado.resize(std::min(esperado.size(), static_cast<std::size_t>(k)));
        exigir(top_k(a,k) == esperado, "top-k: valores, duplicados u orden");
        exigir(a == original, "top-k modifica entrada");
    }
}

void top() {
    exigir(top_k({5,1,8,3,9,2,7},3) == std::vector<int>({9,8,7}), "ejemplo");
    exigir(top_k({4,4,2},2) == std::vector<int>({4,4}), "duplicados");
    bool lanzo = false;
    try { top_k({},-1); }
    catch (const std::invalid_argument&) { lanzo = true; }
    exigir(lanzo, "k negativo debe lanzar invalid_argument");
    for (const auto& a : casos) comprobar_top(a);
    std::mt19937 rng(60);
    std::uniform_int_distribution<int> valor(-10,10);
    for (int n=0; n<100; ++n) {
        std::vector<int> a(n);
        for (int& x : a) x=valor(rng);
        comprobar_top(a);
    }
}

int main() {
    try {
        top();
        std::cout << "PruebasTopK: OK\n";
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "PruebasTopK: FALLO: " << e.what() << '\n';
        return 1;
    }
}
