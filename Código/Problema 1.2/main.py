"""Problema 1.2 (Tópico 1): sistemas lineares, métodos diretos.

Programa com menu. Resolve o problema 1.2 do enunciado, outro problema de
produção com a mesma estrutura (tabela de consumo e disponibilidade) ou
qualquer sistema linear digitado, pelo método de Gauss, pelo de Gauss-Jordan,
pela Fatoração LU ou pelos três, comparando os resultados.

Rodar nesta pasta:    python main.py
"""

import math

try:
    from .sistemaEquacaoLinear import METODOS, sistemaEquacaoLinear
except ImportError:      # rodando o arquivo direto, sem ser pacote
    from sistemaEquacaoLinear import METODOS, sistemaEquacaoLinear

# ---------------------------------------------------------------- dados do 1.2
# Consumo em gramas por componente produzido (linhas: materiais; colunas:
# componentes). O enunciado dá a disponibilidade em kg: 1 kg = 1000 g.
COMPONENTES = ["Componente 1", "Componente 2", "Componente 3"]
MATERIAIS = ["Metal", "Plástico", "Borracha"]
CONSUMO_G = [[15, 17, 19],        # metal
             [0.30, 0.40, 0.55],  # plástico
             [1.0, 1.2, 1.5]]     # borracha
DISPONIVEL_KG = [3.89, 0.095, 0.282]


# ---------------------------------------------------------------- formatação

def numero(valor, casas=4):
    """3.0 -> '3', 0.30 -> '0,3' (vírgula decimal, sem zeros à direita)."""
    if abs(valor) < 0.5 * 10 ** (-casas):
        valor = 0.0
    texto = f"{valor:.{casas}f}"
    if "." in texto:
        texto = texto.rstrip("0").rstrip(".")
    return texto.replace(".", ",")


def titulo(texto):
    print("\n" + "=" * 68)
    print("  " + texto)
    print("=" * 68)


def formatar_equacao(coeficientes, termo, nomes):
    """[4, 3], 960, ['x1', 'x2'] -> '4x1 + 3x2 = 960'."""
    texto = ""
    for coef, nome in zip(coeficientes, nomes):
        if coef == 0:
            continue
        modulo = abs(coef)
        parte = nome if modulo == 1 else f"{numero(modulo)}{nome}"
        if texto == "":
            texto = ("-" if coef < 0 else "") + parte
        else:
            texto += (" - " if coef < 0 else " + ") + parte
    return f"{texto or '0'} = {numero(termo)}"


def mostrar_matriz(matriz, n, recuo="    "):
    """Imprime a matriz alinhada; com n + 1 colunas, separa o termo b com '|'."""
    celulas = [[numero(v) for v in linha] for linha in matriz]
    largura = max(len(c) for linha in celulas for c in linha)
    for linha in celulas:
        partes = [c.rjust(largura) for c in linha]
        if len(linha) == n + 1:
            texto = "  ".join(partes[:n]) + "  | " + partes[n]
        else:
            texto = "  ".join(partes)
        print(recuo + texto)


# ---------------------------------------------------------------- leitura

def ler_inteiro(mensagem, minimo=1, maximo=None, padrao=None):
    while True:
        texto = input(mensagem).strip()
        if texto == "" and padrao is not None:
            return padrao
        try:
            valor = int(texto)
        except ValueError:
            print("  Digite um número inteiro.")
            continue
        if valor < minimo or (maximo is not None and valor > maximo):
            faixa = f"entre {minimo} e {maximo}" if maximo is not None else f"pelo menos {minimo}"
            print(f"  O valor deve ser {faixa}.")
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


def ler_linha_numeros(mensagem, quantidade):
    """Lê uma linha com `quantidade` números (aceita vírgula ou ponto)."""
    while True:
        partes = input(mensagem).replace(",", ".").split()
        try:
            valores = [float(p) for p in partes]
        except ValueError:
            print("  Há algo que não é número, digite a linha de novo.")
            continue
        if len(valores) != quantidade or not all(math.isfinite(v) for v in valores):
            print(f"  São necessários exatamente {quantidade} números finitos.")
            continue
        return valores


def ler_nomes(mensagem, quantidade, padrao):
    """Pede os nomes separados por vírgula; Enter usa 'padrao 1', 'padrao 2'..."""
    while True:
        texto = input(mensagem).strip()
        if texto == "":
            return [f"{padrao} {i + 1}" for i in range(quantidade)]
        nomes = [t.strip() for t in texto.split(",") if t.strip()]
        if len(nomes) == quantidade:
            return nomes
        print(f"  Digite {quantidade} nomes separados por vírgula (ou Enter para o padrão).")


def ler_sistema():
    """Sistema genérico: n e depois uma equação por linha (a_i1 ... a_in b_i)."""
    n = ler_inteiro("Número de equações (e de incógnitas): ", minimo=2)
    print(f"Digite cada equação com {n} coeficientes e o termo independente,")
    print("separados por espaço. Exemplo para 2x + y = 5:  2 1 5")
    A, b = [], []
    for i in range(n):
        linha = ler_linha_numeros(f"  Equação {i + 1}: ", n + 1)
        A.append(linha[:n])
        b.append(linha[n])
    nomes = [f"x{j + 1}" for j in range(n)]
    return A, b, nomes, [f"Equação {i + 1}" for i in range(n)], "", None


def ler_problema_de_producao():
    """Tabela de consumo: cada linha é um material, com o consumo por unidade de
    cada produto e a quantidade disponível do material."""
    n = ler_inteiro("Quantos produtos (e quantos materiais)? ", minimo=2)
    produtos = ler_nomes("Nomes dos produtos, separados por vírgula (Enter = padrão): ", n, "Produto")
    materiais = ler_nomes("Nomes dos materiais, separados por vírgula (Enter = padrão): ", n, "Material")
    print("\nPara cada material, digite o consumo por unidade de cada produto")
    print("e, no fim, a quantidade disponível (tudo na mesma unidade).")
    print("Produtos na ordem: " + ", ".join(produtos))
    A, b = [], []
    for j in range(n):
        linha = ler_linha_numeros(f"  {materiais[j]}: ", n + 1)
        A.append(linha[:n])
        b.append(linha[n])
    unidade = input("Unidade da produção (Enter = 'unidades'): ").strip() or "unidades"
    return A, b, [f"x{i + 1}" for i in range(n)], materiais, unidade, produtos


# ---------------------------------------------------------------- resolução

def residuo_maximo(A, x, b):
    return max(abs(sum(A[i][j] * x[j] for j in range(len(x))) - b[i]) for i in range(len(b)))


def escolher_metodos():
    print("\nMétodo:")
    chaves = list(METODOS)
    for i, chave in enumerate(chaves, 1):
        print(f"  {i}) {METODOS[chave][0]}")
    print(f"  {len(chaves) + 1}) Os três, comparando os resultados")
    escolha = ler_inteiro("Escolha [padrão: todos]: ", minimo=1,
                          maximo=len(chaves) + 1, padrao=len(chaves) + 1)
    return chaves if escolha == len(chaves) + 1 else [chaves[escolha - 1]]


def resolver(A, b, nomes, rotulos, unidade="", produtos=None):
    n = len(A)
    titulo("Sistema de equações lineares")
    for j in range(n):
        print(f"  {formatar_equacao(A[j], b[j], nomes)}    ({rotulos[j]})")
    print("\nForma matricial [A | b]:")
    mostrar_matriz([A[i] + [b[i]] for i in range(n)], n, recuo="  ")

    chaves = escolher_metodos()
    com_passos = ler_sim_nao("Mostrar o passo a passo?", padrao=False)

    solucoes = {}
    for chave in chaves:
        nome = METODOS[chave][0]
        passos = [] if com_passos else None
        try:
            solucoes[chave] = sistemaEquacaoLinear(A, b, metodo=chave, passos=passos)
        except ZeroDivisionError:
            print(f"\n  {nome}: o sistema não tem solução única (matriz singular).")
            return
        except ValueError as erro:
            print(f"\n  {nome}: {erro}")
            return
        if com_passos:
            titulo(nome)
            for descricao, matriz in passos:
                print(f"\n  {descricao}")
                if matriz is not None:
                    mostrar_matriz(matriz, n)

    titulo("Resultado")
    nomes_exibidos = produtos if produtos else nomes
    primeira = solucoes[chaves[0]]
    for nome, valor in zip(nomes_exibidos, primeira):
        sufixo = f" {unidade}" if unidade else ""
        print(f"  {nome:<18s} = {numero(valor, 4)}{sufixo}")

    print("\n  Verificação por substituição (resíduo máximo |A x - b|):")
    for chave in chaves:
        print(f"    {METODOS[chave][0]:<42s} {residuo_maximo(A, solucoes[chave], b):.2e}")
    if len(chaves) > 1:
        dif = max(abs(solucoes[c][i] - primeira[i]) for c in chaves for i in range(n))
        print(f"\n  Maior diferença entre os métodos: {dif:.2e}")
        print("  Os métodos chegaram à mesma solução." if dif < 1e-6
              else "  Atenção: os métodos divergem, o sistema pode estar mal condicionado.")


def dados_do_enunciado():
    n = len(COMPONENTES)
    b = [round(kg * 1000, 6) for kg in DISPONIVEL_KG]
    titulo("Problema 1.2: componentes elétricos")
    print("Consumo por componente (g):")
    print(f"  {'':<14s}" + "".join(f"{c:>14s}" for c in COMPONENTES))
    for material, linha in zip(MATERIAIS, CONSUMO_G):
        print(f"  {material:<14s}" + "".join(f"{numero(v):>14s}" for v in linha))
    print("\nDisponível por dia: " + ", ".join(
        f"{m} = {numero(kg)} kg ({numero(g)} g)"
        for m, kg, g in zip(MATERIAIS, DISPONIVEL_KG, b)))
    print("\nx1, x2, x3 = quantidade produzida por dia de cada componente.")
    return ([list(map(float, linha)) for linha in CONSUMO_G], b,
            [f"x{i + 1}" for i in range(n)], MATERIAIS,
            "por dia", COMPONENTES)


def main():
    titulo("PROBLEMA 1.2 · Sistemas lineares, métodos diretos")
    while True:
        print("\n1) Problema 1.2 do enunciado (componentes elétricos)")
        print("2) Outro problema de produção (tabela de consumo)")
        print("3) Digitar um sistema linear qualquer")
        print("0) Sair")
        escolha = ler_inteiro("Escolha: ", minimo=0, maximo=3)
        if escolha == 0:
            print("Até mais.")
            return
        if escolha == 1:
            A, b, nomes, rotulos, unidade, produtos = dados_do_enunciado()
        elif escolha == 2:
            A, b, nomes, rotulos, unidade, produtos = ler_problema_de_producao()
        else:
            A, b, nomes, rotulos, unidade, produtos = ler_sistema()
        resolver(A, b, nomes, rotulos, unidade, produtos)
        if not ler_sim_nao("\nFazer outro cálculo?", padrao=True):
            print("Até mais.")
            return


if __name__ == "__main__":
    main()
