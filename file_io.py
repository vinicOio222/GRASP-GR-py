def read_instance(file_path: str) -> tuple[int, int, list[int]]:
    """Read an instance from a file and return the number of items, bin capacity, and list of item sizes."""
    if not file_path.lower().endswith(".txt"):
        raise ValueError(f"Only .txt instance files are supported: {file_path}")

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        values = [int(value) for value in file.read().split()]

    if len(values) < 2:
        raise ValueError(f"Invalid instance format in: {file_path}")

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
