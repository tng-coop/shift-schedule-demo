import random
import numpy
from deap import base, creator, tools, algorithms

# Constants
DAYS = 7
STAFF = 5
SHIFTS = ['M', 'A', 'N']  # Morning, Afternoon, Night
MAX_CONSECUTIVE_WORKING_DAYS = 3
MIN_DAYS_OFF = 2

# Example vacation requests
vacation_requests = {
    0: [0, 1, 5],
    1: [0, 1, 5, 2, 3, 4, 6],
    2: [3],
    # Add more requests as needed
}

# Genetic Algorithm Setup
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Initialize a valid individual
def create_individual():
    individual = []
    for day in range(DAYS):
        daily_schedule = random.sample(range(STAFF), len(SHIFTS))
        individual.extend(daily_schedule)
    return creator.Individual(individual)

toolbox.register("individual", create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Decode individual to a 2D schedule array
def decode_individual(individual):
    schedule = [[None for _ in range(len(SHIFTS))] for _ in range(DAYS)]  # Change here
    for day in range(DAYS):
        day_schedule = individual[day * len(SHIFTS):(day + 1) * len(SHIFTS)]
        for shift_index, staff_id in enumerate(day_schedule):
            schedule[day][shift_index] = staff_id
    return schedule



# Fitness Evaluation
def evaluate(individual):
    schedule = decode_individual(individual)
    penalty = 0

    # Check for proper shift coverage
    for day_schedule in schedule:
        if len(set(day_schedule)) != len(day_schedule):
            penalty += 10  # Major penalty for duplicate shift assignments

    # Check vacation requests and working day constraints
    for staff_id in range(STAFF):
        consecutive_days = 0
        for day, shift in enumerate(schedule):
            if staff_id in shift:
                # Working this day
                if day in vacation_requests.get(staff_id, []):
                    penalty += 5  # Penalize for working on a vacation day
                consecutive_days += 1
                if consecutive_days > MAX_CONSECUTIVE_WORKING_DAYS:
                    penalty += 2 # Penalize for too many consecutive working days
                else:
                    # Not working this day
                    if consecutive_days > 0 and consecutive_days < MIN_DAYS_OFF:
                        penalty += 1 # Penalize for too few consecutive days off
                        consecutive_days = 0 # Reset working day counter
    return penalty,
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(64)
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, stats=stats, halloffame=hof, verbose=True)

    # Print vacation requirements
    print("Vacation Requirements:")
    for staff_id, days_off in vacation_requests.items():
        days_off_str = ", ".join(map(str, days_off))
        print(f"Staff {staff_id} requested days off: {days_off_str}")

    # Decode and print the best schedule found
    best_schedule = decode_individual(hof[0])
    print("\nGenerated Schedule:")
    for day in range(DAYS):
        for shift_index, staff_id in enumerate(best_schedule[day]):
            if shift_index >= len(SHIFTS):
                continue
            print(f"Day {day}, Staff {staff_id}, Shift {SHIFTS[shift_index]}")  # Modified print format

    return pop, log, hof

    
if __name__ == "__main__":
    pop, log, hof = main()

