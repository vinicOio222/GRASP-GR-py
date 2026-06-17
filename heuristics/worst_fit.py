from core.bin import Bin


class WorstFit:
    """Worst Fit heuristic: place item in the bin with the most remaining space."""

    def insert(self, item, bins, capacity):
        """Worst Fit heuristic for the bin packing problem.
        
        Args:
            item (float): The size of the item to be packed.
            bins (list[Bin]): A list of existing bins.
            capacity (float): The maximum capacity of each bin.
        """
        worst_bin = None
        worst_space = -1

        # Iterate through existing bins to find the one
        # with the most remaining space that can fit the item
        for b in bins:
            if b.can_fit(item) and b.remaining > worst_space:
                worst_space = b.remaining
                worst_bin = b

        # If a suitable bin is found, add the item to it; otherwise, create a new bin
        if worst_bin is not None:
            worst_bin.add(item)
        else:
            new_bin = Bin(capacity)
            new_bin.add(item)
            bins.append(new_bin)
