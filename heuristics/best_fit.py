from core.bin import Bin

class BestFit:
    """Best Fit heuristic for the bin packing problem."""
    
    @staticmethod
    def insert(item, bins: list[Bin], capacity):
        """Best Fit heuristic for the bin packing problem.
        
        Args:
            item (float): The size of the item to be packed.
            bins (list[Bin]): A list of existing bins.
            capacity (float): The maximum capacity of each bin.
        """
        best_bin = None
        best_space = float("inf") # Initialize as an infinity space

        # Iterate through existing bins to
        # find the best fit for the item
        for b in bins:
            if b.can_fit(item):
                space = b.remaining - item
                if space < best_space:
                    best_space = space
                    best_bin = b

        # If a suitable bin is found, add the item
        # to it; otherwise, create a new bin    
        if best_bin is not None:
            best_bin.add(item)
        else:
            new_bin = Bin(capacity)
            new_bin.add(item)
            bins.append(new_bin)
