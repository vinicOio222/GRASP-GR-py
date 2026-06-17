Segue um `.md` que eu colocaria na raiz do projeto para orientar o Copilot e os integrantes da equipe.

# GRASP for Bin Packing Problem (BPP)

## Project Overview

This project implements the **GRASP (Greedy Randomized Adaptive Search Procedure)** metaheuristic to solve the **Bin Packing Problem (BPP)**.

The objective is to minimize the number of bins used while respecting the fixed capacity of each bin.

The project is part of the Computational Optimization assignment and corresponds to:

* Team: 3
* Metaheuristic: GRASP (GR)

---

## Problem Definition

Given:

* A set of `n` items
* A bin capacity `C`

Find a packing arrangement that minimizes the number of bins used.

### Example

Capacity:

```text
10
```

Items:

```text
9 1 8 2 7 3 6 3 5 4 2
```

Optimal solution:

```text
{9,1}
{8,2}
{7,3}
{6,4}
{5,3,2}
```

Number of bins:

```text
5
```

---

## Input File Format

Each instance file must follow exactly this format:

```text
n
C
item_1
item_2
...
item_n
```

Example:

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

Where:

* `n` = number of items
* `C` = bin capacity
* Remaining lines = item weights

---

## Required Heuristics

The project must support the following packing heuristics:

### Basic Versions

* Next Fit (NF)
* First Fit (FF)
* Last Fit (LF)
* Best Fit (BF)
* Worst Fit (WF)

### Decreasing Versions

Items sorted in descending order before packing.

* NFD
* FFD
* LFD
* BFD
* WFD

### Increasing Versions

Items sorted in ascending order before packing.

* NFI
* FFI
* LFI
* BFI
* WFI

---

## GRASP Requirements

The GRASP implementation must contain:

### Construction Phase

Greedy randomized construction using:

* Restricted Candidate List (RCL)
* Alpha parameter (`0 <= alpha <= 1`)
* Random candidate selection

Construction should be independent of the packing heuristic.

### Local Search Phase

Apply local improvements attempting to:

* Relocate items
* Eliminate bins
* Reduce the total number of bins

Preferred strategy:

* Select the least loaded bin
* Attempt to redistribute all its items
* Remove the bin if successful

---

## Experimental Requirements

For every provided instance:

* Execute at least 3 independent runs
* Record execution statistics
* Save the best solution found

Metrics:

* Initial value
* Worst solution
* Average solution
* Best solution
* Loss percentage
* Execution time

---

## Expected Output

Example:

```text
Bins used: 5

Bin 1: [9, 1]
Bin 2: [8, 2]
Bin 3: [7, 3]
Bin 4: [6, 4]
Bin 5: [5, 3, 2]
```

---

## Suggested Project Structure

```text
grasp_bpp/
│
├── main.py
├── config.py
│
├── models/
│   ├── bin.py
│   └── solution.py
│
├── heuristics/
│   ├── next_fit.py
│   ├── first_fit.py
│   ├── last_fit.py
│   ├── best_fit.py
│   ├── worst_fit.py
│
├── grasp/
│   ├── constructor.py
│   ├── local_search.py
│   └── grasp.py
│
├── file_io.py
│
├── experiments/
│   └── runner.py
│
└── instances/
```

---

## Design Guidelines

### Modularity

Each heuristic must be implemented in a separate module.

Example:

```python
class PackingHeuristic:
    def insert(self, item, bins, capacity):
        pass
```

### Extensibility

New heuristics must be pluggable without modifying the GRASP implementation.

### Reproducibility

Allow fixed random seeds:

```python
random.seed(42)
```

### Performance

Avoid unnecessary deep copies.

Prioritize:

* Efficient bin elimination
* Efficient local search
* Low memory usage

---

## Success Criteria

A valid solution must:

* Never exceed bin capacity
* Pack all items exactly once
* Minimize the number of bins used

The main evaluation metric is:

```text
Number of bins used
```

Lower is better.

---

## Deliverables

* Source code
* Experimental results table
* Best packing arrangement for each instance
* PDF report
* Presentation for seminar day
