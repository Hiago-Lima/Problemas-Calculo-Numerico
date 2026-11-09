"""Programa principal do Projeto Final, Unidade 2 (Cálculo Numérico, UNIVASF).

Reúne os quatro problemas da equipe num menu só. Rodar na pasta do projeto:

    python main.py

Como cada problema é ligado ao menu:
  - 1.2, 2.2 e 3.1: o menu abre o programa que estiver na pasta do problema
    (um arquivo .py, que não comece com "teste", com uma função main()).
  - 4.1: a interface está aqui, e usa simpson_repetido(y, h) da pasta do
    problema 4.1 e, se existir lá, trapezio_repetido(y, h).

As cores só aparecem em terminal; com a variável NO_COLOR definida saem
desligadas.
"""

import importlib.util
import math
import os
import sys
import textwrap
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
CODIGO = RAIZ / "Código"
LARGURA = 66  # largura interna das caixas

# número do tópico -> (problema, assunto, método)
PROBLEMAS = {
    1: ("1.2", "Componentes elétricos", "Métodos diretos"),
    2: ("2.2", "Treliça", "Gauss-Seidel"),
    3: ("3.1", "Lei de Moore", "Mínimos quadrados"),
    4: ("4.1", "Seção reta de um rio", "Trapézio e Simpson"),
}

# problema 4.1: seção do rio do enunciado (x de 0 a 20 m, de 2 em 2 m)
RIO_H = 2.0
RIO_Y = [0, 1.8, 2, 4, 4, 6, 4, 3.6, 3.4, 2.8, 0]


# ---------------------------------------------------------------- aparência

USAR_COR = (sys.stdout.isatty() or bool(os.environ.get("FORCE_COLOR"))) \
    and not os.environ.get("NO_COLOR")

NEGRITO, CINZA, VERMELHO, VERDE, AMARELO, CIANO = "1", "90", "31", "32", "33", "36"


def estilo(texto, *codigos):
    if not USAR_COR or not codigos:
        return texto
    return f"\033[{';'.join(codigos)}m{texto}\033[0m"


def linha(*segmentos):
    """Uma linha da caixa. Cada segmento é um texto ou (texto, códigos...).
    O preenchimento é calculado só sobre o texto visível."""
    partes, tamanho = [], 0
    for seg in segmentos:
        texto, codigos = (seg, ()) if isinstance(seg, str) else (seg[0], seg[1:])
        tamanho += len(texto)
        partes.append(estilo(texto, *codigos))
    return "│" + "".join(partes) + " " * max(0, LARGURA - tamanho) + "│"


def topo():
    print("╭" + "─" * LARGURA + "╮")


def divisoria():
    print("├" + "─" * LARGURA + "┤")


def base():
    print("╰" + "─" * LARGURA + "╯")


def centro(texto, *codigos):
    esq = (LARGURA - len(texto)) // 2
    return linha(" " * esq, (texto, *codigos))


def aviso(texto):
    print(estilo("  ! " + texto, AMARELO))


def erro(texto):
    print(estilo("  ✗ " + texto, VERMELHO))


def prompt(texto):
    return input(estilo("  ▸ ", CIANO) + texto)


# ---------------------------------------------------------------- leitura

def ler_numero(mensagem):
    """Lê um número real (aceita vírgula ou ponto)."""
    while True:
        texto = prompt(mensagem).strip()
        try:
            valor = float(texto.replace(",", "."))
        except ValueError:
            erro("Valor inválido, digite um número.")
            continue
        if not math.isfinite(valor):
            erro("Valor inválido, digite um número finito.")
            continue
        return valor


def ler_lista(mensagem):
    """Lê vários números numa linha, separados por espaço."""
    while True:
        partes = prompt(mensagem).replace(",", ".").split()
        try:
            numeros = [float(p) for p in partes]
        except ValueError:
            erro("Há algo que não é número, digite a linha de novo.")
            continue
        if not all(math.isfinite(v) for v in numeros):
            erro("Todos os valores precisam ser finitos.")
            continue
        return numeros


def ler_opcao(mensagem, validas):
    while True:
        texto = prompt(mensagem).strip()
        if texto in validas:
            return texto
        erro("Opção inexistente.")


def ler_sim_nao(mensagem, padrao=True):
    sufixo = " [S/n]: " if padrao else " [s/N]: "
    while True:
        texto = prompt(mensagem + sufixo).strip().lower()
        if texto == "":
            return padrao
        if texto in ("s", "sim"):
            return True
        if texto in ("n", "nao", "não"):
            return False
        erro("Responda s ou n.")


# ------------------------------------------------- pastas e módulos

def pasta_do_problema(topico):
    """Pasta 'Código/Problema <n>'. Se não houver, procura pelo tópico, então
    uma pasta chamada 'Problema 3.2' no lugar de 'Problema 3.1' também serve."""
    exata = CODIGO / f"Problema {PROBLEMAS[topico][0]}"
    if exata.is_dir():
        return exata
    for pasta in sorted(CODIGO.glob(f"Problema {topico}.*")):
        if pasta.is_dir():
            return pasta
    return None


def arquivos_do_programa(pasta):
    """Arquivos .py da pasta que não são testes."""
    if pasta is None:
        return []
    return sorted(
        p for p in pasta.glob("*.py")
        if not p.name.startswith(("teste", "test", "_"))
    )


_cache = {}


def carregar(arquivo):
    """Importa um arquivo .py pelo caminho. A pasta dele entra no sys.path
    para que os imports entre arquivos da mesma pasta funcionem."""
    if arquivo in _cache:
        return _cache[arquivo]
    pasta = str(arquivo.parent)
    entrou = pasta not in sys.path
    if entrou:
        sys.path.insert(0, pasta)
    try:
        spec = importlib.util.spec_from_file_location(arquivo.stem, arquivo)
        modulo = importlib.util.module_from_spec(spec)
        sys.modules[arquivo.stem] = modulo
        spec.loader.exec_module(modulo)
    finally:
        if entrou:
            sys.path.remove(pasta)
    _cache[arquivo] = modulo
    return modulo


def procurar_funcao(topico, nome):
    """Primeira função com esse nome nos arquivos da pasta do problema."""
    for arquivo in arquivos_do_programa(pasta_do_problema(topico)):
        try:
            funcao = getattr(carregar(arquivo), nome, None)
        except Exception:
            continue
        if callable(funcao):
            return funcao
    return None


# ------------------------------------------------- problemas 1.2, 2.2, 3.1

def rodar_programa_da_pasta(topico):
    problema = PROBLEMAS[topico][0]
    pasta = pasta_do_problema(topico)
    candidatos, falhas = [], []
    for arquivo in arquivos_do_programa(pasta):
        try:
            modulo = carregar(arquivo)
        except Exception as e:      # um arquivo quebrado não derruba os outros
            falhas.append((arquivo, e))
            continue
        if callable(getattr(modulo, "main", None)):
            candidatos.append(modulo)

    if not candidatos and falhas:
        print()
        erro(f"Não foi possível abrir o programa do problema {problema}:")
        for arquivo, e in falhas:
            print(estilo(f"    {arquivo.name}: {e}", CINZA))
            if isinstance(e, ModuleNotFoundError) and e.name:
                aviso(f"Falta instalar: {e.name}")
        return
    if not candidatos:
        print()
        aviso(f"O programa do problema {problema} ainda não está na pasta")
        print(estilo(f"    {pasta if pasta else CODIGO / ('Problema ' + problema)}", CINZA))
        print(estilo("    (um arquivo .py, sem 'teste' no nome, com uma função main())", CINZA))
        return
    if len(candidatos) == 1:
        candidatos[0].main()
        return
    print(f"\n  A pasta do problema {problema} tem mais de um programa:")
    for i, modulo in enumerate(candidatos, 1):
        print(f"    {estilo(str(i), AMARELO, NEGRITO)}  {Path(modulo.__file__).name}")
    escolha = ler_opcao("Escolha: ", [str(i) for i in range(1, len(candidatos) + 1)])
    candidatos[int(escolha) - 1].main()


# ------------------------------------------------- problema 4.1

def mostrar_pontos(y, h):
    n = len(y) - 1
    print(f"\n  {n} intervalos de h = {h:g}  ({len(y)} pontos)\n")
    colunas = [f"{i * h:g}" for i in range(len(y))], [f"{v:g}" for v in y]
    larg = max(len(t) for linha_ in colunas for t in linha_) + 2
    # quebra em blocos para caber na tela
    por_bloco = max(1, (LARGURA - 2 - 16) // larg)
    for ini in range(0, len(y), por_bloco):
        fim = ini + por_bloco
        print("  " + estilo("x (m)".ljust(16), CINZA)
              + "".join(estilo(t.rjust(larg), NEGRITO) for t in colunas[0][ini:fim]))
        print("  " + estilo("profundidade".ljust(16), CINZA)
              + "".join(t.rjust(larg) for t in colunas[1][ini:fim]))
        if fim < len(y):
            print()


def calcular_4_1(y, h):
    mostrar_pontos(y, h)
    trapezio = procurar_funcao(4, "trapezio_repetido")
    simpson = procurar_funcao(4, "simpson_repetido")
    resultados = {}

    print()
    topo()
    print(linha(" ", ("Área da seção", NEGRITO)))
    divisoria()
    for nome, funcao in (("Trapézio repetido", trapezio),
                         ("Simpson 1/3 repetido", simpson)):
        if funcao is None:
            print(linha(f" {nome:<24}", ("ainda não está na pasta do 4.1", AMARELO)))
            continue
        try:
            resultados[nome] = funcao(y, h)
        except ValueError as e:
            print(linha(f" {nome:<24}", ("não foi possível", VERMELHO)))
            for parte in textwrap.wrap(str(e), LARGURA - 6):
                print(linha("   ", (parte, CINZA)))
            continue
        print(linha(f" {nome:<24}", (f"{resultados[nome]:.4f}", VERDE, NEGRITO)))
    if len(resultados) == 2:
        dif = abs(resultados["Simpson 1/3 repetido"] - resultados["Trapézio repetido"])
        divisoria()
        print(linha(f" {'Diferença entre os dois':<24}", f"{dif:.4f}"))
    base()


def problema_4_1():
    print()
    topo()
    print(centro("Problema 4.1 · Área da seção reta de um rio", NEGRITO, CIANO))
    base()
    if not arquivos_do_programa(pasta_do_problema(4)):
        aviso("Nenhum programa encontrado na pasta do problema 4.1.")
        return
    while True:
        print()
        print(f"  {estilo('1', AMARELO, NEGRITO)}  Rio do enunciado {estilo('(x de 0 a 20 m, h = 2 m)', CINZA)}")
        print(f"  {estilo('2', AMARELO, NEGRITO)}  Digitar outros dados")
        print(f"  {estilo('0', AMARELO, NEGRITO)}  Voltar")
        print()
        escolha = ler_opcao("Escolha: ", ("0", "1", "2"))
        if escolha == "0":
            return
        if escolha == "1":
            calcular_4_1(RIO_Y, RIO_H)
        else:
            h = ler_numero("Distância h entre as medições (m): ")
            if h <= 0:
                erro("O passo h deve ser positivo.")
                continue
            print(estilo("    Profundidades na ordem, separadas por espaço.", CINZA))
            y = ler_lista("y0 y1 y2 ...: ")
            if len(y) < 3:
                erro("São necessários pelo menos 3 pontos.")
                continue
            calcular_4_1(y, h)
        print()
        if not ler_sim_nao("Fazer outro cálculo neste problema?", padrao=True):
            return


# ------------------------------------------------- menu

def pronto(topico):
    return bool(arquivos_do_programa(pasta_do_problema(topico)))


def mostrar_menu():
    print()
    topo()
    print(centro("CÁLCULO NUMÉRICO", NEGRITO, CIANO))
    print(centro("Projeto Final · Unidade 2", NEGRITO))
    print(centro("UNIVASF · Prof. Jorge Cavalcanti", CINZA))
    divisoria()
    print(linha())
    for topico, (problema, assunto, metodo) in PROBLEMAS.items():
        if pronto(topico):
            marca = ("● pronto", VERDE)
        else:
            marca = ("○ pendente", CINZA)
        print(linha("  ", (f"[{topico}]", AMARELO, NEGRITO), "  ",
                    (problema, NEGRITO), "  ",
                    f"{assunto:<22}", " ",
                    (f"{metodo:<18}", CINZA), "  ", marca))
    print(linha())
    print(linha("  ", ("[0]", AMARELO, NEGRITO), "  Sair"))
    base()


def main():
    while True:
        mostrar_menu()
        escolha = ler_opcao("Escolha: ", ("0", "1", "2", "3", "4"))
        if escolha == "0":
            print("\n  Até mais.\n")
            return
        topico = int(escolha)
        try:
            if topico == 4:
                problema_4_1()
            else:
                rodar_programa_da_pasta(topico)
        except (KeyboardInterrupt, EOFError):
            print()
            aviso("Cálculo interrompido.")
        except Exception as e:
            print()
            erro(f"Erro no problema {PROBLEMAS[topico][0]}: {e}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n  Até mais.\n")
