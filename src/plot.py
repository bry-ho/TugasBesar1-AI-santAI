import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os


def plot_objective_history(result, algorithm_name: str, run_num: int):
    if not hasattr(result, 'objective_history') or not result.objective_history:
        print(f"No objective history available for {algorithm_name}")
        return
    
    plt.figure(figsize=(10, 6))
    
    iterations = list(range(len(result.objective_history)))
    plt.plot(iterations, result.objective_history, 'b-', linewidth=2, label='Objective Value')
    
    plt.plot(0, result.initial_value, 'go', markersize=10, label=f'Initial: {result.initial_value:.2f}')
    plt.plot(len(result.objective_history)-1, result.final_value, 'ro', markersize=10, 
             label=f'Final: {result.final_value:.2f}')
    
    plt.xlabel('Iteration', fontsize=12)
    plt.ylabel('Objective Function Value', fontsize=12)
    plt.title(f'{algorithm_name} - Objective Function vs Iterations (Run {run_num})', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    
    improvement = result.initial_value - result.final_value
    stats_text = f'Iterations: {result.iterations}\n'
    stats_text += f'Improvement: {improvement:.2f}\n'
    stats_text += f'Duration: {result.duration:.3f}s'
    
    plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    plots_dir = os.path.join(project_root, 'plots')
    
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    
    safe_algo_name = algorithm_name.replace(' ', '_').replace('(', '').replace(')', '')
    filename = f"{timestamp}_{safe_algo_name}_run{run_num}.png"
    save_path = os.path.join(plots_dir, filename)
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.close()


def plot_genetic_population_fitness(result, run_num: int):
    if not hasattr(result, 'best_fitness_history') or not result.best_fitness_history:
        print("No fitness history available for Genetic Algorithm")
        return
    
    if not hasattr(result, 'average_fitness_history') or not result.average_fitness_history:
        print("No average fitness history available for Genetic Algorithm")
        return
    
    plt.figure(figsize=(12, 7))
    
    generations = list(range(len(result.best_fitness_history)))
    
    plt.plot(generations, result.best_fitness_history, 'b-', linewidth=2.5, 
             label='Best Fitness', marker='o', markersize=4, 
             markevery=max(1, len(generations)//20))
    
    plt.plot(generations, result.average_fitness_history, 'r--', linewidth=2.5, 
             label='Average Fitness', marker='s', markersize=4,
             markevery=max(1, len(generations)//20))
    
    plt.plot(0, result.best_fitness_history[0], 'go', markersize=12, 
             label=f'Initial Best: {result.best_fitness_history[0]:.2f}', zorder=5)
    plt.plot(len(generations)-1, result.best_fitness_history[-1], 'mo', markersize=12, 
             label=f'Final Best: {result.best_fitness_history[-1]:.2f}', zorder=5)
    
    plt.xlabel('Generasi', fontsize=13)
    plt.ylabel('Objective Function Value', fontsize=13)
    plt.title(f'Genetic Algorithm - Best & Average Fitness vs Generasi (Run {run_num})', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=10, loc='best')
    plt.grid(True, alpha=0.3)
    
    improvement = result.best_fitness_history[0] - result.best_fitness_history[-1]
    avg_improvement = result.average_fitness_history[0] - result.average_fitness_history[-1]
    
    stats_text = f'Population Size: {result.population_size}\n'
    stats_text += f'Generations: {result.iterations}\n'
    stats_text += f'Best Improvement: {improvement:.2f}\n'
    stats_text += f'Avg Improvement: {avg_improvement:.2f}\n'
    stats_text += f'Final Best: {result.best_fitness_history[-1]:.2f}\n'
    stats_text += f'Final Average: {result.average_fitness_history[-1]:.2f}\n'
    stats_text += f'Duration: {result.duration:.3f}s'
    
    plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
             fontsize=9, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

    plt.tight_layout()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    plots_dir = os.path.join(project_root, 'plots')
    
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    
    filename = f"{timestamp}_Genetic_Algorithm_run{run_num}.png"
    save_path = os.path.join(plots_dir, filename)
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.close()


def plot_simulated_annealing_eET(result, run_num: int):
    if not hasattr(result, 'objective_history') or not result.objective_history:
        print("No objective history available")
        return
    
    if not hasattr(result, 'temperature_history') or not result.temperature_history:
        print("No temperature history available")
        return
    
    eET_history = []
    min_len = min(len(result.objective_history), len(result.temperature_history))
    
    for i in range(1, min_len):
        delta_E = result.objective_history[i] - result.objective_history[i-1]
        temperature = result.temperature_history[i]
        
        if temperature > 0:
            eET = np.exp(delta_E / temperature)
        else:
            eET = 0 if delta_E > 0 else 1
        
        eET_history.append(eET)
    
    fig, ax = plt.subplots(3, 1, figsize=(12, 14))
    fig.suptitle(f'Simulated Annealing - e^(ΔE/T) Analysis (Run {run_num})', 
                 fontsize=15, fontweight='bold')
    
    iterations = list(range(1, len(eET_history) + 1))
    
    ax.plot(iterations, eET_history, 'purple', linewidth=2.5, label='e^(ΔE/T)')
    ax.fill_between(iterations, eET_history, alpha=0.3, color='purple')
    ax.axhline(y=1, color='red', linestyle='--', linewidth=1, alpha=0.5, label='Threshold (e^0 = 1)')
    ax.set_xlabel('Iteration', fontsize=12)
    ax.set_ylabel('e^(ΔE/T) Value', fontsize=12)
    ax.set_title('Acceptance Probability Factor e^(ΔE/T) Over Iterations', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    avg_eET = np.mean(eET_history)
    max_eET = max(eET_history)
    min_eET = min(eET_history)
    
    stats_text = f'Average e^(ΔE/T): {avg_eET:.4f}\n'
    stats_text += f'Max e^(ΔE/T): {max_eET:.4f}\n'
    stats_text += f'Min e^(ΔE/T): {min_eET:.4f}'
    
    ax.text(0.02, 0.98, stats_text, transform=ax[0].transAxes,
               fontsize=9, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='plum', alpha=0.7))
    
    plt.tight_layout()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    plots_dir = os.path.join(project_root, 'plots')
    
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    
    filename = f"{timestamp}_Simulated_Annealing_eET_run{run_num}.png"
    save_path = os.path.join(plots_dir, filename)
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.close()


__all__ = [
    'plot_objective_history',
    'plot_genetic_population_fitness',
    'plot_simulated_annealing_eET',
]
