"""Entry point and experiment runner for GRASP + Bin Packing heuristics.

Usage:
    python main.py [--instance PATH] [--runs N] [--iterations N] [--alpha A] [--heuristic CODE]

Defaults: runs=3, iterations=1000, alpha=0.25
"""

import argparse
import math
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
# Default parameters
# ---------------------------------------------------------------------------
ALPHA = 0.25
ITERATIONS = 1000
RUNS = 3
SEED = 42

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
    """Validate basic feasibility criteria from the assignment.
    
    Args:
        solution (list[Bin]): The list of bins representing the solution.
        items (list): The original list of items to be packed.
        capacity (float): The maximum capacity of each bin.
    """
    packed = []
    for bin_ in solution:
        if bin_.load > capacity:
            return False
        packed.extend(bin_.items)
    return Counter(packed) == Counter(items)


def _select_heuristics(heuristic_name):
    """Select heuristics based on the provided name.
    
    Args:
        heuristic_name (str | None): The name of the heuristic to select. If None, all heuristics are selected.
    """
    if heuristic_name is None:
        return HEURISTICS
    target = heuristic_name.strip().upper()
    selected = [h for h in HEURISTICS if h[0] == target]
    if not selected:
        available = ", ".join(name for name, _, _ in HEURISTICS)
        raise ValueError(f"Unknown heuristic '{heuristic_name}'. Available: {available}")
    return selected


def _collect_instance_paths(input_path: str) -> list[str]:
    """Collect instance file paths from a directory or return the single file path.
    
    Args:
        input_path (str): The path to a directory or a single instance file.
    """
    if os.path.isdir(input_path):
        instance_paths = []
        for entry in sorted(os.listdir(input_path)):
            full_path = os.path.join(input_path, entry)
            if os.path.isfile(full_path) and os.path.splitext(entry)[1].lower() == ".txt":
                instance_paths.append(full_path)
        return instance_paths
    return [input_path]


def _instance_label(instance_name: str) -> str:
    base_name = os.path.splitext(instance_name)[0].lstrip("_")
    return base_name.split("_")[0]


def _print_summary_table(summary_rows):
    if not summary_rows:
        return

    print("\n" + "=" * 96)
    print("Consolidated results by instance")
    print("=" * 96)
    header = (
        f"{'No':<3} {'Instance':<10} {'n':>5} {'C':>5} {'Initial':>8} {'Worst':>6} "
        f"{'Average':>8} {'Best':>8} {'Loss%':>8} {'Time(s)':>10}"
    )
    print(header)
    print("-" * 96)

    for idx, row in enumerate(summary_rows):
        print(
            f"{idx:<3} {row['instance']: <10} {row['n']:>5} {row['capacity']:>5} "
            f"{row['initial']:>8} {row['worst']:>6} {row['average']:>8.2f} "
            f"{row['best']:>8} {row['loss_pct']:>7.2f}% {row['time']:>10.3f}"
        )

    print("-" * 96)
    print("Note: the Time(s) column represents the total time spent on the instance.")
    print("=" * 96 + "\n")


def _run_single_instance(
    instance_path: str, runs: int = RUNS, iterations: int = ITERATIONS,
    alpha: float = ALPHA, seed: int | None = SEED,
    heuristic_name: str | None = None,
):
    """Run all heuristics on a single instance file."""
    if seed is not None:
        random.seed(seed)

    n_items, capacity, items = read_instance(instance_path)
    instance_name = os.path.basename(instance_path)

    # Lower bound teórico: ceil(soma dos pesos / capacidade)
    optimum = math.ceil(sum(items) / capacity)

    print(f"\n{'='*70}")
    print(f"  Instance : {instance_name}")
    print(f"  Items    : {len(items)}  |  Capacity: {capacity}  |  LB: {optimum}")
    print(f"  Runs     : {runs}  |  Iterations: {iterations}  |  Alpha: {alpha}")
    print(f"{'='*70}")
    header = f"{'Heuristic':<8} {'Initial':>7} {'Best':>6} {'Worst':>6} {'Avg':>7} {'Loss%':>7} {'Time(s)':>9}"
    print(header)
    print("-" * 70)

    os.makedirs("results", exist_ok=True)
    instance_start = time.perf_counter()
    overall_best_cost = float("inf")
    overall_best_solution = None
    overall_best_name = ""
    overall_best_stats = None

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

        print(f"{name:<8} {stats['initial']:>7} {stats['best']:>6} {stats['worst']:>6} "
              f"{stats['average']:>7.2f} {stats['loss_pct']:>6.2f}% {stats['time']:>8.3f}s")

        out_file = f"results/{instance_name}_{name}.txt"
        write_solution(best_run_solution, out_file, verbose=False)

        if best_run_cost < overall_best_cost:
            overall_best_cost = best_run_cost
            overall_best_solution = best_run_solution
            overall_best_name = name
            overall_best_stats = stats

    print("-" * 70)
    print(f"  Overall best: {overall_best_name} with {overall_best_cost} bins")
    best_out = f"results/{instance_name}_BEST.txt"
    write_solution(overall_best_solution, best_out, verbose=True)
    print(f"  Best solution saved to: {best_out}")
    print(f"{'='*70}\n")

    total_elapsed = time.perf_counter() - instance_start
    return {
        "instance": _instance_label(instance_name),
        "n": n_items,
        "capacity": capacity,
        "initial": overall_best_stats["initial"],
        "worst": overall_best_stats["worst"],
        "average": overall_best_stats["average"],
        "best": overall_best_stats["best"],
        "loss_pct": overall_best_stats["loss_pct"],
        "time": total_elapsed,
        "heuristic": overall_best_name,
    }


def run_experiment(
    instance_path: str, runs: int = RUNS, iterations: int = ITERATIONS,
    alpha: float = ALPHA, seed: int | None = SEED,
    heuristic_name: str | None = None,
):
    """Run all heuristics on one instance file or all .txt instances in a directory."""
    instance_paths = _collect_instance_paths(instance_path)
    if not instance_paths:
        raise FileNotFoundError(f"No instance files found in: {instance_path}")

    summary_rows = []
    for current_instance_path in instance_paths:
        summary_rows.append(_run_single_instance(
            current_instance_path,
            runs=runs,
            iterations=iterations,
            alpha=alpha,
            seed=seed,
            heuristic_name=heuristic_name,
        ))

    _print_summary_table(summary_rows)


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def _alpha_value(value: str) -> float:
    parsed = float(value)
    if not 0.0 <= parsed <= 1.0:
        raise argparse.ArgumentTypeError("must be between 0 and 1")
    return parsed


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Run GRASP experiments for Bin Packing instances."
    )
    parser.add_argument(
        "--instance",
        "-i",
        dest="instance_file_or_dir",
        default="instances",
        help="Path to a .txt instance file or a directory containing .txt instances.",
    )
    parser.add_argument(
        "--runs",
        "-r",
        type=_positive_int,
        default=RUNS,
        help=f"Number of independent runs per heuristic (default: {RUNS}).",
    )
    parser.add_argument(
        "--iterations",
        "-n",
        type=_positive_int,
        default=ITERATIONS,
        help=f"Number of GRASP iterations per run (default: {ITERATIONS}).",
    )
    parser.add_argument(
        "--alpha",
        "-a",
        type=_alpha_value,
        default=ALPHA,
        help=f"RCL alpha value in [0, 1] (default: {ALPHA}).",
    )
    parser.add_argument(
        "--heuristic",
        "-H",
        default=None,
        help="Optional heuristic code (e.g., BF, FFD, WFI).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    run_experiment(
        args.instance_file_or_dir,
        runs=args.runs,
        iterations=args.iterations,
        alpha=args.alpha,
        seed=SEED,
        heuristic_name=args.heuristic,
    )
    