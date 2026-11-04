#!/usr/bin/env python3
"""
simular_pi.py - Réplica en Python del ejemplo "pi" de Hadoop (QuasiMonteCarlo).

Uso:   python simular_pi.py <nMaps> <nSamples>
Ej.:   python simular_pi.py 10 1000     ->  3.14080000000000000000

Sirve para verificar los resultados esperados SIN necesitar Hadoop.
Usa la misma secuencia de Halton (bases 2 y 3) que Hadoop y reparte los
puntos entre "mappers" con el mismo esquema (offset = i * nSamples).
"""
import sys
from decimal import Decimal, getcontext, ROUND_HALF_UP

BASES = [2, 3]
DIGITOS = [63, 40]          # máximo de dígitos por base (igual que Hadoop)


class Halton:
    """Secuencia de Halton 2D; arranca en H(inicio) y el primer punto es H(inicio+1)."""

    def __init__(self, inicio):
        self.q = [[0.0] * k for k in DIGITOS]
        self.d = [[0] * k for k in DIGITOS]
        self.x = [0.0, 0.0]
        for i in range(2):
            k = inicio
            for j in range(DIGITOS[i]):
                self.q[i][j] = (1.0 if j == 0 else self.q[i][j - 1]) / BASES[i]
                self.d[i][j] = k % BASES[i]
                k = (k - self.d[i][j]) // BASES[i]
                self.x[i] += self.d[i][j] * self.q[i][j]

    def siguiente(self):
        for i in range(2):
            for j in range(DIGITOS[i]):
                self.d[i][j] += 1
                self.x[i] += self.q[i][j]
                if self.d[i][j] < BASES[i]:
                    break
                self.d[i][j] = 0
                self.x[i] -= (1.0 if j == 0 else self.q[i][j - 1])
        return self.x[0], self.x[1]


def mapper(offset, size):
    """Fase Map: cuenta puntos dentro y fuera del círculo inscrito."""
    halton = Halton(offset)
    dentro = fuera = 0
    for _ in range(size):
        px, py = halton.siguiente()
        x, y = px - 0.5, py - 0.5
        if x * x + y * y > 0.25:
            fuera += 1
        else:
            dentro += 1
    return dentro, fuera


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    n_maps, n_samples = int(sys.argv[1]), int(sys.argv[2])

    total_dentro = total_fuera = 0
    for i in range(n_maps):                       # Map (uno tras otro)
        d, f = mapper(i * n_samples, n_samples)
        print(f"Map #{i}: dentro={d} fuera={f}")
        total_dentro += d                         # Reduce: suma
        total_fuera += f

    getcontext().prec = 60
    pi = (Decimal(4) * total_dentro / Decimal(n_maps * n_samples)).quantize(
        Decimal(1).scaleb(-20), rounding=ROUND_HALF_UP)
    print(f"Reduce: dentro={total_dentro} fuera={total_fuera}")
    print(f"Estimated value of Pi is {pi}")


if __name__ == "__main__":
    main()
