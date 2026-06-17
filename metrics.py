def average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def loss_percentage(obtained: float, optimum: float) -> float:
    return ((obtained - optimum) / optimum) * 100 if optimum != 0 else 0.0


def compute_stats(costs: list[int], initial_cost: int, exec_time: float) -> dict:
    """Compute experiment statistics from a list of solution costs across runs.

    Args:
        costs: Number of bins from each independent run.
        initial_cost: Cost of the very first (pre-local-search) solution.
        exec_time: Total execution time in seconds.

    Returns:
        dict with keys: initial, worst, average, best, loss_pct, time.
    """
    best = min(costs)
    worst = max(costs)
    avg = average(costs)
    loss = loss_percentage(avg, best)
    return {
        "initial": initial_cost,
        "worst": worst,
        "average": avg,
        "best": best,
        "loss_pct": loss,
        "time": exec_time,
    }
