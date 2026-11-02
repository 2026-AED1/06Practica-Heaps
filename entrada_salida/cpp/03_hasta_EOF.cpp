#include <iostream>
#include <vector>

long long suma(const std::vector<long long>& valores) {
    long long total = 0;
    for (long long valor : valores) {
        total += valor;
    }
    return total;
}

int main() {
}
