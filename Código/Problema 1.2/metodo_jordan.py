"""Método da Eliminação de Gauss-Jordan (com pivoteamento parcial) para resolver A x = b.

Ideia do método: em vez de parar na forma triangular (como o método de Gauss),
continuamos até transformar a matriz A na matriz IDENTIDADE. Quando isso acontece,
a coluna do lado direito já é a solução, e não há retrosubstituição.

Este arquivo é INDEPENDENTE: não importa nada do projeto, então pode ser
copiado e usado sozinho. Se o sistema for singular, levanta ZeroDivisionError.
"""


def gauss_jordan(A, b, passos=None):
    """Resolve o sistema linear A x = b pelo método de Gauss-Jordan e devolve x.

    Parâmetros
    ----------
    A : lista de listas (n x n)  - coeficientes das equações (uma linha por equação)
    b : lista (n)                - termos independentes (lado direito das equações)
    passos : lista opcional      - se for informada, a função anota nela cada etapa
                                   como (título, matriz); matriz = None quando a etapa
                                   é só um texto. Serve para mostrar o passo a passo.

    Retorna
    -------
    x : lista (n) com x[0], x[1], ... (as incógnitas, na ordem das colunas de A)

    Levanta
    -------
    ValueError         - se as dimensões de A e b não forem compatíveis
    ZeroDivisionError  - se o sistema não tiver solução única (matriz singular)

    Exemplo
    -------
    2x1 +  x2 =  5
     x1 + 3x2 = 10          ->  gauss_jordan([[2, 1], [1, 3]], [5, 10])
                                 devolve [1.0, 3.0]
    """

    # Formata números nos textos do passo a passo (vírgula decimal).
    def fmt(valor):
        return f"{valor:.6g}".replace(".", ",")


    # PASSO 1 - Conferir as entradas
    # Um sistema com solução única precisa ter o mesmo número de equações e
    # de incógnitas: A deve ser quadrada (n x n) e b deve ter n termos.
    n = len(A)
    if n == 0 or any(len(linha) != n for linha in A):
        raise ValueError("A matriz dos coeficientes deve ser quadrada (n x n).")
    if len(b) != n:
        raise ValueError("O vetor b deve ter um termo para cada equação.")


    # PASSO 2 - Montar a matriz aumentada [A | b]
    # Cada linha representa uma equação:  [a_i1 ... a_in | b_i].
    # Trabalhamos numa CÓPIA (convertida para float) para não alterar A e b
    # originais de quem chamou a função.
    M = [[float(v) for v in A[i]] + [float(b[i])] for i in range(n)]
    if passos is not None:
        passos.append(("Matriz aumentada inicial [A | b]", [linha[:] for linha in M]))


    # PASSO 3 - Definir quando um pivô é "zero"
    # No computador, um zero matemático pode aparecer como 1e-17 por causa de
    # arredondamentos. Comparamos o pivô com uma tolerância pequena,
    # proporcional ao maior coeficiente do sistema.

    maior_coeficiente = max(abs(v) for linha in A for v in linha)
    tolerancia = 1e-12 * maior_coeficiente

    # PASSO 4 - Eliminação de Gauss-Jordan
    # Objetivo: transformar [A | b] em [I | x], onde I é a identidade.
    # Só usamos operações elementares entre linhas (trocar linhas, multiplicar
    # uma linha por um número, somar um múltiplo de uma linha a outra); elas
    # NÃO alteram a solução do sistema.
    

    # Para cada coluna k (de 0 até n-1) fazemos:
    #   4.1 escolher o pivô        (o elemento que vai ficar igual a 1)
    #   4.2 trocar linhas se preciso
    #   4.3 dividir a linha do pivô pelo próprio pivô (o pivô vira 1)
    #   4.4 zerar a coluna k em TODAS as outras linhas (acima E abaixo)
    for k in range(n):

        # 4.1 Escolha do pivô (pivoteamento parcial) 
        # Da linha k para baixo, escolhemos a linha cujo elemento na coluna k
        # tem o MAIOR valor absoluto. Isso evita dividir por zero (ou por um
        # número minúsculo) e reduz erros de arredondamento.
        p = max(range(k, n), key=lambda i: abs(M[i][k]))

        # Se mesmo o maior candidato é praticamente zero, a coluna k não tem
        # pivô: o sistema NÃO tem solução única (determinante = 0).
        if abs(M[p][k]) <= tolerancia:
            raise ZeroDivisionError("Sistema sem solução única (matriz singular).")

        # 4.2 Troca de linhas 
        # Trocar a ordem das equações não muda a solução do sistema.
        trocou = (p != k)
        if trocou:
            M[k], M[p] = M[p], M[k]

        # 4.3 Normalização da linha do pivô
        # Dividimos a linha inteira pelo pivô, de modo que M[k][k] passe a ser 1.
        # (Como a equação inteira é dividida, ela continua equivalente.)
        pivo = M[k][k]
        M[k] = [v / pivo for v in M[k]]

        # 4.4 Zerar a coluna k nas outras linhas 
        # Para cada linha i diferente de k (acima e abaixo do pivô):
        #     multiplicador m = M[i][k]
        #     linha_i  <-  linha_i - m * linha_k
        # Como M[k][k] = 1, o elemento M[i][k] vira exatamente 0.
        # Esta é a diferença para o método de Gauss, que zera só ABAIXO do pivô.
        for i in range(n):
            if i == k:
                continue
            m = M[i][k]
            for j in range(k, n + 1):          # n + 1 inclui a coluna de b
                M[i][j] -= m * M[k][j]
            M[i][k] = 0.0                      # remove resíduo de arredondamento

        if passos is not None:
            origem = f"veio da linha {p + 1}, linhas trocadas" if trocou else "sem troca de linhas"
            passos.append((f"Coluna {k + 1}: pivô = {fmt(pivo)} ({origem}); "
                           f"linha {k + 1} dividida pelo pivô e coluna {k + 1} zerada nas outras linhas",
                           [linha[:] for linha in M]))

    # Neste ponto a matriz aumentada está na forma [I | x]:
    #     1 0 0 | x1
    #     0 1 0 | x2
    #     0 0 1 | x3
    # Cada equação ficou do tipo  1*x_i = valor.



    # Não existe retrosubstituição: a solução é a última coluna da matriz.
    x = [M[i][n] for i in range(n)]
    if passos is not None:
        for i in range(n):
            passos.append((f"Solução lida da última coluna: x{i + 1} = {fmt(x[i])}", None))

    # x[0] é a incógnita da 1ª coluna de A, x[1] a da 2ª, e assim por diante.
    return x