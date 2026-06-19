from copy import deepcopy

from grasp.constructor import GRASPConstructor, local_search


class GRASP:
    """A class implementing the GRASP metaheuristic for the bin packing problem.

    Attributes:
        alpha (float): Controls RCL randomness (0 = greedy, 1 = fully random).
        iterations (int): Number of GRASP iterations.
        heuristic: Packing heuristic (must implement insert()).
        sort_order (str | None): Item ordering in construction ('D', 'I', or None).
    """
    def __init__(self, alpha=0.3, iterations=100, heuristic=None, sort_order='D'):
        self.alpha = alpha
        self.iterations = iterations
        self.heuristic = heuristic
        self.sort_order = sort_order

    def solve(self, items, capacity):
        """Backward-compatible API that returns only the best solution."""
        best_solution, _, _ = self.solve_with_details(items, capacity)
        return best_solution

    def solve_with_details(self, items, capacity):
        """Solve the bin packing problem using the GRASP approach.

        Args:
            items (list): The list of items to be packed.
            capacity (int): The capacity of each bin.

        Returns:
            tuple:
                - best solution bins
                - initial construction cost (before local search)
                - best cost after local search
        """
        constructor = GRASPConstructor(self.alpha, self.heuristic, self.sort_order)
        best_solution = None
        best_cost = float("inf")
        initial_construction_cost = None

        for _ in range(self.iterations):
            bins = constructor.build(items, capacity)
            if initial_construction_cost is None:
                initial_construction_cost = len(bins)

            improved_bins = local_search(bins)
            cost = len(improved_bins)

            if cost < best_cost:
                best_cost = cost
                best_solution = deepcopy(improved_bins)

        return best_solution, initial_construction_cost, best_cost
