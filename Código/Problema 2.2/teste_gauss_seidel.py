"""Testes rápidos do gauss_seidel.py. Rodar com: python teste_gauss_seidel.py"""

import numpy as np

from gauss_seidel import (criterio_linhas, criterio_sassenfeld, gauss_seidel,
                          melhor_ordem, montar_trelica, raio_espectral)


def teste_exemplo_do_slide():
    A = np.array([[5.0, 1, 1], [3, 4, 1], [3, 3, 6]])
    b = np.array([5.0, 6, 0])
    r = gauss_seidel(A, b, [-1, 0, 1], precisao=5e-2)
    primeira = r.historico[1][1]
    assert np.allclose(primeira, [0.8, 0.65, -0.725]), primeira
    assert r.convergiu and r.iteracoes == 4, r.iteracoes
    assert np.allclose(r.x, [1.002, 0.998, -1], atol=5e-3), r.x
    assert max(criterio_linhas(A)) == 1.0       # linha 2: 4/4, não passa
    assert max(criterio_sassenfeld(A)) < 1      # Sassenfeld passa


def teste_slide_2x2():
    A = np.array([[2.0, -1], [1, 2]])
    b = np.array([1.0, 3])
    r = gauss_seidel(A, b, [0, 0], precisao=1e-6)
    assert np.allclose(r.x, [1, 1], atol=1e-5), r.x


def teste_trelica():
    A, b, nomes, _ = montar_trelica()
    assert raio_espectral(A) is None            # há zero na diagonal
    perm, raio = melhor_ordem(A)
    assert perm is not None and raio < 1, (perm, raio)
    r = gauss_seidel(A[:, perm], b, np.zeros(10), precisao=1e-4)
    assert r.convergiu
    x = np.zeros(10)
    x[perm] = r.x
    exato = np.linalg.solve(A, b)
    assert np.allclose(x, exato, atol=0.1), np.max(np.abs(x - exato))
    # equilíbrio global: reações somam as cargas, sem reação horizontal
    ay, ey, ax = x[nomes.index("Ay")], x[nomes.index("Ey")], x[nomes.index("Ax")]
    assert abs(ay + ey - 600) < 0.1 and abs(ax) < 0.1


def teste_singular():
    A = np.array([[1.0, 2], [2, 4]])
    assert np.linalg.matrix_rank(A) < 2


if __name__ == "__main__":
    for nome, fn in list(globals().items()):
        if nome.startswith("teste_"):
            fn()
            print("ok  ", nome)