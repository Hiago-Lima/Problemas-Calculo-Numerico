"""Problema 4.1 - Integração Numérica (Pessoa 3: Interface e Comparação).

NOTA PARA PESSOA 1: Criar 'integracao.py' com a função:
    def trapezio_repetido(y: list, h: float) -> float
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa os métodos das Pessoas 1 e 2
try:
    from integracao import trapezio_repetido
except ImportError:
    trapezio_repetido = None  # Pessoa 1 ainda não finalizou

try:
    from simpson import simpson_repetido
except ImportError:
    simpson_repetido = None  # Pessoa 2 ainda não finalizou

# Dados oficiais do rio (x de 0 a 20m, h = 2m)
RIO_X = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
RIO_Y = [0.0, 1.8, 2.0, 4.0, 4.0, 6.0, 4.0, 3.6, 3.4, 2.8, 0.0]
RIO_H = 2.0


def comparar(y, h):
    """Calcula e compara as áreas pelos métodos de Trapézio e Simpson."""
    n = len(y) - 1
    print(f"\nPontos: {len(y)} | Intervalos (n): {n} | Passo (h): {h} m")
    
    # 1. Trapézio (Pessoa 1)
    area_trap = None
    if trapezio_repetido:
        try:
            area_trap = trapezio_repetido(y, h)
            print(f"Área (Trapézios):  {area_trap:.4f} m² [O(h²)]")
        except Exception as e:
            print(f"Área (Trapézios):  Erro ({e})")
    else:
        print("Área (Trapézios):  PENDENTE (aguardando Pessoa 1 em integracao.py)")

    # 2. Simpson (Pessoa 2)
    area_simp = None
    if simpson_repetido:
        try:
            area_simp = simpson_repetido(y, h)
            print(f"Área (Simpson):    {area_simp:.4f} m² [O(h⁴)]")
        except ValueError as e:
            print(f"Área (Simpson):    Não aplicável ({e})")
    else:
        print("Área (Simpson):    PENDENTE (aguardando Pessoa 2 em simpson.py)")

    # Comparativo
    if area_trap is not None and area_simp is not None:
        diff = abs(area_simp - area_trap)
        relativa = f" ({(diff/area_simp)*100:.2f}%)" if area_simp else ""
        print(f"\nDiferença |Simpson - Trapézio|: {diff:.4f} m²{relativa}")
        print("Conclusão: Simpson é mais preciso para leitos curvos por usar parábolas.")


def coletar_novos_dados():
    h = float(input("\nPasso h constante: ").replace(",", "."))
    n_pts = int(input("Quantidade de pontos: "))
    print(f"Digite os {n_pts} valores de y:")
    y = [float(input(f"  y[{i}]: ").replace(",", ".")) for i in range(n_pts)]
    return y, h


def main():
    while True:
        print("\n=== PROBLEMA 4.1: SEÇÃO RETA DO RIO ===")
        print("1 - Dados oficiais do rio (h = 2m)")
        print("2 - Inserir novos dados")
        print("0 - Sair")
        
        op = input("Opção: ").strip()
        if op == "0":
            print("Encerrado.")
            break
        elif op == "1":
            comparar(RIO_Y, RIO_H)
        elif op == "2":
            try:
                y, h = coletar_novos_dados()
                comparar(y, h)
            except Exception as e:
                print(f"Entrada inválida: {e}")
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
