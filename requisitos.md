# Requisitos do Projeto - GRASP para Bin Packing Problem (BPP)

## Objetivo

Implementar a meta-heurística **GRASP (Greedy Randomized Adaptive Search Procedure)** para resolver o problema de empacotamento de bins (Bin Packing Problem - BPP).

O objetivo é minimizar o número de bins utilizados respeitando a capacidade máxima de cada bin.

---

# Problema

## Entrada

Dado:

* n objetos
* capacidade fixa C para cada bin
* peso de cada objeto

Objetivo:

* empacotar todos os objetos
* cada objeto deve aparecer exatamente uma vez
* nenhum bin pode exceder sua capacidade
* minimizar o número total de bins utilizados

---

# Formato das Instâncias

## Arquivo de Entrada

Formato obrigatório:

```text
n
C
peso_1
peso_2
...
peso_n
```

Exemplo:

```text
11
10
9
1
8
2
7
3
6
3
5
4
2
```

Onde:

* n = quantidade de itens
* C = capacidade do bin
* demais linhas = peso dos itens

---

# Meta-Heurística Obrigatória

Equipe 3:

```text
GRASP (GR)
```

A implementação deve utilizar:

## Fase 1 - Construção

Construção gulosa randomizada.

Deve conter:

* lista restrita de candidatos (RCL)
* parâmetro alpha
* escolha aleatória de candidatos da RCL

A construção não deve ser totalmente determinística.

---

## Fase 2 - Busca Local

Após construir uma solução:

* executar busca local
* tentar melhorar a solução
* reduzir a quantidade de bins

Possíveis movimentos:

* mover item
* trocar itens
* eliminar bins
* redistribuir itens

Objetivo da busca local:

```text
diminuir a quantidade de bins
```

---

# Heurísticas Auxiliares Obrigatórias

A implementação deve permitir usar:

## Versões Básicas

### NF

Next Fit

### FF

First Fit

### LF

Last Fit

### BF

Best Fit

### WF

Worst Fit

---

## Versões Decrescentes

Ordenar itens em ordem decrescente antes da inserção.

### NFD

Next Fit Decreasing

### FFD

First Fit Decreasing

### LFD

Last Fit Decreasing

### BFD

Best Fit Decreasing

### WFD

Worst Fit Decreasing

---

## Versões Crescentes

Ordenar itens em ordem crescente antes da inserção.

### NFI

Next Fit Increasing

### FFI

First Fit Increasing

### LFI

Last Fit Increasing

### BFI

Best Fit Increasing

### WFI

Worst Fit Increasing

---

# Requisitos Funcionais

## RF-01

Ler instâncias em arquivo.

---

## RF-02

Permitir escolher a heurística auxiliar.

Exemplos:

```text
GRASP + BF
GRASP + FF
GRASP + WF
```

---

## RF-03

Permitir configurar:

```python
ALPHA
ITERATIONS
```

---

## RF-04

Executar múltiplas iterações do GRASP.

---

## RF-05

Executar busca local após cada construção.

---

## RF-06

Armazenar a melhor solução encontrada.

---

## RF-07

Exibir a distribuição dos itens nos bins.

Exemplo:

```text
Bin 1: [9,1]
Bin 2: [8,2]
Bin 3: [7,3]
Bin 4: [6,4]
Bin 5: [5,3,2]
```

---

## RF-08

Permitir execução em novas instâncias sem alterar código.

O professor explicitamente exige:

```text
O programa deve permitir de forma facilitada
que novos testes possam ser realizados para
outras instâncias.
```

---

# Experimentos Computacionais

## Execuções

Para cada instância:

```text
mínimo de 3 execuções independentes
```

---

## Instâncias Obrigatórias

| Instância | n    | C    |
| --------- | ---- | ---- |
| BP-0      | 11   | 10   |
| BP-1      | 50   | 1000 |
| BP-2      | 100  | 1000 |
| BP-4      | 200  | 1000 |
| BP-6      | 500  | 150  |
| BP-7      | 1000 | 150  |

Além disso:

```text
Outras (livre)
```

Instâncias extras podem ser utilizadas.

---

# Tabela Obrigatória de Resultados

Para cada instância registrar:

| Campo         |
| ------------- |
| Valor Inicial |
| Pior (Máx)    |
| Média         |
| Melhor (Min)  |
| % Perda       |
| Tempo (s)     |

---

## Valor Inicial

Resultado da heurística auxiliar antes da busca local.

Exemplo:

```text
BFD inicial
```

---

## Pior

Maior número de bins encontrado.

```python
max(resultados)
```

---

## Média

```python
sum(resultados) / len(resultados)
```

---

## Melhor

Menor número de bins encontrado.

```python
min(resultados)
```

---

## Percentual de Perda

```python
((melhor - ótimo) / ótimo) * 100
```

Exemplo:

```text
Ótimo = 5
Melhor = 5

Perda = 0%
```

---

## Tempo

Tempo total de execução.

Medido em segundos.

---

# Critérios de Avaliação

Uma solução é válida apenas se:

* todos os itens forem empacotados
* nenhum item for perdido
* nenhum item for duplicado
* nenhum bin ultrapassar a capacidade
* o número de bins for minimizado

---

# Entregáveis

## Código-fonte

Implementação completa do GRASP.

## Relatório PDF

Contendo:

* descrição da solução
* estratégia de construção
* estratégia de busca local
* experimentos computacionais
* tabela de resultados

## Apresentação

Seminário da disciplina.

## Melhor Solução

A distribuição dos itens nos bins da melhor execução deve ser apresentada.
