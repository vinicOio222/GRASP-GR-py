from experiments.runner import run_experiment

# Constants for default parameters
ALPHA = 0.25
ITERATIONS = 1000
RUNS = 3
OPTIMUM = 50
SEED = 42

def main():
    run_experiment(
        instance_path="instances", runs=RUNS, iterations=ITERATIONS,
        alpha=ALPHA, seed=SEED, optimum=OPTIMUM
    )

if __name__ == "__main__":
    main()
    