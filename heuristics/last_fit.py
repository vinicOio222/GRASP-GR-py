from core.bin import Bin


class LastFit:
    """Last Fit heuristic: place item in the last bin that can fit it."""

    def insert(self, item, bins, capacity):
        """Last Fit heuristic for the bin packing problem.
        
        Args:
            item (float): The size of the item to be packed.
            bins (list[Bin]): A list of existing bins.
            capacity (float): The maximum capacity of each bin.
        """
        # Iterate through bins in reverse order to
        # find the last one that can fit the item
        for b in reversed(bins):
            if b.can_fit(item):
                b.add(item)
                return
        
        # If no existing bin can accommodate the item, create a new bin
        new_bin = Bin(capacity)
        new_bin.add(item)
        bins.append(new_bin)
