import sys
from typing import List, Dict, Any, Tuple, Union
from . import parser
from .algorithm.hill_climbing import HillClimbing, HillClimbingResult
from .algorithm.simulated_annealing import SimulatedAnnealing, SimulatedAnnealingResult
from .output_formatter import (
    print_summary, print_schedule, print_result_summary, 
    print_statistics, print_objective_history, print_temperature_history,
    print_comparison_table, print_final_schedule_summary, AlgorithmResult
)

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
    print("\n0. Jalankan Semua Algoritma")

    while True:
        choice = input("\nPilihan (0-7): ").strip()
        if choice in ["0", "1", "2", "3", "4", "5", "6", "7"]:
            choice_num = int(choice)
            if choice_num == 0:
                return "ALL", 0
            elif choice_num == 1:
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
        else:
            print("Pilihan tidak valid. Coba lagi.")

def get_algorithm_parameters(choice_num: int) -> Dict[str, Any]:
    params = {}

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
    else:
        raise ValueError(f"Unknown algorithm choice: {choice_num}")


def run_experiment(data: dict, algorithm_name: str, choice_num: int,
                   params: Dict[str, Any], num_runs: int, objective_type: str):
    print(f"\n{'#'*60}")
    print(f"EKSPERIMEN: {algorithm_name}")
    if params:
        print(f"Parameter: {params}")
    print(f"{'#'*60}")

    results = []
    for run in range(num_runs):
        print(f"\n--- Run {run + 1}/{num_runs} ---")
        result = run_algorithm(data, choice_num, params, objective_type)
        results.append(result)
        print_result_summary(result, algorithm_name, run + 1)

        # kondisi awal schedule
        print_schedule(result.initial_state, f"STATE AWAL (Run {run + 1})")
        # hasil akhir schedule
        print_schedule(result.final_state, f"STATE AKHIR (Run {run + 1})")
        # history dari objective function
        print_objective_history(result, 1)
            
        # temperature history untuk SA
        if isinstance(result, SimulatedAnnealingResult):
            print_temperature_history(result, 1)

    print_statistics(results, algorithm_name, num_runs)
    
    # Show the best schedule from all runs
    best_result = min(results, key=lambda r: r.final_value)
    best_run_index = results.index(best_result) + 1
    
    print_schedule(best_result.final_state, f"JADWAL TERBAIK (Run {best_run_index}) - {algorithm_name}")
    print_final_schedule_summary(best_result, algorithm_name, best_run_index)
    
    return results


def run_all_algorithms(data: dict, num_runs: int, objective_type: str):
    algorithms = [
        ("Steepest Ascent Hill Climbing", 1, {}),
        ("Stochastic Hill Climbing", 2, {}),
        ("Hill Climbing with Sideways Move", 3, {'max_sideways': 100}),
        ("Random Restart Hill Climbing", 4, {'max_restarts': 10, 'max_iterations_per_restart': 100}),
        ("Simulated Annealing (Linear)", 5, {'initial_temperature': 1000.0, 'final_temperature': 0.1, 'max_iterations': 1000}),
        ("Simulated Annealing (Exponential)", 6, {'initial_temperature': 1000.0, 'alpha': 0.95, 'max_iterations': 1000}),
        ("Simulated Annealing (Logarithmic)", 7, {'initial_temperature': 1000.0, 'max_iterations': 1000}),
    ]

    all_results = {}
    for algo_name, choice_num, params in algorithms:
        results = run_experiment(data, algo_name, choice_num, params, num_runs, objective_type)
        best_result = min(results, key=lambda r: r.final_value)
        all_results[algo_name] = best_result

    print_comparison_table(all_results)
    
    # Tabel perbandingan tiap algoritma
    overall_best_result = min(all_results.values(), key=lambda r: r.final_value)
    overall_best_algorithm = [algo for algo, result in all_results.items() if result == overall_best_result][0]
    
    print_schedule(overall_best_result.final_state, f"JADWAL TERBAIK KESELURUHAN - {overall_best_algorithm}")
    print_final_schedule_summary(overall_best_result, f"KESELURUHAN - {overall_best_algorithm}")

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

    if algorithm_name == "ALL":
        run_all_algorithms(data, num_runs, objective_type)
    else:
        params = get_algorithm_parameters(choice_num)
        run_experiment(data, algorithm_name, choice_num, params, num_runs, objective_type)

    print("\n" + "="*60)
    print("EKSPERIMEN SELESAI!")
    print("="*60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
