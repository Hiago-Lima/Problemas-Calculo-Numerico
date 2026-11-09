"""Seletor dos métodos diretos para resolver sistemas de equações lineares A x = b.

Os três métodos da disciplina ficam cada um em seu arquivo:
    metodo_gauss.py   - Método de Gauss (eliminação + retrosubstituição)
    metodo_jordan.py  - Método da Eliminação de Gauss-Jordan
    metodo_lu.py      - Fatoração LU

A função sistemaEquacaoLinear só ESCOLHE qual deles usar; toda a matemática de
cada método está no respectivo arquivo.
"""
import unicodedata

try:
    from .metodo_diretoGaus import gauss
    from .metodo_jordan import gauss_jordan
    from .metodo_lu import fatoracao_lu
except ImportError:      # arquivo usado direto da pasta, sem ser pacote
    from metodo_diretoGaus import gauss
    from metodo_jordan import gauss_jordan
    from metodo_lu import fatoracao_lu

# Registro dos métodos: chave -> (nome para exibir, função).
METODOS = {
    "gauss": ("Método de Gauss (pivoteamento parcial)", gauss),
    "jordan": ("Método de Gauss-Jordan", gauss_jordan),
    "lu": ("Fatoração LU", fatoracao_lu),
}

# Nomes alternativos aceitos (já sem acentos, espaços ou hífens, em minúsculas).
_APELIDOS = {
    "gauss": "gauss", "eliminacaodegauss": "gauss",
    "jordan": "jordan", "gaussjordan": "jordan", "eliminacaodejordan": "jordan",
    "lu": "lu", "fatoracaolu": "lu", "decomposicaolu": "lu",
}


def _normalizar(texto):
    """'Gauss-Jordan' -> 'gaussjordan'; 'Fatoração LU' -> 'fatoracaolu'."""
    decomposto = unicodedata.normalize("NFD", texto.lower())
    sem_acento = "".join(c for c in decomposto if unicodedata.category(c) != "Mn")
    return "".join(c for c in sem_acento if c.isalnum())


def sistemaEquacaoLinear(A, b, metodo="gauss", passos=None):
    """Resolve A x = b pelo método direto escolhido e devolve a lista x.

    Parâmetros
    ----------
    A, b    : sistema (A n x n, b com n termos)
    metodo  : "gauss" (padrão), "jordan" ou "lu"  (também aceita "Gauss-Jordan",
              "Fatoração LU" etc.)
    passos  : lista opcional que recebe o passo a passo (ver cada método)

    Exemplo
    -------
    sistemaEquacaoLinear([[2, 1], [1, 3]], [5, 10], metodo="lu")  ->  [1.0, 3.0]
    """
    # PASSO 1 - Descobrir qual método o usuário pediu (ignorando maiúsculas,
    # acentos e hífens) e recusar nomes desconhecidos.
    chave = _APELIDOS.get(_normalizar(str(metodo)))
    if chave is None:
        raise ValueError(f"Método '{metodo}' desconhecido. Opções: gauss, jordan, lu.")

    # PASSO 2 - Executar o método escolhido (a resolução acontece dentro dele).
    funcao = METODOS[chave][1]
    return funcao(A, b, passos)