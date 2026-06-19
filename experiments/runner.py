"""Experiment runner for GRASP + Bin Packing heuristics.

Usage:
    python -m experiments.runner <instance_file_or_dir> [runs] [iterations] [alpha] [heuristic] [optimum]

Defaults: runs=3, iterations=1000, alpha=0.25
"""

import sys
import time
import random
import os
from copy import deepcopy
from collections import Counter

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


def _validate_solution(solution, items, capacity):
    """Validate basic feasibility criteria from the assignment."""
    packed = []
    for bin_ in solution:
        if bin_.load > capacity:
            return False
        packed.extend(bin_.items)

    return Counter(packed) == Counter(items)


def _select_heuristics(heuristic_name: str | None):
    if heuristic_name is None:
        return HEURISTICS

    target = heuristic_name.strip().upper()
    selected = [h for h in HEURISTICS if h[0] == target]
    if not selected:
        available = ", ".join(name for name, _, _ in HEURISTICS)
        raise ValueError(f"Unknown heuristic '{heuristic_name}'. Available: {available}")
    return selected


def _collect_instance_paths(input_path: str) -> list[str]:
    if os.path.isdir(input_path):
        instance_paths = []
        for entry in sorted(os.listdir(input_path)):
            full_path = os.path.join(input_path, entry)
            if os.path.isfile(full_path) and os.path.splitext(entry)[1].lower() == ".txt":
                instance_paths.append(full_path)
        return instance_paths

    return [input_path]


def _run_single_instance(
    instance_path: str, runs: int = 3, iterations: int = 1000,
    alpha: float = 0.25, seed: int | None = None,
    heuristic_name: str | None = None,
    optimum: int | None = None,
):
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

    for name, heuristic, sort_order in _select_heuristics(heuristic_name):
        costs = []
        initial_cost = None
        start = time.perf_counter()
        best_run_solution = None
        best_run_cost = float("inf")

        for run_idx in range(runs):
            grasp = GRASP(alpha=alpha, iterations=iterations,
                          heuristic=heuristic, sort_order=sort_order)
            solution, initial_construction_cost, cost = grasp.solve_with_details(items, capacity)
            costs.append(cost)

            if cost < best_run_cost:
                best_run_cost = cost
                best_run_solution = deepcopy(solution)

            if run_idx == 0:
                initial_cost = initial_construction_cost

        elapsed = time.perf_counter() - start
        stats = compute_stats(costs, initial_cost, elapsed, optimum)
        if not _validate_solution(best_run_solution, items, capacity):
            raise ValueError(f"Invalid solution generated for heuristic {name} on {instance_name}")

        loss_display = f"{stats['loss_pct']:>6.2f}%" if stats["optimum"] is not None else "   n/a "

        print(f"{name:<8} {stats['initial']:>7} {stats['best']:>6} {stats['worst']:>6} "
              f"{stats['average']:>7.2f} {loss_display} {stats['time']:>8.3f}s")

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


def run_experiment(
    instance_path: str, runs: int = 3, iterations: int = 1000,
    alpha: float = 0.25, seed: int | None = None,
    heuristic_name: str | None = None,
    optimum: int | None = None,
):
    """Run all heuristics on one instance file or all instances in a directory.

    Args:
        instance_path: Path to an instance file or a directory of instances.
        runs: Number of independent GRASP runs per heuristic.
        iterations: GRASP iterations per run.
        alpha: RCL alpha parameter.
        seed: Optional random seed for reproducibility.
        heuristic_name: Optional heuristic code (e.g., BF, FFD, WFI).
        optimum: Optional known optimum bin count for loss percentage.
    """
    instance_paths = _collect_instance_paths(instance_path)
    if not instance_paths:
        raise FileNotFoundError(f"No instance files found in: {instance_path}")

    for current_instance_path in instance_paths:
        _run_single_instance(
            current_instance_path,
            runs=runs,
            iterations=iterations,
            alpha=alpha,
            seed=seed,
            heuristic_name=heuristic_name,
            optimum=optimum,
        )


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "instances"
    runs = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    iters = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    alpha = float(sys.argv[4]) if len(sys.argv) > 4 else 0.25
    heuristic_name = sys.argv[5] if len(sys.argv) > 5 else None
    optimum = int(sys.argv[6]) if len(sys.argv) > 6 else None
    run_experiment(
        path,
        runs=runs,
        iterations=iters,
        alpha=alpha,
        seed=42,
        heuristic_name=heuristic_name,
        optimum=optimum,
    )
