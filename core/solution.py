class Solution:
    """Represents a solution to the bin packing problem."""
    
    def __init__(self, bins):
        self.bins = bins
    
    @property
    def cost(self):
        """Calculate the cost of the solution, typically the number of bins used."""
        return len(self.bins)
    
    def copy(self):
        """Create a deep copy of the solution."""
        from copy import deepcopy
        return deepcopy(self)
