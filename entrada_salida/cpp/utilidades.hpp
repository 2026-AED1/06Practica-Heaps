#include <vector>

inline long long sumar_caso(const std::vector<long long>& valores) {
    long long total = 0;
    for (long long x : valores) {
        total += x;
    }
    return total;
}
