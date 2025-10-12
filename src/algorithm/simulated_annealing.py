import random
import copy
import time
import math
from typing import Dict, Any
from ..core import Schedule, ObjectiveFunction


class SimulatedAnnealingResult:
    """Class untuk menyimpan hasil simulated annealing"""
    def __init__(self):
        self.initial_state = None
        self.final_state = None
        self.initial_value = None
        self.final_value = None
        self.iterations = 0
        self.duration = 0.0
        self.objective_history = []
        self.accepted_moves = 0
        self.rejected_moves = 0
        self.temperature_history = []
        self.initial_temperature = None
        self.final_temperature = None

class SimulatedAnnealing:
    def __init__(self, data: Dict[str, Any], objective_type: str = 'combined'):
        self.data = data
        self.objective_type = objective_type
        self.objective_func = ObjectiveFunction(data)
    
    # Evaluasi dengan fungsi objektif
    def _evaluate(self, schedule: Schedule) -> float:
        return self.objective_func.calculate(schedule.schedule, self.objective_type)
    
    # Pengurangan temperatur secara linear
    def _cooling_schedule_linear(self, initial_temp: float, final_temp: float, current_iteration: int, max_iterations: int) -> float:
        if current_iteration >= max_iterations:
            return final_temp
        return initial_temp - (initial_temp - final_temp) * (current_iteration / max_iterations)
    
    # Pengurangan temperatur secara eksponensial
    def _cooling_schedule_exponential(self, initial_temp: float, alpha: float, current_iteration: int) -> float:
        return initial_temp * (alpha ** current_iteration)
    
    # Pengurangan temperatur secara logaritmik
    def _cooling_schedule_logarithmic(self, initial_temp: float, current_iteration: int) -> float:
        if current_iteration == 0:
            return initial_temp
        return initial_temp / math.log(current_iteration + 1)
    
    # Perhitungan probabilitas move
    def _acceptance_probability(self, current_value: float, neighbor_value: float, temperature: float) -> float:
        if neighbor_value <= current_value:
            return 1.0
        if temperature <= 0:
            return 0.0
        return math.exp(-(neighbor_value - current_value) / temperature)
    
    def run(self, initial_temperature: float = 1000.0, final_temperature: float = 0.1, max_iterations: int = 1000, cooling_schedule: str = 'exponential', alpha: float = 0.95) -> SimulatedAnnealingResult:
        result = SimulatedAnnealingResult()
        start_time = time.time()
        
        # Initialize
        current = Schedule(self.data)
        current.initialize_random()
        current_value = self._evaluate(current)
        
        best = copy.deepcopy(current)
        best_value = current_value
        
        result.initial_state = copy.deepcopy(current.schedule)
        result.initial_value = current_value
        result.initial_temperature = initial_temperature
        result.final_temperature = final_temperature
        result.objective_history.append(current_value)
        
        temperature = initial_temperature
        iteration = 0
        
        while iteration < max_iterations and temperature > final_temperature:
            # Generate random neighbor
            neighbors = current.get_neighbors()
            if not neighbors:
                break
            
            neighbor = random.choice(neighbors)
            neighbor_value = self._evaluate(neighbor)
            
            # Hitung probability move
            accept_prob = self._acceptance_probability(current_value, neighbor_value, temperature)
            
            # terima/tidak move
            if random.random() < accept_prob:
                current = neighbor
                current_value = neighbor_value
                result.accepted_moves += 1
                
                if current_value < best_value:
                    best = copy.deepcopy(current)
                    best_value = current_value
            else:
                result.rejected_moves += 1

            # simpan ke history
            result.objective_history.append(current_value)
            result.temperature_history.append(temperature)
            
            # Update temperature berdasarkan jenis penurunan temp
            if cooling_schedule == 'linear':
                temperature = self._cooling_schedule_linear(initial_temperature, final_temperature, iteration + 1, max_iterations)
            elif cooling_schedule == 'exponential':
                temperature = self._cooling_schedule_exponential(initial_temperature, alpha, iteration + 1)
            elif cooling_schedule == 'logarithmic':
                temperature = self._cooling_schedule_logarithmic(initial_temperature, iteration + 1)
            else:
                raise ValueError(f"Unknown cooling schedule: {cooling_schedule}")
            
            iteration += 1
        
        result.final_state = best.schedule
        result.final_value = best_value
        result.iterations = iteration
        result.duration = time.time() - start_time
        
        return result
    
    # run dengan penurunan temp secara linear
    def run_linear_cooling(self, initial_temperature: float = 1000.0, final_temperature: float = 0.1, max_iterations: int = 1000) -> SimulatedAnnealingResult:
        return self.run(initial_temperature, final_temperature, max_iterations, 'linear')

    # run dengan penurunan temp secara eksponensial
    def run_exponential_cooling(self, initial_temperature: float = 1000.0, alpha: float = 0.95, max_iterations: int = 1000) -> SimulatedAnnealingResult:
        return self.run(initial_temperature, 0.1, max_iterations, 'exponential', alpha)

    # run dengan penurunan temp secara logaritmik
    def run_logarithmic_cooling(self, initial_temperature: float = 1000.0, max_iterations: int = 1000) -> SimulatedAnnealingResult:
        return self.run(initial_temperature, 0.1, max_iterations, 'logarithmic')


# Export public API
__all__ = ['SimulatedAnnealing', 'SimulatedAnnealingResult']
