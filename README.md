# GRASP-GR-py

Implementation of the GRASP (*Greedy Randomized Adaptive Search Procedure*) metaheuristic applied to the one-dimensional **Bin Packing Problem (BPP)**.

> Course assignment for Complexity Theory — State University of Ceará (UECE)  
> **Team 3 · Metaheuristic: GRASP (GR)**

---

## Objective

Minimize the number of bins required to pack a set of `n` items while respecting a fixed bin capacity `C`.

---

## Implemented Heuristics

Each heuristic is available in three variants:

| Suffix | Item ordering |
|--------|---------------|
| (basic) | No pre-sorting (random RCL) |
| D | Decreasing (largest item first) |
| I | Increasing (smallest item first) |

| Heuristic | Insertion strategy |
|-----------|--------------------|
| **NF** — Next Fit | Insert into the last open bin; open a new one if it does not fit |
| **FF** — First Fit | Insert into the first bin that fits |
| **LF** — Last Fit | Insert into the last bin that fits |
| **BF** — Best Fit | Insert into the bin with the least remaining space that still fits |
| **WF** — Worst Fit | Insert into the bin with the most remaining space |

Combining base × variant yields **15 heuristics** tested per instance: `NF, FF, LF, BF, WF, NFD, FFD, LFD, BFD, WFD, NFI, FFI, LFI, BFI, WFI`.

---

## GRASP

### Construction Phase

- Restricted Candidate List (RCL) controlled by the `alpha` parameter (0 = greedy, 1 = fully random)
- Random item selection from the RCL
- Decoupled from the packing heuristic used

### Local Search Phase

- Sorts bins by lightest load
- Attempts to redistribute **all** items from the least loaded bin into the remaining bins
- Removes the bin if redistribution succeeds without exceeding any bin capacity
- Rolls back partial moves if the bin cannot be fully emptied

---

## Instance File Format

```
firt line ==> n (number of items)
second line ==> C (bin capacity)
next n lines ==> item weights (one per line)
Pi
where:
Pi = weight of item i (1 ≤ i ≤ n)
```

**Example (`BP-0.txt`):**
```
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

---

## How to Run

### Requirements

- Python 3.12+
- No external dependencies

### Default execution

```bash
python main.py
```

Runs the full experiment with all 15 heuristics on every instance inside `instances/` (3 runs, 1000 iterations, alpha=0.25).

### Custom execution

```bash
python -m experiments.runner <instance_file_or_dir> [runs] [iterations] [alpha] [heuristic] [optimum]
```

**Examples:**
```bash
python -m experiments.runner instances
python -m experiments.runner instances 5 2000 0.3
python -m experiments.runner BP-0.txt
python -m experiments.runner instances/_BP-1_n50C1000.txt 3 1000 0.25 BF
python -m experiments.runner instances/_BP-1_n50C1000.txt 3 1000 0.25 BFD 19
```

- `heuristic` (optional): runs only one heuristic code (`NF`, `FF`, `LF`, `BF`, `WF`, `NFD`, ...)
- `optimum` (optional): known optimum bin count used for `% Perda = ((melhor - otimo) / otimo) * 100`

### Expected output

```
======================================================================
  Instance : BP-0.txt
  Items    : 11  |  Capacity: 10
  Runs     : 3  |  Iterations: 1000  |  Alpha: 0.25
======================================================================
Heuristic Initial   Best  Worst     Avg   Loss%   Time(s)
----------------------------------------------------------------------
FFD            5      5      5    5.00   0.00%    0.057s
...
----------------------------------------------------------------------
  Overall best: FFD with 5 bins
======================================================================
```

Individual results per heuristic are saved under `results/` for each processed instance.

---

## Project Structure

```
GRASP-GR-py/
│
├── main.py                  # Entry point
├── file_io.py               # Instance reading and solution writing
├── metrics.py               # Statistics (best, worst, avg, loss%)
│
├── core/
│   ├── bin.py               # Bin class (capacity, items, remaining)
│   └── solution.py          # Solution class
│
├── heuristics/
│   ├── next_fit.py          # Next Fit
│   ├── first_fit.py         # First Fit
│   ├── last_fit.py          # Last Fit
│   ├── best_fit.py          # Best Fit
│   ├── worst_fit.py         # Worst Fit
│   └── sorted_heuristic.py  # Wrapper for D/I variants
│
├── grasp/
│   ├── constructor.py       # Construction phase (RCL + alpha + sort_order)
│   └── grasp.py             # Main GRASP loop
│
├── experiments/
│   └── runner.py            # Full runner with statistics table
│
└── results/                 # Generated solutions (created automatically)
```

---

## Authors

| Name |
|------|
| Vinícius dos Santos |
| Lucas Monteiro |
| Tiago Magalhães |

---

## License

Distributed under the MIT License. See `LICENSE` for more details.

