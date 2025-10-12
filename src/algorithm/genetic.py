import random
import copy
import time
from typing import Dict, Any, List, Tuple
from ..core import Schedule, ObjectiveFunction


class GeneticResult:
    """Class to store genetic algorithm results"""
    def __init__(self):
        self.initial_state = None
        self.final_state = None
        self.initial_value = None
        self.final_value = None
        self.iterations = 0
        self.duration = 0.0
        self.objective_history = []
        self.population_size = 0
        self.best_fitness_history = []
        self.average_fitness_history = []


class GeneticAlgorithm:
    def __init__(self, data: Dict[str, Any], objective_type: str = 'combined'):
        self.data = data
        self.objective_type = objective_type
        self.objective_func = ObjectiveFunction(data)
    
    def _evaluate(self, schedule: Schedule) -> float:
        """Evaluate objective function (lower is better)"""
        return self.objective_func.calculate(schedule.schedule, self.objective_type)
    
    def _create_individual(self) -> Schedule:
        """Create a random individual (schedule)"""
        individual = Schedule(self.data)
        individual.initialize_random()
        return individual
    
    def _initialize_population(self, population_size: int) -> List[Schedule]:
        """Initialize population with random individuals"""
        population = []
        for _ in range(population_size):
            individual = self._create_individual()
            population.append(individual)
        return population
    
    def _selection_roulette(self, population: List[Schedule]) -> Schedule:
        """Roulette wheel selection - probability based on fitness"""
        # Convert to fitness values (higher is better)
        fitness_values = []
        max_penalty = max(self._evaluate(ind) for ind in population) + 1
        
        for individual in population:
            penalty = self._evaluate(individual)
            fitness = max_penalty - penalty  # Convert penalty to fitness
            fitness_values.append(max(fitness, 0.1))  # Ensure positive fitness
        
        total_fitness = sum(fitness_values)
        if total_fitness == 0:
            return copy.deepcopy(random.choice(population))
        
        # Roulette wheel selection
        spin = random.uniform(0, total_fitness)
        current = 0
        
        for i, fitness in enumerate(fitness_values):
            current += fitness
            if current >= spin:
                return copy.deepcopy(population[i])
        
        return copy.deepcopy(population[-1])
    
    def _crossover(self, parent1: Schedule, parent2: Schedule) -> Tuple[Schedule, Schedule]:
        if len(parent1.schedule) <= 1:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)
        
        # Create offspring
        child1 = Schedule(self.data)
        child2 = Schedule(self.data)
        
        crossover_point = random.randint(1, len(parent1.schedule) - 1)
        
        child1.schedule = parent1.schedule[:crossover_point] + parent2.schedule[crossover_point:]
        child2.schedule = parent2.schedule[:crossover_point] + parent1.schedule[crossover_point:]
        
        return child1, child2
    
    def _mutate(self, individual, mutation_rate: float = 0.1) -> Schedule:
        """Mutate an individual with given mutation rate"""
        mutated = copy.deepcopy(individual)
        
        for meeting in mutated.schedule:
            # Only mutate with probability = mutation_rate
            if random.random() < mutation_rate:
                # Randomly change one attribute
                attribute = random.choice(['day', 'start', 'room'])
                
                if attribute == 'day':
                    meeting['day'] = random.choice(mutated.days)
                elif attribute == 'start':
                    max_start = 18 - meeting['duration']
                    if max_start >= 7:
                        meeting['start'] = random.randint(7, max_start)
                elif attribute == 'room':
                    meeting['room'] = random.choice(self.data['ruangan'])['kode']
        
        return mutated
    
    def run(self, population_size: int = 50, max_iterations: int = 100, 
            mutation_rate: float = 0.1) -> GeneticResult:
        """
        Run genetic algorithm with specified parameters
        
        Args:
            population_size: Size of the population
            max_iterations: Maximum number of generations
            mutation_rate: Probability of mutation for each gene (default: 0.1)
        """
        result = GeneticResult()
        start_time = time.time()
        
        # Store parameters
        result.population_size = population_size
        
        # Initialize population
        population = self._initialize_population(population_size)
        
        # Evaluate initial population
        initial_best = min(population, key=lambda x: self._evaluate(x))
        result.initial_state = copy.deepcopy(initial_best.schedule)
        result.initial_value = self._evaluate(initial_best)
        
        # Evolution loop
        for generation in range(max_iterations):
            # Evaluate population
            fitness_values = [self._evaluate(ind) for ind in population]
            best_fitness = min(fitness_values)
            avg_fitness = sum(fitness_values) / len(fitness_values)
            
            # Store statistics
            result.best_fitness_history.append(best_fitness)
            result.average_fitness_history.append(avg_fitness)
            result.objective_history.append(best_fitness)
            
            # Create new generation
            offspring = []
            
            while len(offspring) < population_size:
                # Selection
                parent1 = self._selection_roulette(population)
                parent2 = self._selection_roulette(population)
                
                # Crossover
                child1, child2 = self._crossover(parent1, parent2)
                
                # Mutation
                child1 = self._mutate(child1, mutation_rate)
                child2 = self._mutate(child2, mutation_rate)
                
                offspring.extend([child1, child2])
            
            # Limit offspring to population size
            offspring = offspring[:population_size]
            
            # Replacement
            population = offspring
        
        # Final evaluation
        final_best = min(population, key=lambda x: self._evaluate(x))
        result.final_state = final_best.schedule
        result.final_value = self._evaluate(final_best)
        result.iterations = max_iterations
        result.duration = time.time() - start_time
        
        return result


# Export public API
__all__ = ['GeneticAlgorithm', 'GeneticResult']