"""Método de Gauss (eliminação de Gauss com pivoteamento parcial) para resolver A x = b.

Ideia do método: transformar o sistema num sistema TRIANGULAR SUPERIOR usando
operações entre linhas e depois resolvê-lo de baixo para cima .
"""

def gauss(A, b, passos=None):
    """Resolve o sistema linear A x = b e devolve a lista x com a solução.
    Parâmetros
    A : lista de listas (n x n)  - coeficientes das equações (uma linha por equação)
    b : lista (n)                - termos independentes (lado direito das equações)
    passos : lista opcional      - se for informada, a função anota nela cada etapa
                                   como (título, matriz); matriz = None quando a etapa
                                   é só um texto. Serve para mostrar o passo a passo.

    Retorna
    x : lista (n) com x[0], x[1], ... (as incógnitas, na ordem das colunas de A)

    Levanta
    ValueError            - se as dimensões de A e b não forem compatíveis
    ZeroDivisionError     - se o sistema não tiver solução única (matriz singular)

    Exemplo
    2x1 +  x2 =  5
     x1 + 3x2 = 10          ->  gauss([[2, 1], [1, 3]], [5, 10])
                                 devolve [1.0, 3.0]
    """

    # Formata números nos textos do passo a passo (vírgula decimal).
    def fmt(valor):
        return f"{valor:.6g}".replace(".", ",")

    # PASSO 1 - Conferir as entradas
    # Um sistema com solução única precisa ter o mesmo número de equações e
    # de incógnitas, ou seja, A deve ser quadrada (n x n) e b deve ter n termos.

    n = len(A)
    if n == 0 or any(len(linha) != n for linha in A):
        raise ValueError("A matriz dos coeficientes deve ser quadrada (n x n).")
    if len(b) != n:
        raise ValueError("O vetor b deve ter um termo para cada equação.")


    # PASSO 2 - Montar a matriz aumentada [A | b]
    # Cada linha da matriz aumentada representa uma equação:
    #     a_i1*x1 + a_i2*x2 + ... + a_in*xn = b_i   ->   [a_i1 ... a_in | b_i]
    # Trabalhamos numa CÓPIA (convertida para float) para não alterar A e b
    # originais de quem chamou a função.

    M = [[float(v) for v in A[i]] + [float(b[i])] for i in range(n)]
    if passos is not None:
        passos.append(("Matriz aumentada inicial [A | b]", [linha[:] for linha in M]))

    # PASSO 3 - Definir quando um pivô é "zero"
    # ----------------------------------------------------------------------
    # No computador, um zero matemático pode aparecer como 1e-17 por causa de
    # arredondamentos. Por isso comparamos o pivô com uma tolerância pequena,
    # proporcional ao maior coeficiente do sistema.

    maior_coeficiente = max(abs(v) for linha in A for v in linha)
    tolerancia = 1e-12 * maior_coeficiente

    # PASSO 4 - Eliminação de Gauss (fase "para frente")

    # Objetivo: transformar o sistema num sistema TRIANGULAR SUPERIOR (zeros
    # abaixo da diagonal), que é fácil de resolver de baixo para cima.

    # Usamos apenas operações elementares entre linhas (trocar duas linhas ou
    # subtrair de uma linha um múltiplo de outra). Elas NÃO alteram a solução
    # do sistema, só deixam as equações mais simples.
    
    # Para cada coluna k (de 0 até n-1) fazemos:
    #   4.1 escolher o pivô        (o elemento M[k][k] que vai "zerar" a coluna)
    #   4.2 trocar linhas se preciso
    #   4.3 zerar os elementos abaixo do pivô
    
    for k in range(n):

        # 4.1 Escolha do pivô (pivoteamento parcial) 
        # Procuramos, da linha k para baixo, a linha cujo elemento na coluna k
        # tem o MAIOR valor absoluto. Isso evita dividir por zero (ou por um
        # número minúsculo) e reduz erros de arredondamento.
        p = max(range(k, n), key=lambda i: abs(M[i][k]))

        # Se mesmo o maior candidato é praticamente zero, a coluna k não tem
        # pivô: as equações são dependentes (ou incompatíveis) e o sistema NÃO
        # tem solução única (determinante = 0).
        if abs(M[p][k]) <= tolerancia:
            raise ZeroDivisionError("Sistema sem solução única (matriz singular).")

        # 4.2 Troca de linhas 
        # Colocamos a linha escolhida na posição k. Trocar a ordem das
        # equações não muda a solução do sistema.
        trocou = (p != k)
        if trocou:
            M[k], M[p] = M[p], M[k]

        # 4.3 Zerar os elementos abaixo do pivô 
        # Para cada linha i abaixo de k:
        #     multiplicador m = M[i][k] / M[k][k]
        #     linha_i  <-  linha_i - m * linha_k
        # Assim o elemento M[i][k] vira exatamente 0 e a coluna k fica
        # "limpa" abaixo da diagonal.
        for i in range(k + 1, n):
            m = M[i][k] / M[k][k]
            for j in range(k, n + 1):          # n + 1 inclui a coluna de b
                M[i][j] -= m * M[k][j]
            M[i][k] = 0.0                      # remove resíduo de arredondamento

        if passos is not None:
            origem = f"veio da linha {p + 1}, linhas trocadas" if trocou else "sem troca de linhas"
            passos.append((f"Coluna {k + 1}: pivô = {fmt(M[k][k])} ({origem})",
                           [linha[:] for linha in M]))

    # Neste ponto M está na forma triangular superior:
    #     a11'x1 + a12'x2 + ... + a1n'xn = b1'
    #              a22'x2 + ... + a2n'xn = b2'
    #                              ...
    #                           ann'xn   = bn'

   
   
    # PASSO 5 - Retrosubstituição (fase "para trás")

    # A última equação tem uma única incógnita: x_n = b_n' / a_nn'.
    # Com x_n conhecido, a penúltima equação passa a ter uma única incógnita,
    # e assim por diante, subindo até a primeira equação:
    #
    #     x_i = ( b_i' - soma_{j > i} a_ij' * x_j ) / a_ii'

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        soma = sum(M[i][j] * x[j] for j in range(i + 1, n))   # termos já conhecidos
        x[i] = (M[i][n] - soma) / M[i][i]
        if passos is not None:
            passos.append((f"Retrosubstituição: x{i + 1} = ({fmt(M[i][n])} - {fmt(soma)}) "
                           f"/ {fmt(M[i][i])} = {fmt(x[i])}", None))

 
    # x[0] é a incógnita da 1ª coluna de A, x[1] a da 2ª, e assim por diante.
    return x