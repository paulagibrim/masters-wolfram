# Cellular Automaton

## Sobre o Projeto

Este projeto implementa um **autômato celular unidimensional (ACE)** utilizando Python e as bibliotecas NumPy, <!-- @TODO: acrescentar. -->

A classe `CellularAutomaton` define um autômato celular unidimensional, e permite simular a evolução de um autômato celular baseado em regras definidas pelo usuário, para uma vizinhança padrão de tamanho 1, baseado nas **Regras de Wolfram**, para autômatos celulares unidimensionais. A implementação inclui funcionalidades para:
- Configuração inicial da grade (randomizada ou com uma célula central ativa).
- Evolução temporal do autômato.
- Suporte para composição de duas regras.
- Futuro suporte para composição unilateral de regras (modo ``zip``).
- Personalização do estado inicial.

---

## Estrutura do Código

### **`CellularAutomaton`**

#### **Construtor**
```python
def __init__(self, size, steps, rule, rule2=None, begin_type='random', zip_mode=False)
```
**Parâmetros:**
- `size` (int): Número de células na grade.
- `steps` (int): Número de passos (temporal) a serem simulados.
- `rule` (function): Mapeia o estado atual de uma célula e seus vizinhos para o próximo estado.
- `rule2` (function, opcional): Segunda regra para alternância (usada no modo zip). Padrão: `None`.
- `begin_type` (str, opcional): Define o estado inicial ('random' ou 'center'). Padrão: `random`.
- `zip_mode` (bool, opcional): Alterna entre duas regras a cada passo, caso ativado. Padrão: `False`.


**Métodos:**
- ```set_initial_state(initial_state)```
    Define um estado inicial personalizado.
    *Parâmetros:*
    `initial_state` (list ou numpy array): Lista booleana representando o estado inicial da grade.
    *Validações:*
O estado inicial deve ter o mesmo tamanho que o número de células (size).

- ```evolve()```
    Simula a evolução temporal do autômato por steps passos.
    *Lógica:*
    Aplica rule para calcular o próximo estado.
    Se rule2 for diferente de None, faz a composição de rule e rule2.
