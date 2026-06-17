from core.bin import Bin

class FirstFit:
    """First Fit heuristic for the bin packing problem."""

    def insert(self, item, bins, capacity):
        """First Fit heuristic for the bin packing problem.
        
        Args:
            item (float): The size of the item to be packed.
            bins (list[Bin]): A list of existing bins.
            capacity (float): The maximum capacity of each bin.
        """
        # Iterate through existing bins and place the item
        # in the first one that can accommodate it
        for bin_ in bins:

            if bin_.can_fit(item):
                bin_.add(item)
                return
        
        # If no existing bin can accommodate the item,
        # create a new bin and add the item to it
        new_bin = Bin(capacity)
        new_bin.add(item)
        bins.append(new_bin)
