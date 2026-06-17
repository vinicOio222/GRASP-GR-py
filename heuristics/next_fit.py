from core.bin import Bin


class NextFit:
    """Next Fit heuristic for the bin packing problem."""

    def insert(self, item, bins, capacity):
        """Next Fit heuristic for the bin packing problem.
        
        Args:
            item (float): The size of the item to be packed.
            bins (list[Bin]): A list of existing bins.
            capacity (float): The maximum capacity of each bin.
        """
        # Place the item in the current bin if it fits; otherwise, create a new bin
        if bins and bins[-1].can_fit(item):
            bins[-1].add(item)
        else:
            new_bin = Bin(capacity)
            new_bin.add(item)
            bins.append(new_bin)
