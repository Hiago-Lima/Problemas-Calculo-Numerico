"""Programa interativo do Problema 3.1 - Lei de Moore (Mínimos Quadrados).

Permite resolver o problema oficial com os dados da Intel ou inserir
novos dados para problemas semelhantes de mesma natureza.
"""

from minimos_quadrados import (ajustar_lei_de_moore, prever_transistores)

DADOS_PADRAO_CHIPS = [
    "4004", "8008", "8080", "8086", "80286",
    "80386", "80486", "Pentium", "Pentium II", "Pentium III", "Pentium 4"
]
DADOS_PADRAO_ANOS = [1971, 1972, 1974, 1978, 1982, 1986, 1989, 1993, 1997, 1999, 2000]
DADOS_PADRAO_TRANSISTORES = [
    2250, 3300, 6000, 29000, 134000,
    275000, 1200000, 3100000, 7500000, 9500000, 42000000
]


def exibir_tabela(rotulos, anos, transistores, y_log):
    print("\n" + "=" * 72)
    print(f"{'Item/Chip':<16} | {'Ano (a)':<8} | {'N (Transistores)':<18} | {'y = log10(N)':<15}")
    print("-" * 72)
    for rotulo, ano, n, y in zip(rotulos, anos, transistores, y_log):
        print(f"{rotulo:<16} | {ano:<8.0f} | {n:<18,.0f} | {y:<15.6f}")
    print("=" * 72)


def exibir_detalhes_mmq(resultado):
    print("\n--- DETALHAMENTO DO SISTEMA NORMAL (MMQ) ---")
    print(f"Número de pontos (n):     {resultado.n}")
    print(f"Somatório de x:           {resultado.sum_x:,.2f}")
    print(f"Somatório de x²:          {resultado.sum_x2:,.2f}")
    print(f"Somatório de y (log10 N): {resultado.sum_y:,.6f}")
    print(f"Somatório de x * y:       {resultado.sum_xy:,.6f}")
    print("\nSistema Normal 2x2:")
    print(f"  [ {resultado.n:>4}      {resultado.sum_x:>12.1f} ] * [ a0 ] = [ {resultado.sum_y:>14.6f} ]")
    print(f"  [ {resultado.sum_x:>6.1f}  {resultado.sum_x2:>12.1f} ]   [ a1 ]   [ {resultado.sum_xy:>14.6f} ]")

    print("\n--- COEFICIENTES E MODELO OBTIDO ---")
    print(f"Intercepto (a0):         {resultado.a0:.8f}")
    print(f"Inclinação (a1):         {resultado.a1:.8f}")
    print(f"Equação Linearizada:     {resultado.equacao_linear}")
    print(f"Função Exponencial:      {resultado.equacao_exponencial}")
    print(f"Coeficiente R²:          {resultado.r2 * 100:.2f}% (R² = {resultado.r2:.6f})")
    print(f"Soma resíduos quadr.:    {resultado.sq_res:.6f}")


def coletar_novos_dados():
    while True:
        try:
            qtd_txt = input("\nQuantos pontos deseja inserir? ").strip()
            qtd = int(qtd_txt)
            if qtd < 2:
                print("  Digite pelo menos 2 pontos.")
                continue
            rotulos, anos, transistores = [], [], []
            for i in range(qtd):
                rotulo = input(f"Rótulo do ponto {i+1}: ").strip() or f"Ponto {i+1}"
                ano = float(input(f"  Ano/x do ponto {i+1}: ").replace(",", "."))
                n = float(input(f"  Valor N (positivo): ").replace(",", "."))
                if n <= 0:
                    print("  O valor de N deve ser positivo. Tente novamente.")
                    return None
                rotulos.append(rotulo)
                anos.append(ano)
                transistores.append(n)
            return rotulos, anos, transistores
        except ValueError:
            print("  Entrada inválida. Digite valores numéricos válidos.")
            return None


def menu_previsoes(a0, a1, anos_iniciais=None):
    if anos_iniciais:
        print("\n--- PREVISÕES DO ENUNCIADO ---")
        for ano in anos_iniciais:
            log_n, n_est = prever_transistores(ano, a0, a1)
            print(f"Ano {ano}:")
            print(f"  -> log10(N) = {log_n:.6f}")
            print(f"  -> N estimado = {n_est:,.0f} ({n_est:.2e} transistores)")

    while True:
        resp = input("\nDeseja estimar para outro ano? (digite o ano ou 'n' para voltar): ").strip()
        if resp.lower() == 'n' or resp == '':
            break
        try:
            ano_custom = float(resp.replace(",", "."))
            log_n, n_est = prever_transistores(ano_custom, a0, a1)
            print(f"Previsão para o ano {ano_custom:.1f}:")
            print(f"  -> log10(N) = {log_n:.6f}")
            print(f"  -> N estimado = {n_est:,.0f} ({n_est:.2e} transistores)")
        except ValueError:
            print("  Ano inválido.")


def main():
    print("=" * 72)
    print("  TÓPICO 03 - PROBLEMA 3.1: LEI DE MOORE (MÍNIMOS QUADRADOS)")
    print("=" * 72)

    while True:
        print("\nEscolha uma opção:")
        print("1 - Usar dados padrão da questão (Chips Intel / Lei de Moore)")
        print("2 - Inserir novos dados personalizados")
        print("0 - Sair")

        opcao = input("\nOpção: ").strip()

        if opcao == "0":
            print("\nPrograma finalizado.")
            break
        elif opcao == "1":
            rotulos = DADOS_PADRAO_CHIPS
            anos = DADOS_PADRAO_ANOS
            transistores = DADOS_PADRAO_TRANSISTORES
            anos_prev_iniciais = [2010, 2020]
        elif opcao == "2":
            dados = coletar_novos_dados()
            if not dados:
                continue
            rotulos, anos, transistores = dados
            anos_prev_iniciais = None
        else:
            print("Opção inválida.")
            continue

        try:
            resultado, y_log = ajustar_lei_de_moore(anos, transistores)
            exibir_tabela(rotulos, anos, transistores, y_log)
            exibir_detalhes_mmq(resultado)
            menu_previsoes(resultado.a0, resultado.a1, anos_prev_iniciais)
        except Exception as err:
            print(f"Erro durante o cálculo: {err}")


if __name__ == "__main__":
    main()
