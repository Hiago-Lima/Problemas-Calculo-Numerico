"""Método de Gauss-Seidel para sistemas lineares (Tópico 2, problema 2.2: treliça).

Aqui ficam o método e a montagem do sistema da treliça. O programa com menu,
a leitura dos dados e a saída na tela estão em main.py.

Critério de parada:
    dR = max|x_i(k+1) - x_i(k)| / max|x_i(k+1)|  <  precisão
"""

import math
from dataclasses import dataclass

import numpy as np

# ---------------------------------------------------------------- treliça

def montar_trelica(carga_b=500.0, carga_c=100.0, ang_ab=45.0, ang_bd=45.0,
                   ang_cd=60.0, ang_ce=30.0):
    """Sistema da treliça do enunciado (5 nós, 7 barras, 3 reações).

    Nós: A (apoio fixo, esquerda), B (topo esquerdo), C (topo direito),
    D (embaixo, no meio) e E (apoio móvel, direita). Barras: AB, BC, BD, CD,
    CE, AD, DE. Os ângulos são medidos com a horizontal. Tração é positiva;
    as reações Ax e Ay são positivas para a direita e para cima.
    """
    c = lambda g: math.cos(math.radians(g))
    s = lambda g: math.sin(math.radians(g))
    nomes = ["F_AB", "F_BC", "F_BD", "F_CD", "F_CE", "F_AD", "F_DE",
             "Ax", "Ay", "Ey"]
    col = {nome: j for j, nome in enumerate(nomes)}
    A = np.zeros((10, 10))
    b = np.zeros(10)

    def equacao(i, termos, termo_indep=0.0):
        for nome, coef in termos.items():
            A[i, col[nome]] = coef
        b[i] = termo_indep

    equacao(0, {"F_AB": c(ang_ab), "F_AD": 1, "Ax": 1})
    equacao(1, {"F_AB": s(ang_ab), "Ay": 1})
    equacao(2, {"F_AB": -c(ang_ab), "F_BD": c(ang_bd), "F_BC": 1})
    equacao(3, {"F_AB": -s(ang_ab), "F_BD": -s(ang_bd)}, carga_b)
    equacao(4, {"F_BC": -1, "F_CD": -c(ang_cd), "F_CE": c(ang_ce)})
    equacao(5, {"F_CD": -s(ang_cd), "F_CE": -s(ang_ce)}, carga_c)
    equacao(6, {"F_AD": -1, "F_BD": -c(ang_bd), "F_CD": c(ang_cd), "F_DE": 1})
    equacao(7, {"F_BD": s(ang_bd), "F_CD": s(ang_cd)})
    equacao(8, {"F_CE": -c(ang_ce), "F_DE": -1})
    equacao(9, {"F_CE": s(ang_ce), "Ey": 1})
    rotulos = ["Nó A, soma Fx", "Nó A, soma Fy", "Nó B, soma Fx",
               "Nó B, soma Fy", "Nó C, soma Fx", "Nó C, soma Fy",
               "Nó D, soma Fx", "Nó D, soma Fy", "Nó E, soma Fx",
               "Nó E, soma Fy"]
    return A, b, nomes, rotulos


# ---------------------------------------------------------------- critérios

def criterio_linhas(A):
    """alfa_i = soma |a_ij| (j != i) / |a_ii|. Converge se o maior for < 1."""
    n = len(A)
    alfas = []
    for i in range(n):
        if A[i, i] == 0:
            alfas.append(math.inf)
        else:
            resto = sum(abs(A[i, j]) for j in range(n) if j != i)
            alfas.append(resto / abs(A[i, i]))
    return alfas


def criterio_sassenfeld(A):
    """beta_i do slide do professor. Converge se o maior for < 1."""
    n = len(A)
    betas = []
    for i in range(n):
        if A[i, i] == 0:
            betas.append(math.inf)
            continue
        soma = sum(abs(A[i, j]) * betas[j] for j in range(i))
        soma += sum(abs(A[i, j]) for j in range(i + 1, n))
        betas.append(soma / abs(A[i, i]))
    return betas


def raio_espectral(A):
    """Raio espectral da matriz de iteração de Gauss-Seidel (None se a_ii = 0).

    O método converge, para qualquer chute inicial, se e somente se ele é < 1.
    """
    if np.any(np.diag(A) == 0):
        return None
    inferior = np.tril(A)
    T = -np.linalg.solve(inferior, A - inferior)
    return float(max(abs(np.linalg.eigvals(T))))


def melhor_ordem(A, limite=20000):
    """Procura uma troca de colunas (ordem das incógnitas) com diagonal não
    nula e menor raio espectral. Devolve (permutação, raio) ou (None, None).

    A coluna perm[i] passa a ocupar a posição i. Os candidatos de cada linha
    são testados do maior |a_ij| para o menor, e a busca para em `limite`
    arranjos completos.
    """
    n = len(A)
    candidatos = [sorted((j for j in range(n) if A[i, j] != 0),
                         key=lambda j: -abs(A[i, j])) for i in range(n)]
    melhor = {"perm": None, "raio": None, "testados": 0}

    def busca(i, usadas, perm):
        if melhor["testados"] >= limite:
            return
        if i == n:
            melhor["testados"] += 1
            raio = raio_espectral(A[:, perm])
            if raio is not None and (melhor["raio"] is None or raio < melhor["raio"]):
                melhor["perm"], melhor["raio"] = perm[:], raio
            return
        for j in candidatos[i]:
            if j not in usadas:
                perm.append(j)
                busca(i + 1, usadas | {j}, perm)
                perm.pop()

    busca(0, frozenset(), [])
    return melhor["perm"], melhor["raio"]


# ---------------------------------------------------------------- método

@dataclass
class Resultado:
    x: np.ndarray
    iteracoes: int
    dr: float
    convergiu: bool
    historico: list  # (k, x, dR); k = 0 é o chute inicial


def gauss_seidel(A, b, x0, precisao=1e-4, max_iter=500):
    n = len(b)
    x = np.array(x0, dtype=float)
    historico = [(0, x.copy(), None)]
    dr = math.inf
    for k in range(1, max_iter + 1):
        anterior = x.copy()
        with np.errstate(all="ignore"):  # em divergência o valor estoura
            for i in range(n):
                soma = b[i] - sum(A[i, j] * x[j] for j in range(n) if j != i)
                x[i] = soma / A[i, i]
        if not np.all(np.isfinite(x)):
            return Resultado(x, k, math.inf, False, historico)
        maior = np.max(np.abs(x))
        diferenca = np.max(np.abs(x - anterior))
        if maior == 0:
            dr = 0.0 if diferenca == 0 else math.inf
        else:
            dr = diferenca / maior
        historico.append((k, x.copy(), dr))
        if dr < precisao:
            return Resultado(x, k, dr, True, historico)
    return Resultado(x, max_iter, dr, False, historico)
