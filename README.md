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
