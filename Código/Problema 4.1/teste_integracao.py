"""Testes do integracao.py. Rodar com "python teste_integracao.py" """

import math

from integracao import trapezio_repetido
from simpson import simpson_repetido


def teste_rio_problema_4_1():
    # profundidades da figura de x = 0 a x = 20m, h = 2m
    y = [0, 1.8, 2, 4, 4, 6, 4, 3.6, 3.4, 2.8, 0]
    assert math.isclose(trapezio_repetido(y, 2), 63.2, rel_tol=1e-12)


def teste_exato_para_retas():
    # trapézio eh exato para grau 1: integral de 2x + 1 em [0, 2] vale 6
    assert math.isclose(trapezio_repetido([1, 3, 5], 1), 6.0)
    # e com um unico intervalo tambem (regra dos trapézios simples)
    assert math.isclose(trapezio_repetido([1, 5], 2), 6.0)


def teste_erro_da_parabola():
    # x² em [0, 1] vale 1/3, mas com n = 2 o trapézio dá 0,375
    r = trapezio_repetido([0, 0.25, 1], 0.5)
    assert math.isclose(r, 0.375)
    # erro previsto pela teoria: (b - a)/12 * h² * f'' = 1/12 * 0,25 * 2 = 1/24
    assert math.isclose(r - 1/3, 1/24)


def teste_seno():
    # integral de sen(x) em [0, π] vale 2; com n = 4 o erro eh de ~0,104
    n = 4
    h = math.pi / n
    y = [math.sin(i * h) for i in range(n + 1)]
    r = trapezio_repetido(y, h)
    assert abs(r - 2) < 0.11, r

    # dobrando n o erro cai cerca de 4x (ordem h²)
    n2 = 8
    h2 = math.pi / n2
    r2 = trapezio_repetido([math.sin(i * h2) for i in range(n2 + 1)], h2)
    assert abs(r2 - 2) < abs(r - 2) / 3.5


def teste_simpson_mais_preciso_que_trapezio():
    # mesmos 5 pontos de sen(x): Simpson (erro ~0,0046) vence o trapézio (~0,104)
    n = 4
    h = math.pi / n
    y = [math.sin(i * h) for i in range(n + 1)]
    assert abs(simpson_repetido(y, h) - 2) < abs(trapezio_repetido(y, h) - 2) / 10


def teste_aceita_numero_impar_de_intervalos():
    # diferente do Simpson, não exige n par: integral de x em [0, 3] vale 4,5
    assert math.isclose(trapezio_repetido([0, 1, 2, 3], 1), 4.5)


def teste_aceita_inteiros_e_tuplas():
    assert math.isclose(trapezio_repetido((1, 1, 1), 2), 4.0)


def teste_entradas_invalidas():
    casos = [
        ([1], 1),                  # 1 ponto (0 intervalos)
        ([], 1),                   # vazio
        ([0, 1, 2], 0),            # h zero
        ([0, 1, 2], -1),           # h negativo
        ([0, float("nan"), 2], 1), # valor invalido
        ([0, float("inf"), 2], 1), # valor invalido
        ([0, 1, 2], float("nan")), # valor invalido
    ]
    for y, h in casos:
        try:
            trapezio_repetido(y, h)
        except ValueError:
            continue
        raise AssertionError(f"deveria recusar y={y}, h={h}")


if __name__ == "__main__":
    for nome, fn in list(globals().items()):
        if nome.startswith("teste_"):
            fn()
            print("ok  ", nome)