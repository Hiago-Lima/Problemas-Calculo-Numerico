"""Teste: resolução completa do Problema 1.2 (Tópico 1, questão 2) pelos 3 métodos diretos.

Enunciado: um engenheiro supervisiona a produção de três componentes elétricos,
que usam metal, plástico e borracha. Com 3,89 kg de metal, 0,095 kg de plástico
e 0,282 kg de borracha disponíveis por dia, quantos componentes de cada tipo
podem ser produzidos por dia?

O teste:
    1. mostra os dados e modela o problema como sistema linear;
    2. resolve o sistema pelo Método de Gauss, pelo Método de Gauss-Jordan e pela
       Fatoração LU (funções do projeto), mostrando o passo a passo de cada um;
    3. confere as soluções e compara os métodos entre si;
    4. compara o tempo de execução dos três métodos;
    5. mostra o resultado final.

Rode a partir da pasta do projeto:   python3 tests/teste_problema_1_2.py
"""
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Funções do projeto: o seletor de método e o registro com os três métodos
from .sistemaEquacaoLinear import METODOS, sistemaEquacaoLinear  

# DADOS DO PROBLEMA 1.2

COMPONENTES = ["Componente 1", "Componente 2", "Componente 3"]   # incógnitas
MATERIAIS = ["Metal", "Plástico", "Borracha"]                    # uma equação cada

# Linhas = componentes, colunas = materiais em gramas
CONSUMO_G = [[15, 0.30, 1.0],
             [17, 0.40, 1.2],
             [19, 0.55, 1.5]]

# Disponibilidade diária informada em QUILOGRAMAS no enunciado.
DISPONIVEL_KG = [3.89, 0.095, 0.282]

SOLUCAO_ESPERADA = [90, 60, 80]

# Parâmetros da medição de tempo
REPETICOES_3X3 = 10000      # resoluções por rodada (sistema do problema)
RODADAS_3X3 = 7             # a melhor rodada de cada método é a usada (menos ruído)
ORDEM_GRANDE = 60           # sistema maior, só para o comparativo ficar mais nítido
REPETICOES_GRANDE = 5
RODADAS_GRANDE = 7


# FUNÇÕES DE IMPRESSÃO 
def numero(valor, casas=4):
    """Formata sem zeros à direita: 3.0 -> '3', 0.30 -> '0,3'."""
    if abs(valor) < 0.5 * 10 ** (-casas):
        valor = 0.0
    texto = f"{valor:.{casas}f}"
    if "." in texto:
        texto = texto.rstrip("0").rstrip(".")
    return texto.replace(".", ",")


def titulo(texto):
    print("\n" + "=" * 72)
    print(texto)
    print("=" * 72)


def formatar_equacao(coeficientes, termo_independente, nomes):
    """Ex.: [4, 3], 960, ['x1', 'x2'] -> '4x1 + 3x2 = 960'."""
    texto = ""
    for coef, nome in zip(coeficientes, nomes):
        if coef == 0:
            continue
        modulo = abs(coef)
        termo = nome if modulo == 1 else f"{numero(modulo)}{nome}"
        if texto == "":
            texto = ("-" if coef < 0 else "") + termo
        else:
            texto += (" - " if coef < 0 else " + ") + termo
    return f"{texto or '0'} = {numero(termo_independente)}"


def mostrar_matriz(matriz, termos_independentes=None, recuo="   "):
    """Imprime a matriz alinhada; com `termos_independentes`, mostra [A | b]."""
    celulas = [[numero(v) for v in linha] for linha in matriz]
    largura = max(len(c) for linha in celulas for c in linha)
    for i, linha in enumerate(celulas):
        texto = "  ".join(c.rjust(largura) for c in linha)
        if termos_independentes is not None:
            texto += "  | " + numero(termos_independentes[i])
        print(recuo + texto)


def residuo_maximo(A, x, b):
    """max |A x - b|: quanto a solução 'erra' as equações (deve ser ~0)."""
    return max(abs(sum(A[i][j] * x[j] for j in range(len(x))) - b[i]) for i in range(len(b)))


# MEDIÇÃO DE TEMPO

def medir_tempos(funcoes, A, b, repeticoes, rodadas):
    """Tempo médio (em segundos) de UMA resolução de A x = b, para cada método.

    A cada rodada, cada método executa `repeticoes` resoluções seguidas. Os métodos são
    INTERCALADOS (e a ordem muda de rodada em rodada) para que oscilações do computador
    afetem todos igualmente; de cada método usamos a MELHOR rodada, já que outros
    programas só podem atrasar a medição, nunca acelerá-la.
    """
    chaves = list(funcoes)
    for chave in chaves:
        funcoes[chave](A, b)                          # aquecimento (não entra na medição)
    melhor = {chave: float("inf") for chave in chaves}
    for rodada in range(rodadas):
        deslocamento = rodada % len(chaves)
        for chave in chaves[deslocamento:] + chaves[:deslocamento]:
            funcao = funcoes[chave]
            inicio = time.perf_counter()
            for _ in range(repeticoes):
                funcao(A, b)
            melhor[chave] = min(melhor[chave], time.perf_counter() - inicio)
    return {chave: melhor[chave] / repeticoes for chave in chaves}


def tabela_de_tempos(A, b, repeticoes, rodadas):
    """Mede os três métodos e imprime a tabela. Devolve {chave: tempo em segundos}."""
    funcoes = {chave: funcao for chave, (_, funcao) in METODOS.items()}
    tempos = medir_tempos(funcoes, A, b, repeticoes, rodadas)
    mais_rapido = min(tempos.values())
    print(f"  {'Método':<42s}{'Tempo por resolução':>22s}{'Relativo':>10s}")
    for chave, (nome, _) in METODOS.items():
        t = tempos[chave]
        unidade = f"{t * 1e6:,.2f} µs" if t < 1e-3 else f"{t * 1e3:,.2f} ms"
        print(f"  {nome:<42s}{unidade:>22s}{t / mais_rapido:>9.2f}x")
    return tempos


def mais_rapidos(tempos, margem=0.05):
    """Nomes dos métodos até `margem` (5%) mais lentos que o mais rápido: abaixo disso é empate técnico."""
    menor = min(tempos.values())
    return [METODOS[c][0] for c in tempos if tempos[c] <= menor * (1 + margem)]


def sistema_aleatorio(n, semente=42):
    """Sistema n x n reprodutível, com diagonal dominante (solução única garantida)."""
    sorteio = random.Random(semente)
    A = [[sorteio.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] += n
    b = [sorteio.uniform(-10, 10) for _ in range(n)]
    return A, b


# TESTE

def main():
    # Dados do problema (com a conversão de unidades)
    # A tabela está em gramas e o enunciado em kg: 1 kg = 1000 g.

    titulo("ETAPA 1 - Dados do problema 1.2")
    disponivel_g = [round(kg * 1000, 6) for kg in DISPONIVEL_KG]
    print("Consumo por componente (g):")
    print(f"  {'':<14s}" + "".join(f"{m:>10s}" for m in MATERIAIS))
    for nome, linha in zip(COMPONENTES, CONSUMO_G):
        print(f"  {nome:<14s}" + "".join(f"{numero(v):>10s}" for v in linha))
    print("\nDisponível por dia: " + ", ".join(
        f"{m} = {numero(kg)} kg = {numero(g)} g"
        for m, kg, g in zip(MATERIAIS, DISPONIVEL_KG, disponivel_g)))

    # Modelagem como sistema de equações lineares
    # x1, x2, x3 = quantidade produzida por dia de cada componente.
    # Para cada material j:  soma_i( consumo[i][j] * x_i ) = disponível[j]
    # Logo A[j][i] = consumo[i][j] .
    # ------------------------------------------------------------------
    titulo("ETAPA 2 - Sistema de equações lineares")
    n = len(COMPONENTES)
    A = [[CONSUMO_G[i][j] for i in range(n)] for j in range(n)]
    b = disponivel_g
    nomes = [f"x{i + 1}" for i in range(n)]
    for j, material in enumerate(MATERIAIS):
        print(f"  {formatar_equacao(A[j], b[j], nomes)}    ({material})")
    print("\nForma matricial [A | b]:")
    mostrar_matriz(A, b)

    #  Resolução pelos três métodos diretos
    # Usa o seletor sistemaEquacaoLinear, escolhendo o método a cada chamada.

    solucoes = {}
    for numero_metodo, (chave, (nome, _)) in enumerate(METODOS.items(), start=1):
        titulo(f"ETAPA 3.{numero_metodo} - {nome}")
        passos = []
        solucoes[chave] = sistemaEquacaoLinear(A, b, metodo=chave, passos=passos)
        for descricao, matriz in passos:
            print(f"\n  {descricao}")
            if matriz is not None:
                mostrar_matriz(matriz)

    # Conferir cada solução e comparar os métodos
    titulo("ETAPA 4 - Verificação e comparação das soluções")
    print(f"  {'Método':<42s}{'x1':>8s}{'x2':>8s}{'x3':>8s}{'Resíduo máx.':>16s}")
    for chave, (nome, _) in METODOS.items():
        x = solucoes[chave]
        print(f"  {nome:<42s}" + "".join(f"{numero(v):>8s}" for v in x)
              + f"{residuo_maximo(A, x, b):>16.2e}")
        assert all(abs(o - e) < 1e-6 for o, e in zip(x, SOLUCAO_ESPERADA)), \
            f"{nome}: solução incorreta {x}"
        assert residuo_maximo(A, x, b) < 1e-8, f"{nome}: resíduo alto"
    referencia = solucoes["gauss"]
    diferenca = max(abs(a - c) for x in solucoes.values() for a, c in zip(x, referencia))
    print(f"\n  Diferença máxima entre os métodos: {diferenca:.2e}")
    assert diferenca < 1e-8, "Os métodos deveriam concordar"

    #  Comparativo de tempo de execução
  
    titulo("ETAPA 5 - Comparativo de tempo de execução")
    repeticoes_texto = f"{REPETICOES_3X3:,}".replace(",", ".")
    print(f"\n  a) Sistema do problema 1.2 (3 x 3): {repeticoes_texto} resoluções por rodada, "
          f"melhor de {RODADAS_3X3} rodadas")
    tempos = tabela_de_tempos(A, b, REPETICOES_3X3, RODADAS_3X3)

    Ag, bg = sistema_aleatorio(ORDEM_GRANDE)
    print(f"\n  b) Sistema maior ({ORDEM_GRANDE} x {ORDEM_GRANDE}, gerado aleatoriamente) - "
          f"{REPETICOES_GRANDE} resoluções por rodada, melhor de {RODADAS_GRANDE} rodadas")
    tempos_grande = tabela_de_tempos(Ag, bg, REPETICOES_GRANDE, RODADAS_GRANDE)

    print("\n  Leitura dos resultados: no sistema 1.2 as diferenças são de poucos microssegundos"
          "\n  e incluem o custo fixo do próprio Python (a LU, por exemplo, monta L, reordena b e"
          "\n  resolve dois sistemas triangulares). No sistema maior o custo da eliminação domina:"
          "\n  Gauss e LU fazem cerca de n³/3 multiplicações e Gauss-Jordan cerca de n³/2"
          "\n  (aprox. 50% a mais, pois zera a coluna também acima do pivô).")

    # RESULTADO FINAL
    titulo("RESULTADO FINAL - Problema 1.2")
    for componente, valor in zip(COMPONENTES, solucoes["gauss"]):
        print(f"  {componente}: {numero(valor, 4)} componentes por dia")
    print("\n  Os três métodos chegaram à mesma solução.")
    for rotulo, t in (("3 x 3", tempos), (f"{ORDEM_GRANDE} x {ORDEM_GRANDE}", tempos_grande)):
        vencedores = mais_rapidos(t)
        if len(vencedores) == 1:
            resumo = vencedores[0]
        else:
            resumo = "empate técnico (diferença < 5%) entre " + " e ".join(vencedores)
        print(f"  Mais rápido no sistema {rotulo}: {resumo}")
    print("\n  TESTE APROVADO: solução confere com o esperado (90, 60, 80).")


if __name__ == "__main__":
    main()