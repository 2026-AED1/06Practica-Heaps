#include "utilidades.hpp"
#include <cassert>

int main() {
    assert(sumar_caso({}) == 0);
    assert(sumar_caso({0,-3,3}) == 0);
    assert(sumar_caso({4,4}) == 8);
    const std::vector<long long> valores{3000000000LL, 7};
    const auto antes = valores;
    assert(sumar_caso(valores) == 3000000007LL);
    assert(sumar_caso(valores) == 3000000007LL);
    assert(valores == antes);
}
