"""Testes do minimos_quadrados.py.

Execução:
    python teste_problema_3_1.py
"""

import math
from minimos_quadrados import (ajustar_lei_de_moore, ajustar_reta,
                                prever_transistores)


def teste_problema_3_1_lei_de_moore():
    """Valida o ajuste com os dados oficiais do enunciado do Problema 3.1."""
    anos = [1971, 1972, 1974, 1978, 1982, 1986, 1989, 1993, 1997, 1999, 2000]
    transistores = [
        2250, 3300, 6000, 29000, 134000,
        275000, 1200000, 3100000, 7500000, 9500000, 42000000
    ]

    res, y_log = ajustar_lei_de_moore(anos, transistores)

    # Coeficientes esperados
    assert math.isclose(res.a0, -266.953401, rel_tol=1e-5), f"a0 incorreto: {res.a0}"
    assert math.isclose(res.a1, 0.137183, rel_tol=1e-4), f"a1 incorreto: {res.a1}"

    # Qualidade do ajuste R² próximo de 99%
    assert res.r2 > 0.989, f"R² inesperadamente baixo: {res.r2}"

    # Previsão 2010 (~6.08 x 10^8)
    log_2010, n_2010 = prever_transistores(2010, res.a0, res.a1)
    assert math.isclose(log_2010, 8.784224, rel_tol=1e-4)
    assert 6.0e8 < n_2010 < 6.2e8, f"Previsão 2010 fora da faixa: {n_2010}"

    # Previsão 2020 (~1.43 x 10^10)
    log_2020, n_2020 = prever_transistores(2020, res.a0, res.a1)
    assert math.isclose(log_2020, 10.156053, rel_tol=1e-4)
    assert 1.4e10 < n_2020 < 1.5e10, f"Previsão 2020 fora da faixa: {n_2020}"


def teste_reta_exata():
    """Valida que uma reta exata y = 3x - 5 possui R² = 1.0 e erro residual zero."""
    x = [0.0, 1.0, 2.0, 3.0, 4.0]
    y = [3 * xi - 5 for xi in x]

    res = ajustar_reta(x, y)
    assert math.isclose(res.a0, -5.0, abs_tol=1e-9)
    assert math.isclose(res.a1, 3.0, abs_tol=1e-9)
    assert math.isclose(res.r2, 1.0, abs_tol=1e-9)
    assert math.isclose(res.sq_res, 0.0, abs_tol=1e-9)


def teste_entradas_invalidas():
    """Valida tratamento de erros para entradas inválidas."""
    # Menos de 2 pontos
    try:
        ajustar_reta([1.0], [2.0])
        assert False, "Deveria recusar menos de 2 pontos"
    except ValueError:
        pass

    # Tamanhos incompatíveis
    try:
        ajustar_reta([1.0, 2.0], [2.0])
        assert False, "Deveria recusar tamanhos diferentes"
    except ValueError:
        pass

    # Valores negativos para transistores
    try:
        ajustar_lei_de_moore([1990, 1991], [1000, -5])
        assert False, "Deveria recusar número de transistores negativo"
    except ValueError:
        pass

    # Pontos x idênticos (determinante zero)
    try:
        ajustar_reta([5.0, 5.0, 5.0], [1.0, 2.0, 3.0])
        assert False, "Deveria recusar x sem variância"
    except ValueError:
        pass


if __name__ == "__main__":
    for nome, fn in list(globals().items()):
        if nome.startswith("teste_"):
            fn()
            print("ok  ", nome)
