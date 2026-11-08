# Problemas de Cálculo Numérico

**Projeto Final, Unidade 2** · Atividade complementar 2026.2 · UNIVASF
Disciplina de Cálculo Numérico, Prof. Jorge Cavalcanti

**Equipe:** Arthur Lincoln, Raioni Felix e Hiago Lima
**Apresentação:** 17/11

---

## Problemas sorteados

| Problema | Tópico | Assunto | Método | Programa |
|:--:|---|---|---|---|
| 1.2 | Sistemas lineares, métodos diretos | Produção de componentes elétricos | Métodos diretos | `Código/Problema 1.2/` |
| 2.2 | Sistemas lineares, métodos iterativos | Forças nas barras de uma treliça | Gauss-Seidel | `Código/Problema 2.2/gauss_seidel.py` |
| 3.1 | Interpolação e mínimos quadrados | Lei de Moore (log10 do nº de transistores) | Mínimos quadrados | `Código/Problema 3.1/` |
| 4.1 | Integração numérica | Área da seção reta de um rio | Trapézio e Simpson repetidos | `Código/Problema 4.1/` |

O relatório explicativo é um só para a equipe e traz os quatro problemas, o código e o que cada membro fez.

## Como executar

**Problema 1.2 (Componetes Elétricos, Métodos Diretos)**
```bash
cd "Código/Problema 1.2"
python main.py                        # programa com menu
python Problema 1.2/teste_problema_1-2.py    # resolve o problema 1.2 pelos 3 métodos e compara o tempo
python -m unittest discover -s tests  # testes unitários
```
 
O menu resolve os três problemas do Tópico 1 do enunciado (produção de transistores, resistores e chips, componentes elétricos e minas de areia e cascalho) pelo método de Gauss, pelo de Gauss-Jordan, pela Fatoração LU ou pelos três ao mesmo tempo, comparando os resultados. Também aceita um novo problema de consumo ou qualquer sistema linear digitado, e depois de cada cálculo o programa pergunta se o usuário quer resolver outro ou voltar ao menu principal, de onde pode sair. O teste do problema 1.2 modela o sistema, resolve pelos três métodos mostrando o passo a passo de cada um, confere as soluções por substituição e compara o tempo de execução dos métodos. Cada método está em um arquivo próprio (`metodo_gauss.py`, `metodo_jordan.py` e `metodo_lu.py`, dentro de `topico1_sistemas_diretos/`), e a função `sistemaEquacaoLinear` escolhe qual deles usar.
 
```python
from .sistemaEquacaoLinear import sistemaEquacaoLinear
 
A = [[15, 17, 19], [0.3, 0.4, 0.55], [1, 1.2, 1.5]]   # linhas: metal, plástico e borracha (g por componente)
b = [3890, 95, 282]                                   # disponível por dia, em g (3,89 kg, 0,095 kg e 0,282 kg)
x = sistemaEquacaoLinear(A, b, metodo="lu")           # "gauss", "jordan" ou "lu"
# x = [90, 60, 80] componentes por dia
```

Precisa de Python 3. O Gauss-Seidel também usa o `numpy`:

```bash
pip install numpy
```

**Problema 2.2 (treliça, Gauss-Seidel)**

```bash
cd "Código/Problema 2.2"
python gauss_seidel.py          # programa com menu
python teste_gauss_seidel.py    # testes
```

O menu resolve a treliça do enunciado (as cargas e os ângulos podem ser trocados) ou qualquer outro sistema linear digitado. Depois de cada cálculo o programa pergunta se o usuário quer fazer outro ou sair.

**Problema 3.1 (Lei de Moore, Mínimos Quadrados)**

```bash
cd "Código/Problema 3.1"
python executar_problema_3_1.py     # programa interativo com menu
python teste_problema_3_1.py        # testes unitários analíticos
python minimos_quadrados_scipy.py   # versão otimizada com SciPy e benchmark
```

O programa resolve o problema oficial da Lei de Moore ou aceita novos dados personalizados para ajuste de curvas. O cálculo analítico detalha todo o Sistema Normal do MMQ, e a versão em SciPy traz os cálculos otimizados com matriz de covariância dos parâmetros.

**Problema 4.1 (rio, Simpson 1/3 repetido)**

```bash
cd "Código/Problema 4.1"
python teste_simpson.py         # testes
```

```python
from simpson import simpson_repetido

profundidades = [0, 1.8, 2, 4, 4, 6, 4, 3.6, 3.4, 2.8, 0]
area = simpson_repetido(profundidades, 2)   # 66.4 m²
```
