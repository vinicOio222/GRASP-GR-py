"""Experiment runner for GRASP + Bin Packing heuristics.

Usage:
    python -m experiments.runner <instance_file> [runs] [iterations] [alpha]

Defaults: runs=3, iterations=1000, alpha=0.25
"""

import sys
import time
import random
import os
from copy import deepcopy

from file_io import read_instance, write_solution
from grasp.grasp import GRASP
from metrics import compute_stats

from heuristics.next_fit import NextFit
from heuristics.first_fit import FirstFit
from heuristics.last_fit import LastFit
from heuristics.best_fit import BestFit
from heuristics.worst_fit import WorstFit

# ---------------------------------------------------------------------------
# Heuristic registry: (name, heuristic_instance, sort_order)
# sort_order: 'D' = decreasing, 'I' = increasing, None = no fixed sort
# ---------------------------------------------------------------------------
HEURISTICS = [
    # Basic
    ("NF",  NextFit(),  None),
    ("FF",  FirstFit(), None),
    ("LF",  LastFit(),  None),
    ("BF",  BestFit(),  None),
    ("WF",  WorstFit(), None),
    # Decreasing
    ("NFD", NextFit(),  'D'),
    ("FFD", FirstFit(), 'D'),
    ("LFD", LastFit(),  'D'),
    ("BFD", BestFit(),  'D'),
    ("WFD", WorstFit(), 'D'),
    # Increasing
    ("NFI", NextFit(),  'I'),
    ("FFI", FirstFit(), 'I'),
    ("LFI", LastFit(),  'I'),
    ("BFI", BestFit(),  'I'),
    ("WFI", WorstFit(), 'I'),
]


def run_experiment(
    instance_path: str, runs: int = 3, iterations: int = 1000,
    alpha: float = 0.25, seed: int | None = None
):
    """Run all heuristics on a single instance and print a statistics table.

    Args:
        instance_path: Path to the instance file.
        runs: Number of independent GRASP runs per heuristic.
        iterations: GRASP iterations per run.
        alpha: RCL alpha parameter.
        seed: Optional random seed for reproducibility.
    """
    if seed is not None:
        random.seed(seed)

    _, capacity, items = read_instance(instance_path)
    instance_name = os.path.basename(instance_path)

    print(f"\n{'='*70}")
    print(f"  Instance : {instance_name}")
    print(f"  Items    : {len(items)}  |  Capacity: {capacity}")
    print(f"  Runs     : {runs}  |  Iterations: {iterations}  |  Alpha: {alpha}")
    print(f"{'='*70}")
    header = f"{'Heuristic':<8} {'Initial':>7} {'Best':>6} {'Worst':>6} {'Avg':>7} {'Loss%':>7} {'Time(s)':>9}"
    print(header)
    print("-" * 70)

    os.makedirs("results", exist_ok=True)
    overall_best_cost = float("inf")
    overall_best_solution = None
    overall_best_name = ""

    for name, heuristic, sort_order in HEURISTICS:
        costs = []
        initial_cost = None
        start = time.perf_counter()

        for run_idx in range(runs):
            grasp = GRASP(alpha=alpha, iterations=iterations,
                          heuristic=heuristic, sort_order=sort_order)
            solution = grasp.solve(items, capacity)
            cost = len(solution)
            costs.append(cost)

            if run_idx == 0:
                initial_cost = cost

        elapsed = time.perf_counter() - start
        stats = compute_stats(costs, initial_cost, elapsed)

        print(f"{name:<8} {stats['initial']:>7} {stats['best']:>6} {stats['worst']:>6} "
              f"{stats['average']:>7.2f} {stats['loss_pct']:>6.2f}% {stats['time']:>8.3f}s")

        # Save best solution per heuristic
        best_run_solution = None
        best_run_cost = float("inf")
        random.seed(seed)  # reset seed for reproducible best-solution extraction
        for _ in range(runs):
            grasp = GRASP(alpha=alpha, iterations=iterations,
                          heuristic=heuristic, sort_order=sort_order)
            sol = grasp.solve(items, capacity)
            if len(sol) < best_run_cost:
                best_run_cost = len(sol)
                best_run_solution = deepcopy(sol)

        out_file = f"results/{instance_name}_{name}.txt"
        write_solution(best_run_solution, out_file, verbose=False)

        if best_run_cost < overall_best_cost:
            overall_best_cost = best_run_cost
            overall_best_solution = best_run_solution
            overall_best_name = name

    print("-" * 70)
    print(f"  Overall best: {overall_best_name} with {overall_best_cost} bins")
    best_out = f"results/{instance_name}_BEST.txt"
    write_solution(overall_best_solution, best_out, verbose=True)
    print(f"  Best solution saved to: {best_out}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "BP-0.txt"
    runs = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    iters = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    alpha = float(sys.argv[4]) if len(sys.argv) > 4 else 0.25
    run_experiment(path, runs=runs, iterations=iters, alpha=alpha, seed=42)
