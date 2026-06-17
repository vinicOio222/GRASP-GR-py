class SortedHeuristic:
    """Wraps any packing heuristic with pre-sorting of items.

    Args:
        base: The base heuristic instance (must implement insert()).
        order: 'D' for decreasing, 'I' for increasing.
    """

    def __init__(self, base, order: str):
        self.base = base
        self.reverse = order.upper() == "D"

    def insert(self, item, bins, capacity):
        self.base.insert(item, bins, capacity)
