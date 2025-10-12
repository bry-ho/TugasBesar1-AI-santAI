import sys
from typing import List, Dict, Any, Tuple
from . import parser
from .algorithm.hill_climbing import HillClimbing
from .algorithm.simulated_annealing import SimulatedAnnealing, SimulatedAnnealingResult
from .algorithm.genetic import GeneticAlgorithm
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
    print("\n=== GENETIC ===")
    print("8. Genetic Algorithm")
    print("9. Genetic Algorithm - Comprehensive Experiments")
    print("\n0. Jalankan Semua Algoritma")

    while True:
        choice = input("\nPilihan (0-9): ").strip()
        if choice in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
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
            elif choice_num == 8:
                return "Genetic Algorithm", 8
            elif choice_num == 9:
                return "Genetic Algorithm - Comprehensive Experiments", 9
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
    elif choice_num == 8:  # Genetic Algorithm
        print("\n--- Parameter untuk Genetic Algorithm ---")
        params['population_size'] = get_int_input("Population Size", 50, 2)
        params['max_iterations'] = get_int_input("Maximum Generations", 100, 1)
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
        ("Genetic Algorithm", 8, {'population_size': 50, 'max_iterations': 100, 'mutation_rate': 0.1}),
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

def run_comprehensive_genetic_experiments(data: dict, objective_type: str):
    """Run comprehensive genetic algorithm experiments as specified in requirements"""
    print(f"\n{'='*80}")
    print("COMPREHENSIVE GENETIC ALGORITHM EXPERIMENTS")
    print(f"{'='*80}")
    
    import matplotlib.pyplot as plt
    import numpy as np
    from datetime import datetime
    
    print("This will run:")
    print("1. Population Size Control (50) with 3 different iteration counts - 3 runs each")
    print("2. Iteration Count Control (100) with 3 different population sizes - 3 runs each")
    print("\nGenerating plots and detailed analysis...")
    
    # Experiment 1: Population size as control (50), varying iterations
    print(f"\n{'#'*60}")
    print("EXPERIMENT 1: Population Size as Control (50)")
    print(f"{'#'*60}")
    
    pop_control_configs = [
        {'population_size': 50, 'max_iterations': 50},
        {'population_size': 50, 'max_iterations': 100}, 
        {'population_size': 50, 'max_iterations': 150}
    ]
    
    exp1_results = []
    for i, config in enumerate(pop_control_configs):
        print(f"\nConfiguration {i+1}: Pop={config['population_size']}, Iterations={config['max_iterations']}")
        config_results = []
        
        for run in range(3):
            print(f"  Run {run+1}/3...", end=" ", flush=True)
            ga = GeneticAlgorithm(data, objective_type=objective_type)
            result = ga.run(
                population_size=config['population_size'],
                max_iterations=config['max_iterations'],
                mutation_rate=0.1
            )
            config_results.append(result)
            print(f"Final: {result.final_value:.2f}, Duration: {result.duration:.3f}s")
        
        exp1_results.append({'config': config, 'results': config_results})
        
        # Print summary for this configuration
        final_values = [r.final_value for r in config_results]
        durations = [r.duration for r in config_results]
        best_result = min(config_results, key=lambda r: r.final_value)
        
        print(f"  Summary - Final Values: {final_values}")
        print(f"           Average: {np.mean(final_values):.2f}, Std: {np.std(final_values):.2f}")
        print(f"           Best Result: Initial={best_result.initial_value:.2f} → Final={best_result.final_value:.2f}")
    
    # Experiment 2: Iterations as control (100), varying population size
    print(f"\n{'#'*60}")
    print("EXPERIMENT 2: Iterations as Control (100)")
    print(f"{'#'*60}")
    
    iter_control_configs = [
        {'population_size': 30, 'max_iterations': 100},
        {'population_size': 60, 'max_iterations': 100},
        {'population_size': 90, 'max_iterations': 100}
    ]
    
    exp2_results = []
    for i, config in enumerate(iter_control_configs):
        print(f"\nConfiguration {i+1}: Pop={config['population_size']}, Iterations={config['max_iterations']}")
        config_results = []
        
        for run in range(3):
            print(f"  Run {run+1}/3...", end=" ", flush=True)
            ga = GeneticAlgorithm(data, objective_type=objective_type)
            result = ga.run(
                population_size=config['population_size'],
                max_iterations=config['max_iterations'],
                mutation_rate=0.1
            )
            config_results.append(result)
            print(f"Final: {result.final_value:.2f}, Duration: {result.duration:.3f}s")
        
        exp2_results.append({'config': config, 'results': config_results})
        
        # Print summary for this configuration
        final_values = [r.final_value for r in config_results]
        durations = [r.duration for r in config_results]
        best_result = min(config_results, key=lambda r: r.final_value)
        
        print(f"  Summary - Final Values: {final_values}")
        print(f"           Average: {np.mean(final_values):.2f}, Std: {np.std(final_values):.2f}")
        print(f"           Best Result: Initial={best_result.initial_value:.2f} → Final={best_result.final_value:.2f}")
    
    # Generate comprehensive plots
    print(f"\n{'='*60}")
    print("GENERATING ANALYSIS PLOTS")
    print(f"{'='*60}")
    
    try:
        # Create plots
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Comprehensive Genetic Algorithm Experiments Analysis', fontsize=16)
        
        # Plot 1: Experiment 1 - Best fitness evolution
        ax1 = axes[0, 0]
        for i, exp_result in enumerate(exp1_results):
            config = exp_result['config']
            results = exp_result['results']
            
            # Average best fitness across runs
            max_gens = max(len(r.best_fitness_history) for r in results)
            avg_best_fitness = []
            for gen in range(max_gens):
                gen_values = [r.best_fitness_history[gen] for r in results if gen < len(r.best_fitness_history)]
                avg_best_fitness.append(np.mean(gen_values))
            
            ax1.plot(avg_best_fitness, label=f'Iter={config["max_iterations"]}', marker='o', markersize=2)
        
        ax1.set_xlabel('Generation')
        ax1.set_ylabel('Best Objective Value')
        ax1.set_title('Exp1: Population Control (50) - Best Fitness Evolution')
        ax1.legend()
        ax1.grid(True)
        
        # Plot 2: Experiment 1 - Average fitness evolution
        ax2 = axes[0, 1]
        for i, exp_result in enumerate(exp1_results):
            config = exp_result['config']
            results = exp_result['results']
            
            max_gens = max(len(r.average_fitness_history) for r in results)
            avg_avg_fitness = []
            for gen in range(max_gens):
                gen_values = [r.average_fitness_history[gen] for r in results if gen < len(r.average_fitness_history)]
                avg_avg_fitness.append(np.mean(gen_values))
            
            ax2.plot(avg_avg_fitness, label=f'Iter={config["max_iterations"]}', marker='s', markersize=2)
        
        ax2.set_xlabel('Generation')
        ax2.set_ylabel('Average Objective Value')
        ax2.set_title('Exp1: Population Control (50) - Average Fitness Evolution')
        ax2.legend()
        ax2.grid(True)
        
        # Plot 3: Experiment 1 - Final values boxplot
        ax3 = axes[0, 2]
        exp1_final_values = []
        exp1_labels = []
        for exp_result in exp1_results:
            config = exp_result['config']
            results = exp_result['results']
            final_values = [r.final_value for r in results]
            exp1_final_values.append(final_values)
            exp1_labels.append(f'Iter={config["max_iterations"]}')
        
        ax3.boxplot(exp1_final_values, labels=exp1_labels)
        ax3.set_ylabel('Final Objective Value')
        ax3.set_title('Exp1: Final Values Distribution')
        ax3.grid(True)
        
        # Plot 4: Experiment 2 - Best fitness evolution
        ax4 = axes[1, 0]
        for i, exp_result in enumerate(exp2_results):
            config = exp_result['config']
            results = exp_result['results']
            
            max_gens = max(len(r.best_fitness_history) for r in results)
            avg_best_fitness = []
            for gen in range(max_gens):
                gen_values = [r.best_fitness_history[gen] for r in results if gen < len(r.best_fitness_history)]
                avg_best_fitness.append(np.mean(gen_values))
            
            ax4.plot(avg_best_fitness, label=f'Pop={config["population_size"]}', marker='o', markersize=2)
        
        ax4.set_xlabel('Generation')
        ax4.set_ylabel('Best Objective Value')
        ax4.set_title('Exp2: Iteration Control (100) - Best Fitness Evolution')
        ax4.legend()
        ax4.grid(True)
        
        # Plot 5: Experiment 2 - Average fitness evolution
        ax5 = axes[1, 1]
        for i, exp_result in enumerate(exp2_results):
            config = exp_result['config']
            results = exp_result['results']
            
            max_gens = max(len(r.average_fitness_history) for r in results)
            avg_avg_fitness = []
            for gen in range(max_gens):
                gen_values = [r.average_fitness_history[gen] for r in results if gen < len(r.average_fitness_history)]
                avg_avg_fitness.append(np.mean(gen_values))
            
            ax5.plot(avg_avg_fitness, label=f'Pop={config["population_size"]}', marker='s', markersize=2)
        
        ax5.set_xlabel('Generation')
        ax5.set_ylabel('Average Objective Value')
        ax5.set_title('Exp2: Iteration Control (100) - Average Fitness Evolution')
        ax5.legend()
        ax5.grid(True)
        
        # Plot 6: Experiment 2 - Final values boxplot
        ax6 = axes[1, 2]
        exp2_final_values = []
        exp2_labels = []
        for exp_result in exp2_results:
            config = exp_result['config']
            results = exp_result['results']
            final_values = [r.final_value for r in results]
            exp2_final_values.append(final_values)
            exp2_labels.append(f'Pop={config["population_size"]}')
        
        ax6.boxplot(exp2_final_values, labels=exp2_labels)
        ax6.set_ylabel('Final Objective Value')
        ax6.set_title('Exp2: Final Values Distribution')
        ax6.grid(True)
        
        plt.tight_layout()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plot_filename = f"genetic_comprehensive_analysis_{timestamp}.png"
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
        
        plt.show()
        
    except ImportError:
        print("⚠ matplotlib not available - skipping plot generation")
        print("  Install with: pip install matplotlib")
    
    # Print comprehensive summary
    print(f"\n{'='*80}")
    print("COMPREHENSIVE EXPERIMENT SUMMARY")
    print(f"{'='*80}")
    
    print("EXPERIMENT 1 - Population Size Control (50):")
    print("=" * 50)
    for i, exp_result in enumerate(exp1_results):
        config = exp_result['config']
        results = exp_result['results']
        final_values = [r.final_value for r in results]
        durations = [r.duration for r in results]
        best_result = min(results, key=lambda r: r.final_value)
        
        print(f"Config {i+1}: Iterations={config['max_iterations']}")
        print(f"  Final Values: {[f'{v:.2f}' for v in final_values]}")
        print(f"  Best: {min(final_values):.2f}, Average: {np.mean(final_values):.2f}")
        print(f"  Durations: {[f'{d:.3f}s' for d in durations]}")
        print(f"  Best Result: {best_result.initial_value:.2f} → {best_result.final_value:.2f}")
        print(f"  State Change: {len(best_result.initial_state)} → {len(best_result.final_state)} meetings")
    
    print("\\nEXPERIMENT 2 - Iteration Count Control (100):")
    print("=" * 50)
    for i, exp_result in enumerate(exp2_results):
        config = exp_result['config']
        results = exp_result['results']
        final_values = [r.final_value for r in results]
        durations = [r.duration for r in results]
        best_result = min(results, key=lambda r: r.final_value)
        
        print(f"Config {i+1}: Population={config['population_size']}")
        print(f"  Final Values: {[f'{v:.2f}' for v in final_values]}")
        print(f"  Best: {min(final_values):.2f}, Average: {np.mean(final_values):.2f}")
        print(f"  Durations: {[f'{d:.3f}s' for d in durations]}")
        print(f"  Best Result: {best_result.initial_value:.2f} → {best_result.final_value:.2f}")
        print(f"  State Change: {len(best_result.initial_state)} → {len(best_result.final_state)} meetings")

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
    elif choice_num == 9:  # Comprehensive Genetic Experiments
        run_comprehensive_genetic_experiments(data, objective_type)
    else:
        params = get_algorithm_parameters(choice_num)
        run_experiment(data, algorithm_name, choice_num, params, num_runs, objective_type)

    print("\n" + "="*60)
    print("EKSPERIMEN SELESAI!")
    print("="*60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
