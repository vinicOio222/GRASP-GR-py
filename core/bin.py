class Bin:
    """A class representing a bin that can hold items up to a certain capacity.
    
    Attributes:
        capacity (float): The maximum capacity of the bin.
        items (list): A list of items currently in the bin.
    """
    def __init__(self, capacity: float):
        self.capacity = capacity
        self.items = []
        self._load = 0.0
        
    @property
    def load(self):
        """Calculate the current load of the bin."""
        return self._load
    
    @property
    def remaining(self):
        """Calculate the remaining capacity of the bin."""
        return self.capacity - self._load
    
    def can_fit(self, item: float) -> bool:
        """Check if an item can fit in the bin without exceeding its capacity.
        
        Args:
            item (float): The size of the item to check.
        """
        return self._load + item <= self.capacity
    
    def add(self, item: float):
        """Add an item to the bin if it can fit.
        
        Args:
            item (float): The size of the item to add.
        """
        self.items.append(item)
        self._load += item
        
    def remove(self, item: float):
        """Remove an item from the bin.
        
        Args:
            item (float): The size of the item to remove.
        """
        self.items.remove(item)
        self._load -= item
        
    def is_empty(self) -> bool:
        """Check if the bin is empty."""
        return len(self.items) == 0
    