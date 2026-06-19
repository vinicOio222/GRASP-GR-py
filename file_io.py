import re


def _parse_instance_values(content: str) -> list[int]:
    """Extract instance values from plain text or simple RTF exports."""
    if "\\rtf" in content or content.lstrip().startswith("{"):
        cleaned = re.sub(r"\\[a-zA-Z*]+-?\d* ?", " ", content)
        cleaned = cleaned.replace("{", " ").replace("}", " ").replace("\\", " ")
        return [int(value) for value in re.findall(r"\d+", cleaned)]

    return [int(value) for value in content.split()]


def read_instance(file_path: str) -> tuple[int, int, list[int]]:
    """Read an instance from a file and return the number of items, bin capacity, and list of item sizes."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        values = _parse_instance_values(file.read())
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
