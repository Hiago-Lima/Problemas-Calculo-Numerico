"""Método de Gauss-Seidel para sistemas lineares (Tópico 2, problema 2.2: treliça).

Resolve qualquer sistema A x = b digitado pelo usuário e também monta
a treliça do enunciado, com cargas e ângulos que podem ser trocados.

Critério de parada:
    dR = max|x_i(k+1) - x_i(k)| / max|x_i(k+1)|  <  precisão
        
"""

import math
from dataclasses import dataclass

import numpy as np


# ---------------------------------------------------------------- leitura

def ler_numero(mensagem, padrao=None):
    """Lê um número real (aceita vírgula ou ponto). Enter usa o padrão."""
    while True:
        texto = input(mensagem).strip()
        if texto == "" and padrao is not None:
            return padrao
        try:
            valor = float(texto.replace(",", "."))
        except ValueError:
            print("  Valor inválido, digite um número.")
            continue
        if not math.isfinite(valor):
            print("  Valor inválido, digite um número finito.")
            continue
        return valor


def ler_inteiro(mensagem, minimo=1, padrao=None):
    while True:
        texto = input(mensagem).strip()
        if texto == "" and padrao is not None:
            return padrao
        try:
            valor = int(texto)
        except ValueError:
            print("  Digite um número inteiro.")
            continue
        if valor < minimo:
            print(f"  O valor deve ser pelo menos {minimo}.")
            continue
        return valor


def ler_sim_nao(mensagem, padrao=True):
    sufixo = " [S/n]: " if padrao else " [s/N]: "
    while True:
        texto = input(mensagem + sufixo).strip().lower()
        if texto == "":
            return padrao
        if texto in ("s", "sim"):
            return True
        if texto in ("n", "nao", "não"):
            return False
        print("  Responda s ou n.")


def ler_sistema():
    """Pede a ordem e as linhas do sistema. Cada linha: a_i1 ... a_in b_i."""
    n = ler_inteiro("Ordem do sistema (número de equações): ", minimo=2)
    print(f"Digite cada equação com {n} coeficientes e o termo independente,")
    print("separados por espaço. Exemplo para 2x + y = 5:  2 1 5")
    A = np.zeros((n, n))
    b = np.zeros(n)
    i = 0
    while i < n:
        partes = input(f"  Equação {i + 1}: ").replace(",", ".").split()
        try:
            numeros = [float(p) for p in partes]
        except ValueError:
            print("  Há algo que não é número, digite a linha de novo.")
            continue
        if len(numeros) != n + 1 or not all(math.isfinite(v) for v in numeros):
            print(f"  São necessários exatamente {n + 1} números finitos.")
            continue
        A[i, :] = numeros[:n]
        b[i] = numeros[n]
        i += 1
    nomes = [f"x{j + 1}" for j in range(n)]
    rotulos = [f"Equação {i + 1}" for i in range(n)]
    return A, b, nomes, rotulos


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


def ler_trelica():
    print("Treliça do enunciado: nós A (apoio fixo), B, C, D e E (apoio móvel).")
    print("Cargas verticais para baixo em B e em C. Enter mantém o valor do enunciado.")
    carga_b = ler_numero("  Carga em B [500]: ", 500.0)
    carga_c = ler_numero("  Carga em C [100]: ", 100.0)
    ang_ab = ler_numero("  Ângulo da barra AB com a horizontal, em graus [45]: ", 45.0)
    ang_bd = ler_numero("  Ângulo da barra BD com a horizontal, em graus [45]: ", 45.0)
    ang_cd = ler_numero("  Ângulo da barra CD com a horizontal, em graus [60]: ", 60.0)
    ang_ce = ler_numero("  Ângulo da barra CE com a horizontal, em graus [30]: ", 30.0)
    return montar_trelica(carga_b, carga_c, ang_ab, ang_bd, ang_cd, ang_ce)


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


# ---------------------------------------------------------------- saída

def termo(coef, nome, primeiro):
    sinal = "-" if coef < 0 else "+"
    valor = f"{abs(coef):.4f}".rstrip("0").rstrip(".")
    if valor == "1":
        valor = ""
    corpo = f"{valor}{nome}" if valor == "" else f"{valor}*{nome}"
    if primeiro:
        return ("-" if coef < 0 else "") + corpo
    return f" {sinal} {corpo}"


def mostrar_sistema(A, b, nomes, rotulos):
    print("\nSistema linear:")
    for i in range(len(b)):
        partes, primeiro = "", True
        for j in range(len(b)):
            if A[i, j] != 0:
                partes += termo(A[i, j], nomes[j], primeiro)
                primeiro = False
        independente = f"{b[i]:.6g}"
        print(f"  {rotulos[i]:<16}: {partes} = {independente}")


def mostrar_criterios(A):
    alfas = criterio_linhas(A)
    betas = criterio_sassenfeld(A)
    raio = raio_espectral(A)
    print("\nCritérios de convergência (matriz já na ordem usada):")
    print(f"  Linhas      : max alfa_i = {max(alfas):.4f}  "
          f"({'atendido' if max(alfas) < 1 else 'não atendido'})")
    print(f"  Sassenfeld  : M = max beta_i = {max(betas):.4f}  "
          f"({'atendido' if max(betas) < 1 else 'não atendido'})")
    if raio is None:
        print("  Raio espectral: não definido (há zero na diagonal)")
    else:
        print(f"  Raio espectral da iteração: {raio:.4f}  "
              f"({'< 1, converge' if raio < 1 else '>= 1, não converge'})")
    return max(alfas) < 1 or max(betas) < 1, raio


def mostrar_iteracoes(historico, nomes):
    larg = 11
    cab = f"{'k':>4} " + " ".join(f"{n:>{larg}}" for n in nomes) + f" {'dR':>11}"
    print(cab)
    print("-" * len(cab))
    for k, x, dr in historico:
        linha = f"{k:>4} " + " ".join(f"{v:>{larg}.4f}" for v in x)
        linha += f" {'-':>11}" if dr is None else f" {dr:>11.3e}"
        print(linha)


def classificar(valor, tolerancia):
    if abs(valor) <= tolerancia:
        return "nula"
    return "tração" if valor > 0 else "compressão"


# ---------------------------------------------------------------- programa

def resolver(A, b, nomes, rotulos, e_trelica=False):
    n = len(b)
    mostrar_sistema(A, b, nomes, rotulos)

    if np.linalg.matrix_rank(A) < n:
        print("\nO sistema não tem solução única (matriz singular). "
              "Gauss-Seidel não se aplica.")
        return

    # Ordem das incógnitas: mantém a original se já converge.
    ordem = list(range(n))
    raio = raio_espectral(A)
    if raio is None or raio >= 1:
        perm, melhor = melhor_ordem(A)
        if perm is not None and (raio is None or melhor < raio):
            ordem = perm
            print("\nA ordem original das incógnitas não serve (zero na diagonal ou raio >= 1)."
                  "\nNova ordem das incógnitas: " + ", ".join(nomes[j] for j in ordem))
        elif perm is None:
            print("\nNão existe ordem das incógnitas com diagonal sem zeros; "
                  "Gauss-Seidel não se aplica.")
            return
    Ao = A[:, ordem]
    nomes_o = [nomes[j] for j in ordem]

    garantido, raio = mostrar_criterios(Ao)
    if not garantido:
        print("  Os dois critérios são só suficientes, não necessários: "
              "falhar neles não prova que diverge.")
    if raio is not None and raio >= 1:
        print("  Atenção: com essa ordem o método não converge. "
              "Vou tentar mesmo assim, até o limite de iterações.")

    print()
    precisao = ler_numero("Precisão (dR) [0.0001]: ", 1e-4)
    max_iter = ler_inteiro("Máximo de iterações [500]: ", minimo=1, padrao=500)
    print("Chute inicial: 1) zeros   2) b_i / a_ii   3) digitar")
    opcao = ler_inteiro("Escolha [1]: ", minimo=1, padrao=1)
    if opcao == 2:
        x0 = b / np.diag(Ao)
    elif opcao == 3:
        x0 = np.array([ler_numero(f"  {nome} inicial: ") for nome in nomes_o])
    else:
        x0 = np.zeros(n)

    r = gauss_seidel(Ao, b, x0, precisao, max_iter)

    if ler_sim_nao("Mostrar a tabela de iterações?", padrao=True):
        print()
        mostrar_iteracoes(r.historico, nomes_o)

    print()
    if r.convergiu:
        print(f"Convergiu em {r.iteracoes} iterações (dR final = {r.dr:.3e}).")
    else:
        print(f"Não convergiu em {r.iteracoes} iterações (dR final = {r.dr:.3e}).")

    x = np.zeros(n)
    x[ordem] = r.x
    tol = 10 * precisao * max(np.max(np.abs(x)), 1e-12)
    print("\nSolução (na ordem original das incógnitas):")
    for nome, v in zip(nomes, x):
        extra = ""
        if e_trelica and nome.startswith("F"):
            extra = f"   ({classificar(v, tol)})"
        print(f"  {nome:<6} = {v:>12.4f}{extra}")

    residuo = np.max(np.abs(A @ x - b))
    print(f"\nVerificação: maior resíduo |A x - b| = {residuo:.3e}")
    try:
        direta = np.linalg.solve(A, b)
        print(f"Conferência com solução direta: maior diferença = "
              f"{np.max(np.abs(x - direta)):.3e}")
    except np.linalg.LinAlgError:
        pass


def main():
    print("=" * 62)
    print("  Método de Gauss-Seidel para sistemas lineares")
    print("=" * 62)
    while True:
        print("\n1) Treliça do enunciado (problema 2.2)")
        print("2) Digitar outro sistema linear")
        print("0) Sair")
        escolha = ler_inteiro("Escolha: ", minimo=0)
        if escolha == 0:
            print("Até mais.")
            return
        if escolha == 1:
            A, b, nomes, rotulos = ler_trelica()
            resolver(A, b, nomes, rotulos, e_trelica=True)
        elif escolha == 2:
            A, b, nomes, rotulos = ler_sistema()
            resolver(A, b, nomes, rotulos)
        else:
            print("  Opção inexistente.")
            continue
        if not ler_sim_nao("\nFazer outro cálculo?", padrao=True):
            print("Até mais.")
            return


if __name__ == "__main__":
    main()