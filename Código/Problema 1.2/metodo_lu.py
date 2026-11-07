"""Fatoração LU (com pivoteamento parcial) para resolver A x = b.

Ideia do método: decompor a matriz A em duas matrizes triangulares,
    P A = L U      (L triangular inferior com 1 na diagonal, U triangular superior,
                    P a permutação de linhas feita pelo pivoteamento),
e então resolver DOIS sistemas triangulares simples em vez de um sistema completo:
    L y = P b   (substituição progressiva)    e    U x = y   (substituição retroativa).

Vantagem: a fatoração (a parte cara) depende só de A; para resolver o mesmo A com
vários vetores b, bastaria repetir os dois sistemas triangulares.
"""


def fatoracao_lu(A, b, passos=None):
    """Resolve o sistema linear A x = b pela fatoração LU e devolve x.

    Parâmetros
    ----------
    A : lista de listas (n x n)  - coeficientes das equações (uma linha por equação)
    b : lista (n)                - termos independentes (lado direito das equações)
    passos : lista opcional      - se for informada, a função anota nela cada etapa
                                   como (título, matriz); matriz = None quando a etapa
                                   é só um texto. Serve para mostrar o passo a passo.

    Retorna
    x : lista (n) com x[0], x[1], ... (as incógnitas, na ordem das colunas de A)

    Levanta
    ValueError         - se as dimensões de A e b não forem compatíveis
    ZeroDivisionError  - se o sistema não tiver solução única (matriz singular)

    Exemplo
    2x1 +  x2 =  5
     x1 + 3x2 = 10          ->  fatoracao_lu([[2, 1], [1, 3]], [5, 10])
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

    # PASSO 2 - Preparar as matrizes da fatoração

    # U começa como uma CÓPIA de A (convertida para float) e será "escalonada"
    # até ficar triangular superior.
    # L começa zerada; nela guardaremos os multiplicadores da eliminação.
    # perm guarda a ordem das linhas (a permutação P do pivoteamento).
    U = [[float(v) for v in linha] for linha in A]
    L = [[0.0] * n for _ in range(n)]
    perm = list(range(n))

    # Tolerância: pivô menor que isto é tratado como zero (um zero matemático
    # pode aparecer como 1e-17 por causa de arredondamentos).
    maior_coeficiente = max(abs(v) for linha in A for v in linha)
    tolerancia = 1e-12 * maior_coeficiente


    # PASSO 3 - Fatoração P A = L U
    # É a mesma eliminação do método de Gauss, mas guardando cada multiplicador
    # na matriz L (na posição que ele "zerou" em U).
    # Para cada coluna k:
    #   3.1 escolher o pivô        (pivoteamento parcial)
    #   3.2 trocar linhas se preciso
    #   3.3 calcular os multiplicadores, guardá-los em L e zerar U abaixo do pivô
    for k in range(n):

        # --- 3.1 Escolha do pivô (pivoteamento parcial) ------------------
        # Da linha k para baixo, escolhemos a linha com o MAIOR valor absoluto
        # na coluna k. Isso evita dividir por zero e reduz erros de arredondamento.
        p = max(range(k, n), key=lambda i: abs(U[i][k]))

        # Se mesmo o maior candidato é praticamente zero, não há pivô: a matriz
        # é singular (determinante = 0) e o sistema NÃO tem solução única.
        if abs(U[p][k]) <= tolerancia:
            raise ZeroDivisionError("Sistema sem solução única (matriz singular).")

        # 3.2 Troca de linhas
        # Trocamos as linhas em U, na permutação e também nos multiplicadores
        # que já estavam guardados em L (colunas anteriores a k), para L e U
        # continuarem coerentes com a ordem das linhas.
        if p != k:
            U[k], U[p] = U[p], U[k]
            L[k][:k], L[p][:k] = L[p][:k], L[k][:k]
            perm[k], perm[p] = perm[p], perm[k]

        #  3.3 Multiplicadores e eliminação 
        # Para cada linha i abaixo de k:
        #     multiplicador  m = U[i][k] / U[k][k]      (guardado em L[i][k])
        #     linha_i de U  <-  linha_i - m * linha_k
        # Assim U[i][k] vira 0 e o multiplicador fica registrado em L.
        for i in range(k + 1, n):
            m = U[i][k] / U[k][k]
            L[i][k] = m
            for j in range(k, n):
                U[i][j] -= m * U[k][j]
            U[i][k] = 0.0                      # remove resíduo de arredondamento

    # A diagonal de L é 1 por definição da fatoração (L tem 1 na diagonal).
    for i in range(n):
        L[i][i] = 1.0

    # Agora vale  P A = L U.
    if passos is not None:
        passos.append(("Matriz L (multiplicadores; diagonal = 1)", [linha[:] for linha in L]))
        passos.append(("Matriz U (triangular superior)", [linha[:] for linha in U]))
        passos.append(("Ordem das linhas após o pivoteamento (permutação P): "
                       + ", ".join(str(q + 1) for q in perm), None))


    # PASSO 4 - Aplicar a mesma permutação ao vetor b
    # Como as linhas de A foram trocadas, as equações (e portanto os termos de b)
    # precisam ser reordenadas do mesmo jeito:  Pb[i] = b[perm[i]].
    # O sistema A x = b passa a ser  L U x = Pb.

    pb = [float(b[perm[i]]) for i in range(n)]
    if passos is not None:
        passos.append(("Vetor Pb (termos independentes reordenados): "
                       + ", ".join(fmt(v) for v in pb), None))


    # PASSO 5 - Substituição progressiva: resolver L y = Pb
    # Chamando y = U x, o sistema vira L y = Pb. Como L é triangular inferior,
    # resolvemos de cima para baixo (a primeira equação tem só y1):
    #     y_i = Pb_i - soma_{j < i} L_ij * y_j        (L_ii = 1, não divide)

    y = [0.0] * n
    for i in range(n):
        soma = sum(L[i][j] * y[j] for j in range(i))        # termos já conhecidos
        y[i] = pb[i] - soma
        if passos is not None:
            passos.append((f"Substituição progressiva: y{i + 1} = {fmt(pb[i])} - {fmt(soma)} "
                           f"= {fmt(y[i])}", None))


    # PASSO 6 - Substituição retroativa: resolver U x = y
    # Como U é triangular superior, resolvemos de baixo para cima (a última
    # equação tem só x_n):
    #     x_i = ( y_i - soma_{j > i} U_ij * x_j ) / U_ii

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        soma = sum(U[i][j] * x[j] for j in range(i + 1, n))  # termos já conhecidos
        x[i] = (y[i] - soma) / U[i][i]
        if passos is not None:
            passos.append((f"Substituição retroativa: x{i + 1} = ({fmt(y[i])} - {fmt(soma)}) "
                           f"/ {fmt(U[i][i])} = {fmt(x[i])}", None))


    # x[0] é a incógnita da 1ª coluna de A, x[1] a da 2ª, e assim por diante.
    return x