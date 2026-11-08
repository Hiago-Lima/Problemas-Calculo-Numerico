"""
Regra dos Trapézios repetida (4.1)

area = trapezio_repetido(y, h)

onde y é a lista dos valores f(x0), f(x1), ..., f(xN)
em pontos igualmente espaçados e h é a distância
entre dois pontos vizinhos

  
A ideia é trocar f(x), em cada subintervalo [xi, xi+1], pela reta que passa
por (xi, yi) e (xi+1, yi+1). A área sob essa reta é a de um trapézio de
altura h e bases yi e yi+1:

      Ai = h/2 * (yi + yi+1)

  Somando os N trapézios, cada ponto interno aparece em dois deles (como base
  direita de um e base esquerda do seguinte) e por isso pesa 2; só y0 e yN
  aparecem uma vez:

      I = h/2 * [y0 + 2(y1 + y2 + ... + y(n-1)) + yn]

"""

import math


def trapezio_repetido(y, h):
    """
    Integral de f entre x0 e xN pela regra dos trapézios repetida

    I = h/2 * [y0 + 2(y1 + y2 + ... + y(n-1)) + yn]
    """
    y = [float(v) for v in y]
    h = float(h)
    n = (len(y) - 1)

    if n < 1:
        raise ValueError("São necessários pelo menos 2 pontos (1 intervalo).")

    if not math.isfinite(h) or h <= 0:
        raise ValueError("O passo h deve ser um número positivo.")
    if not all(math.isfinite(v) for v in y):
        raise ValueError("Todos os valores de y devem ser números finitos.")

    internos = sum(y[1:-1])  # y1, y2, ..., y(n-1): peso 2

    # O calculo em si:
    trapezio = h / 2 * (y[0] + (2 * internos) + y[-1])

    return trapezio