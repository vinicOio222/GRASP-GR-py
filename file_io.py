def read_instance(file_path: str) -> tuple[int, int, list[int]]:
    """Read an instance from a file and return the number of items, bin capacity, and list of item sizes."""
    with open(file_path, "r") as file:
        values = [
            int(x)
            for x in file.read().split()
        ]
    n = values[0]  # Number of items
    capacity = values[1]  # Capacity of each bin
    items = values[2:]  # List of item sizes
    
    return n, capacity, items


def write_solution(solution, file_path: str = "solution.txt", verbose: bool = False):
    """Write the solution to a file, including the number of bins used and the items in each bin."""
    if verbose:
        print(f"\n Bins usados: {len(solution)}")
        for idx, bin_ in enumerate(solution):
            print(f" Bin {idx + 1}: {bin_.items}")
    
    with open(file_path, "w") as file:
        file.write(f"{len(solution)}\n")
        for bin_ in solution:
            file.write(" ".join(map(str, bin_.items)) + "\n")
