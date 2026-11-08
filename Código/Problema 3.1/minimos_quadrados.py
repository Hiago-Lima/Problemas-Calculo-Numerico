"""Método dos Mínimos Quadrados (MMQ) para regressão linear e exponencial.

Problema 3.1 - Lei de Moore:
Ajuste linear sobre os dados transformados: y = log10(N) = a0 + a1 * a,
de modo que o número de transistores estimado seja dado por:
N(a) = 10^(a0 + a1 * a).
"""

import math
from dataclasses import dataclass
from typing import List, Sequence, Tuple


@dataclass
class ResultadoAjuste:
    """Estrutura com os resultados analíticos do ajuste por Mínimos Quadrados."""
    a0: float               # Intercepto linear
    a1: float               # Inclinação da reta
    r2: float               # Coeficiente de determinação R²
    sq_res: float           # Soma dos quadrados dos resíduos (erro quadrático)
    sq_tot: float           # Soma total dos quadrados
    n: int                  # Quantidade de pontos
    sum_x: float            # Somatório de x
    sum_y: float            # Somatório de y
    sum_x2: float           # Somatório de x²
    sum_xy: float           # Somatório de x * y

    @property
    def equacao_linear(self) -> str:
        sinal = "+" if self.a1 >= 0 else "-"
        return f"log10(N) = {self.a0:.6f} {sinal} {abs(self.a1):.6f} * a"

    @property
    def equacao_exponencial(self) -> str:
        sinal = "+" if self.a1 >= 0 else "-"
        return f"N(a) = 10^({self.a0:.6f} {sinal} {abs(self.a1):.6f} * a)"


def ajustar_reta(x: Sequence[float], y: Sequence[float]) -> ResultadoAjuste:
    """Ajusta y = a0 + a1 * x pelo Método dos Mínimos Quadrados.

    Resolve analiticamente o Sistema de Equações Normais 2x2:
        [ n       sum(x)   ] * [ a0 ] = [ sum(y)   ]
        [ sum(x)  sum(x^2) ]   [ a1 ]   [ sum(x*y) ]

    Parâmetros
    ----------
    x : Sequência de coordenadas independentes
    y : Sequência de coordenadas dependentes

    Retorna
    -------
    ResultadoAjuste contendo a0, a1, somatórios e métricas de qualidade (R², resíduos).
    """
    if len(x) != len(y):
        raise ValueError(f"As listas x e y devem ter o mesmo tamanho. Recebido: len(x)={len(x)}, len(y)={len(y)}")

    n = len(x)
    if n < 2:
        raise ValueError("São necessários pelo menos 2 pontos para o ajuste por mínimos quadrados.")

    x_float = [float(val) for val in x]
    y_float = [float(val) for val in y]

    if not all(math.isfinite(v) for v in x_float):
        raise ValueError("Todos os valores de x devem ser números reais finitos.")
    if not all(math.isfinite(v) for v in y_float):
        raise ValueError("Todos os valores de y devem ser números reais finitos.")

    sum_x = sum(x_float)
    sum_y = sum(y_float)
    sum_x2 = sum(xi ** 2 for xi in x_float)
    sum_xy = sum(xi * yi for xi, yi in zip(x_float, y_float))

    det = (n * sum_x2) - (sum_x ** 2)
    if abs(det) < 1e-12:
        raise ValueError("Determinante próximo de zero. Os valores de x não possuem variação suficiente.")

    a1 = (n * sum_xy - sum_x * sum_y) / det
    a0 = (sum_y - a1 * sum_x) / n

    y_medio = sum_y / n
    sq_tot = sum((yi - y_medio) ** 2 for yi in y_float)
    sq_res = sum((yi - (a0 + a1 * xi)) ** 2 for xi, yi in zip(x_float, y_float))

    r2 = 1.0 - (sq_res / sq_tot) if sq_tot != 0 else 1.0

    return ResultadoAjuste(
        a0=a0,
        a1=a1,
        r2=r2,
        sq_res=sq_res,
        sq_tot=sq_tot,
        n=n,
        sum_x=sum_x,
        sum_y=sum_y,
        sum_x2=sum_x2,
        sum_xy=sum_xy,
    )


def ajustar_lei_de_moore(anos: Sequence[float], transistores: Sequence[float]) -> Tuple[ResultadoAjuste, List[float]]:
    """Aplica a transformação y = log10(N) e realiza o ajuste por mínimos quadrados.

    Parâmetros
    ----------
    anos : Sequência de anos de lançamento
    transistores : Sequência de quantidade de transistores (valores estritamente positivos)

    Retorna
    -------
    (resultado, y_log): Objeto ResultadoAjuste e lista com os valores de log10(N).
    """
    if len(anos) != len(transistores):
        raise ValueError("A lista de anos e a de transistores devem ter a mesma quantidade de elementos.")

    for i, n in enumerate(transistores):
        if n <= 0 or not math.isfinite(n):
            raise ValueError(f"O número de transistores deve ser positivo e finito. Posição {i} contém {n}.")

    y_log = [math.log10(float(n)) for n in transistores]
    resultado = ajustar_reta(anos, y_log)
    return resultado, y_log


def prever_transistores(ano: float, a0: float, a1: float) -> Tuple[float, float]:
    """Estima o número de transistores para um dado ano.

    Retorna
    -------
    (log10_estimado, n_estimado)
    """
    log10_estimado = a0 + a1 * float(ano)
    n_estimado = 10.0 ** log10_estimado
    return log10_estimado, n_estimado
