import random
import copy
import time
from typing import Dict, Any
from ..core import Schedule, ObjectiveFunction


class HillClimbingResult:
    """Class to store hill climbing results"""
    def __init__(self):
        self.initial_state = None
        self.final_state = None
        self.initial_value = None
        self.final_value = None
        self.iterations = 0
        self.duration = 0.0
        self.objective_history = []
        self.sideways_moves = 0  # For sideways move variant
        self.restarts = 0  # For random restart variant
        self.iterations_per_restart = []  # For random restart variant


class HillClimbing:
    def __init__(self, data: Dict[str, Any], objective_type: str = 'combined'):
        self.data = data
        self.objective_type = objective_type
        self.objective_func = ObjectiveFunction(data)
    
    def _evaluate(self, schedule: Schedule) -> float:
        """Evaluate objective function (lower is better)"""
        return self.objective_func.calculate(schedule.schedule, self.objective_type)
    
    def steepest_ascent(self) -> HillClimbingResult:
        result = HillClimbingResult()
        start_time = time.time()
        
        current = Schedule(self.data)
        current.initialize_random()
        current_value = self._evaluate(current)
        
        result.initial_state = copy.deepcopy(current.schedule)
        result.initial_value = current_value
        result.objective_history.append(current_value)
        
        iteration = 0
        while True:
            # Get all neighbors
            neighbors = current.get_neighbors()
            
            # Find the best neighbor
            best_neighbor = None
            best_value = current_value
            
            for neighbor in neighbors:
                value = self._evaluate(neighbor)
                if value < best_value:
                    best_value = value
                    best_neighbor = neighbor
            
            if best_neighbor is None:
                break
            
            # Move to best neighbor
            current = best_neighbor
            current_value = best_value
            result.objective_history.append(current_value)
            iteration += 1
        
        result.final_state = current.schedule
        result.final_value = current_value
        result.iterations = iteration
        result.duration = time.time() - start_time
        
        return result
    
    def stochastic(self) -> HillClimbingResult:
        result = HillClimbingResult()
        start_time = time.time()
        
        current = Schedule(self.data)
        current.initialize_random()
        current_value = self._evaluate(current)
        
        result.initial_state = copy.deepcopy(current.schedule)
        result.initial_value = current_value
        result.objective_history.append(current_value)
        
        iteration = 0
        while True:
            # Get all neighbors
            neighbors = current.get_neighbors()
            
            # Find all better neighbors
            better_neighbors = []
            for neighbor in neighbors:
                value = self._evaluate(neighbor)
                if value < current_value:
                    better_neighbors.append((neighbor, value))
            
            if not better_neighbors:
                break
            
            # Randomly select one better neighbor
            selected_neighbor, selected_value = random.choice(better_neighbors)
            
            # Move to selected neighbor
            current = selected_neighbor
            current_value = selected_value
            result.objective_history.append(current_value)
            iteration += 1
        
        result.final_state = current.schedule
        result.final_value = current_value
        result.iterations = iteration
        result.duration = time.time() - start_time
        
        return result
    
    def sideways_move(self, max_sideways: int = 100) -> HillClimbingResult:
        result = HillClimbingResult()
        start_time = time.time()
        
        current = Schedule(self.data)
        current.initialize_random()
        current_value = self._evaluate(current)
        
        result.initial_state = copy.deepcopy(current.schedule)
        result.initial_value = current_value
        result.objective_history.append(current_value)
        
        iteration = 0
        sideways_count = 0
        
        while True:
            # Get all neighbors
            neighbors = current.get_neighbors()
            
            # Find the best neighbor (including equal)
            best_neighbor = None
            best_value = current_value
            is_sideways = False
            
            for neighbor in neighbors:
                value = self._evaluate(neighbor)
                if value < best_value:
                    best_value = value
                    best_neighbor = neighbor
                    is_sideways = False
                elif value == best_value and sideways_count < max_sideways:
                    # Allow sideways move
                    if best_neighbor is None or not is_sideways:
                        best_value = value
                        best_neighbor = neighbor
                        is_sideways = True
            
            if best_neighbor is None:
                break
            
            if is_sideways:
                sideways_count += 1
            else:
                sideways_count = 0 
            
            if sideways_count >= max_sideways:
                break
            
            # Move to best neighbor
            current = best_neighbor
            current_value = best_value
            result.objective_history.append(current_value)
            iteration += 1
        
        result.final_state = current.schedule
        result.final_value = current_value
        result.iterations = iteration
        result.sideways_moves = sideways_count
        result.duration = time.time() - start_time
        
        return result
    
    def random_restart(self, max_restarts: int = 10, 
                       max_iterations_per_restart: int = 100) -> HillClimbingResult:
        result = HillClimbingResult()
        start_time = time.time()
        
        best_overall_state = None
        best_overall_value = float('inf')
        all_objective_history = []
        
        first_schedule = Schedule(self.data)
        first_schedule.initialize_random()
        result.initial_state = copy.deepcopy(first_schedule.schedule)
        result.initial_value = self._evaluate(first_schedule)
        
        for restart in range(max_restarts):
            if restart == 0:
                current = first_schedule
            else:
                current = Schedule(self.data)
                current.initialize_random()
            
            current_value = self._evaluate(current)
            iteration = 0
            
            # Steepest ascent for this restart
            while iteration < max_iterations_per_restart:
                neighbors = current.get_neighbors()
                
                best_neighbor = None
                best_value = current_value
                
                for neighbor in neighbors:
                    value = self._evaluate(neighbor)
                    if value < best_value:
                        best_value = value
                        best_neighbor = neighbor
                
                if best_neighbor is None:
                    break
                
                current = best_neighbor
                current_value = best_value
                all_objective_history.append(current_value)
                iteration += 1
            
            result.iterations_per_restart.append(iteration)
            
            # Update best overall
            if current_value < best_overall_value:
                best_overall_value = current_value
                best_overall_state = current.schedule
        
        result.final_state = best_overall_state
        result.final_value = best_overall_value
        result.restarts = max_restarts
        result.iterations = sum(result.iterations_per_restart)
        result.objective_history = all_objective_history
        result.duration = time.time() - start_time
        
        return result


# Export public API
__all__ = ['HillClimbing', 'HillClimbingResult']