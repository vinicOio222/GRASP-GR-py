import random
from core.bin import Bin


class GRASPConstructor:
    """A class implementing the GRASP (Greedy Randomized Adaptive Search Procedure)
    constructor for the bin packing problem.

    Attributes:
        alpha (float): The parameter controlling the randomness of the construction.
        heuristic: The heuristic function used to insert items into bins.
        sort_order (str | None): Pre-sort strategy for items.
            'D' = decreasing (largest first in RCL),
            'I' = increasing (smallest first in RCL),
            None = no fixed sort (pure random RCL).
    """
    def __init__(self, alpha: float, heuristic, sort_order: str | None = 'D'):
        self.alpha = alpha
        self.heuristic = heuristic
        self.sort_order = sort_order

    def build(self, items, capacity):
        """Build a solution for the bin packing problem using the GRASP approach.

        Args:
            items (list): The list of items to be packed.
            capacity (int): The capacity of each bin.

        Returns:
            list: A list of bins, each containing the items packed in it.
        """
        remaining = items.copy()
        bins = []

        while remaining:
            if self.sort_order == 'D':
                remaining.sort(reverse=True)
            elif self.sort_order == 'I':
                remaining.sort(reverse=False)

            rcl_size = max(1, int(len(remaining) * self.alpha))
            rcl = remaining[:rcl_size]
            chosen = random.choice(rcl)
            self.heuristic.insert(chosen, bins, capacity)
            remaining.remove(chosen)

        return bins


def local_search(bins: list[Bin]):
    """Perform a local search to improve the solution by trying to move items between bins.

    Args:
        bins (list[Bin]): A list of bins representing the current solution.
    """
    improved = True
    while improved:
        improved = False
        bins.sort(key=lambda b: b.load)  # Try to empty least loaded bins first

        for source in bins[:]:
            other_bins = [b for b in bins if b is not source]
            items_to_place = source.items[:]
            placements = []
            success = True

            for item in items_to_place:
                placed = False
                for target in other_bins:
                    if target.can_fit(item):
                        target.add(item)
                        placements.append((target, item))
                        placed = True
                        break
                if not placed:
                    success = False
                    break

            if success:
                bins.remove(source)
                improved = True
                break
            else:
                # Undo all tentative placements
                for target, item in placements:
                    target.remove(item)

    return bins
