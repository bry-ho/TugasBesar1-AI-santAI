import sys
from typing import List, Dict, Any, Tuple
from . import parser
from .algorithm.hill_climbing import HillClimbing
from .algorithm.simulated_annealing import SimulatedAnnealing, SimulatedAnnealingResult
from .algorithm.genetic import GeneticAlgorithm
from .output_formatter import (
    print_summary, print_schedule, AlgorithmResult, print_hill_climbing_result, print_simulated_annealing_result, print_genetic_result
)
from . import plot

def get_int_input(prompt: str, default: int, min_val: int = 1) -> int:
    while True:
        try:
            user_input = input(f"{prompt} (default={default}): ").strip()
            if user_input == "":
                return default
            value = int(user_input)
            if value < min_val:
                print(f"Nilai harus >= {min_val}. Coba lagi.")
                continue
            return value
        except ValueError:
            print("Input tidak valid. Masukkan angka.")

def get_objective_type() -> str:
    print("\n" + "="*60)
    print("Pilih Objective Function:")
    print("="*60)
    print("1. Student Conflict")
    print("2. Room Conflict")
    print("3. Room Capacity")
    print("4. Combined (semua)")

    while True:
        choice = input("Pilihan (1-4, default=4): ").strip()
        if choice == "" or choice == "4":
            return "combined"
        elif choice == "1":
            return "student_conflict"
        elif choice == "2":
            return "room_conflict"
        elif choice == "3":
            return "capacity"
        else:
            print("Pilihan tidak valid. Coba lagi.")

def select_algorithm() -> Tuple[str, int]:
    print("\n" + "="*60)
    print("PILIH ALGORITMA")
    print("="*60)
    print("=== HILL CLIMBING ===")
    print("1. Steepest Ascent Hill Climbing")
    print("2. Stochastic Hill Climbing")
    print("3. Hill Climbing with Sideways Move")
    print("4. Random Restart Hill Climbing")
    print("\n=== SIMULATED ANNEALING ===")
    print("5. Simulated Annealing - Linear Cooling")
    print("6. Simulated Annealing - Exponential Cooling")
    print("7. Simulated Annealing - Logarithmic Cooling")
    print("\n=== GENETIC ===")
    print("8. Genetic Algorithm")

    while True:
        choice = input("\nPilihan (0-9): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            choice_num = int(choice)
            if choice_num == 1:
                return "Steepest Ascent Hill Climbing", 1
            elif choice_num == 2:
                return "Stochastic Hill Climbing", 2
            elif choice_num == 3:
                return "Hill Climbing with Sideways Move", 3
            elif choice_num == 4:
                return "Random Restart Hill Climbing", 4
            elif choice_num == 5:
                return "Simulated Annealing (Linear)", 5
            elif choice_num == 6:
                return "Simulated Annealing (Exponential)", 6
            elif choice_num == 7:
                return "Simulated Annealing (Logarithmic)", 7 
            elif choice_num == 8:
                return "Genetic Algorithm", 8
        else:
            print("Pilihan tidak valid. Coba lagi.")

def get_algorithm_parameters(choice_num: int, run_num: int) -> Dict[str, Any]:
    params = {}
    print("\n--- Masukkan Param Untuk Run ke-"+ str(run_num)+" ---")

    if choice_num == 3:
        print("\n--- Parameter untuk Sideways Move ---")
        params['max_sideways'] = get_int_input("Maximum Sideways Moves", 100, 1)
    elif choice_num == 4:
        print("\n--- Parameter untuk Random Restart ---")
        params['max_restarts'] = get_int_input("Maximum Restarts", 10, 1)
        params['max_iterations_per_restart'] = get_int_input("Maximum Iterations per Restart", 100, 1)
    elif choice_num in [5, 6, 7]:  # Simulated Annealing
        print("\n--- Parameter untuk Simulated Annealing ---")
        params['initial_temperature'] = get_float_input("Initial Temperature", 1000.0, 1.0)
        params['final_temperature'] = get_float_input("Final Temperature", 0.1, 0.001)
        params['max_iterations'] = get_int_input("Maximum Iterations", 1000, 1)
        
        if choice_num == 6:  # Exponential cooling
            params['alpha'] = get_float_input("Alpha (Cooling Rate)", 0.95, 0.01, 0.99)
    elif choice_num == 8:  # Genetic Algorithm
        print("\n--- Parameter untuk Genetic Algorithm ---")
        params['population_size'] = get_int_input("Population Size", 50, 2)
        params['max_iterations'] = get_int_input("Maximum Iterations (Generations)", 100, 1)
        params['mutation_rate'] = get_float_input("Mutation Rate", 0.1, 0.0, 1.0)

    return params

def get_float_input(prompt: str, default: float, min_val: float = 0.0, max_val: float = float('inf')) -> float:
    while True:
        try:
            user_input = input(f"{prompt} (default={default}): ").strip()
            if user_input == "":
                return default
            value = float(user_input)
            if value < min_val or value > max_val:
                print(f"Nilai harus antara {min_val} dan {max_val}. Coba lagi.")
                continue
            return value
        except ValueError:
            print("Input tidak valid. Masukkan angka desimal.")

def run_algorithm(data: dict, choice_num: int, params: Dict[str, Any], objective_type: str) -> AlgorithmResult:
    if choice_num in [1, 2, 3, 4]:  # Hill Climbing algorithms
        hc = HillClimbing(data, objective_type=objective_type)
        if choice_num == 1:
            return hc.steepest_ascent()
        elif choice_num == 2:
            return hc.stochastic()
        elif choice_num == 3:
            return hc.sideways_move(**params)
        elif choice_num == 4:
            return hc.random_restart(**params)
    elif choice_num in [5, 6, 7]:  # Simulated Annealing algorithms
        sa = SimulatedAnnealing(data, objective_type=objective_type)
        if choice_num == 5:  # Linear cooling
            return sa.run_linear_cooling(
                params.get('initial_temperature', 1000.0),
                params.get('final_temperature', 0.1),
                params.get('max_iterations', 1000)
            )
        elif choice_num == 6:  # Exponential cooling
            return sa.run_exponential_cooling(
                params.get('initial_temperature', 1000.0),
                params.get('alpha', 0.95),
                params.get('max_iterations', 1000)
            )
        elif choice_num == 7:  # Logarithmic cooling
            return sa.run_logarithmic_cooling(
                params.get('initial_temperature', 1000.0),
                params.get('max_iterations', 1000)
            )
    elif choice_num == 8:  # Genetic Algorithm
        ga = GeneticAlgorithm(data, objective_type=objective_type)
        return ga.run(
            population_size=params.get('population_size', 50),
            max_iterations=params.get('max_iterations', 100),
            mutation_rate=params.get('mutation_rate', 0.1)
        )
    else:
        raise ValueError(f"Unknown algorithm choice: {choice_num}")


def run_experiment(data: dict, algorithm_name: str, choice_num: int, num_runs: int, objective_type: str):
    print(f"\n{'#'*60}")
    print(f"EKSPERIMEN: {algorithm_name}")
    print(f"{'#'*60}")

    for run in range(num_runs):
        params = get_algorithm_parameters(choice_num, run + 1)
        print(f"\n--- Run {run + 1}/{num_runs} ---")
        result = run_algorithm(data, choice_num, params, objective_type)

        if choice_num == 8: 
            print_genetic_result(result, algorithm_name, run + 1)
        elif isinstance(result, SimulatedAnnealingResult):
            print_simulated_annealing_result(result, algorithm_name, run + 1)
        else:
            print_hill_climbing_result(result, algorithm_name, run + 1)

        print_schedule(result.initial_state, f"STATE AWAL (Run {run + 1})")
        print_schedule(result.final_state, f"STATE AKHIR (Run {run + 1})")
    
        print(f"\n{'='*60}")
        print("GENERATING PLOTS")
        print(f"{'='*60}")
        
        try:
            plot.plot_objective_history(result, algorithm_name, run + 1)

            if isinstance(result, SimulatedAnnealingResult):
                plot.plot_simulated_annealing_eET(result, run + 1)
            
            if choice_num == 8:
                plot.plot_genetic_population_fitness(result, run + 1)
        
        except Exception as e:
            print(f"Error generating plots: {e}")


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("Usage: python -m src.main <input.json>")
        return 1

    path = argv[1]
    try:
        data = parser.load_and_parse(path)
    except Exception as e:
        print(f"Failed to read JSON file '{path}': {e}")
        return 1

    print(f"\nData loaded from: {path}")
    print_summary(data)

    objective_type = get_objective_type()
    num_runs = get_int_input("\nJumlah run per algoritma", 3, 1)
    algorithm_name, choice_num = select_algorithm()

    run_experiment(data, algorithm_name, choice_num, num_runs, objective_type)

    print("\n" + "="*60)
    print("EKSPERIMEN SELESAI!")
    print("="*60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
