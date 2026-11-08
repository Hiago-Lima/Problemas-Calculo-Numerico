"""Versão otimizada do Problema 3.1 utilizando SciPy e NumPy.

Esta abordagem utiliza:
1. `scipy.optimize.curve_fit` para ajuste robusto com estimativa de incertezas (matriz de covariância).
2. Vetorização completa com NumPy para máxima performance.
3. Ajuste no espaço linearizado (log10) e comparativo com ajuste não-linear direto.
"""

import time
from typing import Dict, Tuple
import numpy as np
from scipy.optimize import curve_fit


def modelo_linear(x: np.ndarray, a0: float, a1: float) -> np.ndarray:
    """Modelo linear: y = a0 + a1 * x."""
    return a0 + a1 * x


def modelo_exponencial_direto(x: np.ndarray, c: float, k: float) -> np.ndarray:
    """Modelo exponencial direto: N = C * 10^(k * x)."""
    return c * (10.0 ** (k * x))


def ajustar_lei_de_moore_scipy(
    anos: np.ndarray,
    transistores: np.ndarray
) -> Dict[str, object]:
    """Realiza o ajuste linearizado da Lei de Moore utilizando scipy.optimize.curve_fit.

    Retorna um dicionário com os parâmetros ajustados, desvios-padrão (1-sigma),
    coeficiente R² e funções de predição vetorizadas.
    """
    x = np.asarray(anos, dtype=np.float64)
    n_trans = np.asarray(transistores, dtype=np.float64)

    if np.any(n_trans <= 0):
        raise ValueError("Todos os valores de transistores devem ser estritamente positivos.")

    # 1. Transformação logarítmica
    y_log = np.log10(n_trans)

    # 2. Ajuste por Mínimos Quadrados com scipy.optimize.curve_fit
    popt, pcov = curve_fit(modelo_linear, x, y_log)
    a0, a1 = popt
    desvio_a0, desvio_a1 = np.sqrt(np.diag(pcov))

    # 3. Métricas de resíduo e R²
    y_pred = modelo_linear(x, a0, a1)
    sq_res = np.sum((y_log - y_pred) ** 2)
    sq_tot = np.sum((y_log - np.mean(y_log)) ** 2)
    r2 = 1.0 - (sq_res / sq_tot)

    return {
        "a0": a0,
        "a1": a1,
        "desvio_a0": desvio_a0,
        "desvio_a1": desvio_a1,
        "r2": r2,
        "sq_res": sq_res,
        "matriz_covariancia": pcov,
        "popt": popt,
    }


def prever_scipy(anos_consulta: np.ndarray, a0: float, a1: float) -> Tuple[np.ndarray, np.ndarray]:
    """Gera predições vetorizadas para um array de anos usando NumPy."""
    anos_arr = np.asarray(anos_consulta, dtype=np.float64)
    log_pred = modelo_linear(anos_arr, a0, a1)
    n_pred = 10.0 ** log_pred
    return log_pred, n_pred


def benchmark_comparativo(repeticoes: int = 1000):
    """Compara o tempo de execução entre curve_fit e np.polyfit."""
    anos = np.array([1971, 1972, 1974, 1978, 1982, 1986, 1989, 1993, 1997, 1999, 2000], dtype=float)
    trans = np.array([2250, 3300, 6000, 29000, 134000, 275000, 1200000, 3100000, 7500000, 9500000, 42000000], dtype=float)
    y_log = np.log10(trans)

    t0 = time.perf_counter()
    for _ in range(repeticoes):
        _ = curve_fit(modelo_linear, anos, y_log)
    tempo_scipy = time.perf_counter() - t0

    t0 = time.perf_counter()
    for _ in range(repeticoes):
        _ = np.polyfit(anos, y_log, 1)
    tempo_numpy = time.perf_counter() - t0

    return tempo_scipy, tempo_numpy


def main():
    print("=" * 72)
    print("  PROBLEMA 3.1: AJUSTE OTIMIZADO COM SCIPY (CURVE_FIT)")
    print("=" * 72)

    anos = np.array([1971, 1972, 1974, 1978, 1982, 1986, 1989, 1993, 1997, 1999, 2000])
    transistores = np.array([
        2250, 3300, 6000, 29000, 134000,
        275000, 1200000, 3100000, 7500000, 9500000, 42000000
    ])

    res = ajustar_lei_de_moore_scipy(anos, transistores)

    print("\n--- RESULTADOS OBTIDOS (SCIPY) ---")
    print(f"Intercepto (a0):         {res['a0']:.8f} ± {res['desvio_a0']:.8f}")
    print(f"Inclinação (a1):         {res['a1']:.8f} ± {res['desvio_a1']:.8f}")
    print(f"Coeficiente R²:          {res['r2'] * 100:.2f}% (R² = {res['r2']:.6f})")
    print(f"Soma resíduos quadr.:    {res['sq_res']:.6f}")

    # Previsões vetorizadas para 2010 e 2020
    anos_prev = np.array([2010, 2020])
    log_prev, n_prev = prever_scipy(anos_prev, res['a0'], res['a1'])

    print("\n--- PREVISÕES DO ENUNCIADO ---")
    for ano, lp, np_val in zip(anos_prev, log_prev, n_prev):
        print(f"Ano {ano}:")
        print(f"  -> log10(N) = {lp:.6f}")
        print(f"  -> N estimado = {np_val:,.0f} ({np_val:.2e} transistores)")

    # Benchmark rápido
    print("\n--- BENCHMARK (1.000 iterações) ---")
    t_scipy, t_numpy = benchmark_comparativo(1000)
    print(f"Tempo total scipy.optimize.curve_fit: {t_scipy * 1000:.2f} ms")
    print(f"Tempo total numpy.polyfit:            {t_numpy * 1000:.2f} ms")


if __name__ == "__main__":
    main()
