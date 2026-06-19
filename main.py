from experiments.runner import run_experiment

# Constants for default parameters
ALPHA = 0.25
ITERATIONS = 1000
RUNS = 3

def main():
    run_experiment(
        "instances", runs=RUNS, iterations=ITERATIONS, alpha=ALPHA, seed=42
    )

if __name__ == "__main__":
    main()
    