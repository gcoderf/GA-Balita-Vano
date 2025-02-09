import matplotlib.pyplot as plt
import pandas as pd
import random

def plot_fitness_progress(fitness_history):
    plt.plot(range(len(fitness_history)), fitness_history, marker='o', linestyle='-')
    plt.xlabel('Generasi')
    plt.ylabel('Nilai Fitness')
    plt.title('Perkembangan Nilai Fitness pada Setiap Generasi')
    plt.grid(True)
    plt.show()

def generate_meal_plan_with_fitness_tracking(food_data_path, target_calories, target_carbs, target_fat, target_protein, target_fiber):
    food_data = pd.read_csv(food_data_path)
    food_data = food_data.dropna()
    
    # Pastikan semua kolom numerik dikonversi ke float
    numeric_columns = ['energi (kal)', 'karbo (g)', 'lemak (g)', 'protein (g)', 'serat (g)']
    for col in numeric_columns:
        food_data[col] = pd.to_numeric(food_data[col], errors='coerce').fillna(0)
    
    population_size = 15
    num_generations = 100
    chromosome_size = 15
    fitness_history = []
    
    def calculate_fitness(chromosome):
        total_calories, total_carbs, total_fat, total_protein, total_fiber = 0, 0, 0, 0, 0
        for food in chromosome:
            food_info = food_data.loc[food, numeric_columns]
            total_calories += food_info['energi (kal)']
            total_carbs += food_info['karbo (g)']
            total_fat += food_info['lemak (g)']
            total_protein += food_info['protein (g)']
            total_fiber += food_info['serat (g)']
        
        penalty = abs(total_calories - target_calories) + abs(total_carbs - target_carbs) + \
                  abs(total_fat - target_fat) + abs(total_protein - target_protein) + abs(total_fiber - target_fiber)
        return 100 / (1 + penalty)
    
    population = [random.sample(list(food_data.index), chromosome_size) for _ in range(population_size)]
    best_fitness = 0
    best_chromosome = None
    
    for generation in range(num_generations):
        fitness_scores = [calculate_fitness(chromosome) for chromosome in population]
        fitness_history.append(max(fitness_scores))
        
        if max(fitness_scores) > best_fitness:
            best_fitness = max(fitness_scores)
            best_chromosome = population[fitness_scores.index(best_fitness)]
        
        new_population = []
        for _ in range(population_size):
            parent1, parent2 = random.choices(population, weights=fitness_scores, k=2)
            crossover_point = random.randint(0, chromosome_size - 1)
            child = parent1[:crossover_point] + parent2[crossover_point:]
            new_population.append(child)
        
        population = new_population
    
    plot_fitness_progress(fitness_history)
    return best_chromosome, best_fitness

# Contoh penggunaan:
food_data_path = 'bahan_pangan_eliminated.csv'
target_calories = 1400
target_carbs = 0.45 * target_calories
target_fat = 0.35 * target_calories
target_protein = 0.15 * target_calories
target_fiber = 0.05 * target_calories

best_meal_plan, best_fitness = generate_meal_plan_with_fitness_tracking(food_data_path, target_calories, target_carbs, target_fat, target_protein, target_fiber)
print("Rencana Makanan Terbaik:", best_meal_plan)
print("Nilai Fitness Terbaik:", best_fitness)