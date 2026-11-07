"""Testes do simpson.py. Rodar com "python teste_simpson.py" """

import math

from simpson import simpson_repetido


def teste_rio_problema_4_1():
    # profundidades da figura de x = 0 a x = 20m, h = 2m
    y = [0, 1.8, 2, 4, 4, 6, 4, 3.6, 3.4, 2.8, 0]
    assert math.isclose(simpson_repetido(y, 2), 66.4, rel_tol=1e-12)
    
def teste_exato_para_cubicas():
    
    #Simpson eh exato até grau 3: integral de x³ em [0, 2] vale 4
    assert math.isclose(simpson_repetido([0, 1, 8], 1), 4.0)
    #e de x² em [0, 1] vale 1/3
    assert math.isclose(simpson_repetido([0, 0.25, 1], 0.5), 1/3)
    
def teste_seno():
    #integral de sen(x) em [0, π] vale 2; com n = 4 o erro eh de ~0,0046
    n = 4
    h = math.pi / n #π/n
    y = [math.sin(i * h) for i in range(n + 1)]
    r = simpson_repetido(y, h)
    assert abs(r - 2) < 5e-3, r
    
    #dobrandpo n o erro cai cerca de 16x (ordem h⁴)
    n2 = 8
    h2 = math.pi / n2
    r2 = simpson_repetido([math.sin(i * h2) for i in range(n2 + 1)], h2)
    assert abs(r2 - 2) < abs(r - 2) / 10
    
def teste_aceita_inteiros_e_tuplas():
    assert math.isclose(simpson_repetido((1, 1, 1), 2), 4.0)

def teste_entradas_invalidas():
    casos = [
        ([0, 1, 2, 3], 1), #3 intervalos
        ([1, 2], 1),       #1 intervalo
        ([], 1),           #vazio
        ([0, 1, 2], 0),    #h zero
        ([0, 1, 2], -1),    #h negativo
        ([0, float("nan"), 2], 1), #valor invalido
        ([0, float("inf"), 2], 1), #valor invalido
        ([0, 1, 2], float("nan")), #valor invalido
    ]
    for y, h in casos:
        try:
            simpson_repetido(y, h)
        except ValueError:
            continue
        raise AssertionError(f"deveria recusar y={y}, h={h}")
    
if __name__ == "__main__":
    for nome, fn in list(globals().items()):
        if nome.startswith("teste_"):
            fn()
            print("ok  ", nome)