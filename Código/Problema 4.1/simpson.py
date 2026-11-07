"""
Regra de Simpson 1/3 repetida (4.1)

area = simpson_repetido(y, h)

onde y eh a lista dos valores f(x0), f(x1), ..., f(xN)
em pontos igualmente espaçados e h eh a distancia
entre dois pontos vizinhos
"""

import math

def simpson_repetido(y, h):
    """
    Integral de f entre x0 e xN pela regra 1/3 de Simpson
    
    I = h/3 * [y0 + 4(y1 + y3 + ... y(n-1)) + 2(y2 + y4 + ... + y(n-2)) + yn]
    """
    y = [float(v) for v in y]
    h = float(h)
    n = (len(y) - 1)
    
    if n < 2:
        raise ValueError("São necessários pelo menos 3 pontos (2 intervalos).")
    
    if n % 2 != 0:
        raise ValueError(f"A regra exige número par de intervalos, há {n} "
                         f"({len(y)} pontos) no momento."
                         )
    
    if not math.isfinite(h) or h <= 0:
        raise ValueError("O passo h deve ser um número positivo.")
    if not all(math.isfinite(v) for v in y):
        raise ValueError("Todos os valores de y devem ser números finitos.")
    
    impares = sum(y[1:-1:2]) #y1, y3, ..., y(n-1): peso 4
    pares = sum(y[2:-1:2]) #y2, y4, ..., y(n-2): peso 2
    
    #O calculo em si:
    simpson = h / 3 * (y[0] + (4 * impares) + (2 * pares) + y[-1])
    
    return simpson