import pandas as pd
import random


def calculate_zscore(value, median, sd):
    return (value - median) / sd

# roulle wheel selection
def roulette_wheel_selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual, fitness in zip(population, fitness_scores):
        current += fitness
        if current > pick:
            return individual

# Fungsi untuk mendapatkan informasi makanan
def get_food_info(food, indexes, indexOfChromosome, target_calories, food_data, amount_ratio): 
    nama_bahan = food_data.loc[food, 'nama_bahan']
    kalori = food_data.loc[food, 'energi (kal)']
    amount = 0

    # Encoding Gen
    if indexOfChromosome < 3:
        need = round(0.45 * target_calories)
        amount = need / round(kalori)
    elif indexOfChromosome < 6:
        need = round(0.075 * target_calories)
        amount = need / round(kalori)
    elif indexOfChromosome < 9:
        need = round(0.075 * target_calories)
        amount = need / round(kalori)
    elif indexOfChromosome < 12:
        need = round(0.35 * target_calories)
        amount = need / round(kalori)
    elif indexOfChromosome < 15:
        need = round(0.05 * target_calories)
        amount = need / round(kalori)

    berat_bahan = food_data.loc[food, 'berat (g)'] * amount * amount_ratio
    food_group = food_data.loc[food, 'food_group']
    indexes = indexes[:-1]
    info = [nama_bahan] + [round(berat_bahan, 1)] + [(float(food_data.loc[food, i]) * amount * amount_ratio) for i in indexes] + [food_group]
    return info

# Fungsi untuk menghasilkan rencana makan berdasarkan target
def generate_meal_plan(food_data, target_calories, target_carbs, target_fat, target_protein, target_fiber):
    food_data = pd.read_csv('bahan_pangan_eliminated.csv')
    cols_to_clean = food_data.columns[0:9] 
    food_data[cols_to_clean] = food_data[cols_to_clean].replace(r'\n', '', regex=True)
    food_data['serat (g)'] = food_data['serat (g)'].replace('-', '0')
    food_data = food_data.dropna()

    # Mengelompokkan makanan
    carbs_data = food_data.loc[food_data['food_group'].isin(['serelia', 'umbi'])]
    animal_prot_data = food_data.loc[food_data['food_group'].isin(['ikan', 'daging', 'telur', 'unggas'])]
    plant_prot_data = food_data.loc[food_data['food_group'] == 'kacang']
    fat_data = food_data.loc[food_data['food_group'] == 'lemak']
    fiber_data = food_data.loc[food_data['food_group'].isin(['buah', 'sayuran', 'susu', 'minuman'])]

    population_size = 15
    num_generations = 100
    chromosome_size = 15

    def getAmountOfFood():
        listRandomRatio = [
            [0.38, 0.32, 0.3], [0.29, 0.31, 0.4], [0.35, 0.38, 0.27], 
            [0.45, 0.27, 0.28], [0.32, 0.31, 0.37], [0.29, 0.38, 0.33],
            [0.36, 0.31, 0.33], [0.32, 0.38, 0.3], [0.36, 0.35, 0.29]
        ]
        
        ratioCarbo = random.choice(listRandomRatio)
        ratioProhe = random.choice(listRandomRatio)
        ratioProna = random.choice(listRandomRatio)
        ratioFat = random.choice(listRandomRatio)
        ratioFiber = random.choice(listRandomRatio)
        listAmount = ratioCarbo + ratioProhe + ratioProna + ratioFat + ratioFiber
        return listAmount

    def calculate_fitness(chromosome, target_calories, target_carbs, target_fat, target_protein, target_fiber):
        total_calories = 0
        total_carbs = 0
        total_fat = 0
        total_protein = 0
        total_fiber = 0

        index = 0
        listAmount = getAmountOfFood()
        for food in chromosome:
            amount_ratio = listAmount[index]
            food_info = get_food_info(food, ['energi (kal)', 'karbo (g)', 'lemak (g)', 'protein (g)', 'serat (g)', 'food_group'], index, target_calories, food_data, amount_ratio)
            kalori, karbohidrat, lemak, protein, serat, food_group = food_info[2:]

            total_calories += round(kalori)
            total_carbs += round(karbohidrat)
            total_fat += round(lemak)
            total_protein += round(protein)
            total_fiber += round(serat)
            index += 1

        penalty_calories = abs(total_calories - target_calories)
        penalty_carbs = abs(total_carbs - target_carbs)
        penalty_fat = abs(total_fat - target_fat)
        penalty_protein = abs(total_protein - target_protein)
        penalty_fiber = abs(total_fiber - target_fiber)

        total_penalties = penalty_calories + penalty_carbs + penalty_fat + penalty_protein + penalty_fiber
        fitness = 100 / (1 + total_penalties)

        
        return fitness

    best_fitness = 0
    population = []
    for _ in range(population_size):
        carbs_foods = carbs_data.sample(n=3).index.tolist()
        animal_protein_foods = animal_prot_data.sample(n=3).index.tolist()
        plant_protein_foods = plant_prot_data.sample(n=3).index.tolist()
        fat_foods = fat_data.sample(n=3).index.tolist()
        fiber_foods = fiber_data.sample(n=3).index.tolist()

        chromosome = carbs_foods + animal_protein_foods + plant_protein_foods + fat_foods + fiber_foods
        population.append(chromosome)

    for generation in range(num_generations):
        fitness_scores = [
            calculate_fitness(chromosome, target_calories, target_carbs, target_fat, target_protein, target_fiber)
            for chromosome in population
        ]

        new_population = []
        for _ in range(population_size):
            parent1 = roulette_wheel_selection(population, fitness_scores)
            parent2 = roulette_wheel_selection(population, fitness_scores)

            crossover_rate = 0.8
            if random.random() < crossover_rate:
                crossover_point = random.randint(0, chromosome_size - 1)
                child = parent1[:crossover_point] + parent2[crossover_point:]
            else:
                child = parent1

            mutation_rate = 0.1
            for indexChromosome in range(chromosome_size):
                if random.random() < mutation_rate:
                    if indexChromosome < 3:
                        child[indexChromosome] = random.choice(carbs_data.index.values)
                    elif indexChromosome < 6:
                        child[indexChromosome] = random.choice(animal_prot_data.index.values)
                    elif indexChromosome < 9:
                        child[indexChromosome] = random.choice(plant_prot_data.index.values)
                    elif indexChromosome < 12:
                        child[indexChromosome] = random.choice(fat_data.index.values)
                    else:
                        child[indexChromosome] = random.choice(fiber_data.index.values)

            new_population.append(child)
        population = new_population

    best_chromosome = []
    for chromosome in population:
        fitness = calculate_fitness(chromosome, target_calories, target_carbs, target_fat, target_protein, target_fiber)

        if fitness > best_fitness:
            best_fitness = fitness
            best_chromosome = chromosome

    meal_plan = []
    indexChromosomes = 0
    listAmount = getAmountOfFood()
    for food in best_chromosome:
        amount_ratio = listAmount[indexChromosomes]
        food_info = get_food_info(food, ['energi (kal)', 'karbo (g)', 'lemak (g)', 'protein (g)', 'serat (g)', 'food_group'], indexChromosomes, target_calories, food_data, amount_ratio)
        meal_plan.append(food_info)
        indexChromosomes += 1
    return meal_plan, best_fitness

def final(age, berat_badan, tinggi_badan):
    food_data = pd.read_csv('bahan_pangan_eliminated.csv')

    cols_to_clean = food_data.columns[0:9] 
    food_data[cols_to_clean] = food_data[cols_to_clean].replace(r'\n', '', regex=True)
    food_data['serat (g)'] = food_data['serat (g)'].replace('-', '0')
    food_data = food_data.dropna()

    if age >= 2 and age <= 3: 
        kalori_bayi = 1350  
    elif age >= 4 and age <= 5:
        kalori_bayi = 1400
    else:
        print('Umur yang diinputkan tidak benar')

    if age >= 2 and age <= 3:
        target_calories = kalori_bayi
    elif age >= 4 and age <= 5:
        target_calories = kalori_bayi
    else:
        print('Umur yang diinputkan tidak valid')

    # Reference values based on age
    if age == 2:
        median_bb = 12.2
        sd_bb = 1.2
        median_tb = 86.5
        sd_tb = 3.2
    elif age == 3:
        median_bb = 14.0
        sd_bb = 1.4
        median_tb = 95.1
        sd_tb = 3.8
    elif age == 4:
        median_bb = 15.3
        sd_bb = 1.5
        median_tb = 101.6
        sd_tb = 4.1
    elif age == 5:
        median_bb = 16.2
        sd_bb = 1.6
        median_tb = 107.9
        sd_tb = 4.4
    else:
        return None
    
    # Calculate Z-scores
    zscore_bb = calculate_zscore(berat_badan, median_bb, sd_bb)

    # Interpret Z-scores for BB/U
    if zscore_bb < -3:
        bb_status = "Gizi Buruk"
    elif -3 <= zscore_bb < -2:
        bb_status = "Gizi Kurang"
    elif -2 <= zscore_bb <= 2:
        bb_status = "Gizi Baik"
    else:
        bb_status = "Gizi Lebih"
    
    if bb_status == "Gizi Buruk":
        special_note ="Berikan makanan tinggi kalori dan protein, Porsi kecil tapi sering, Tambahkan minyak atau margarin ke makanan, Prioritaskan protein hewani seperti telur, ikan, daging, Berikan susu formula atau ASI lebih sering"
    elif bb_status == "Gizi Kurang":
        special_note = "Tingkatkan porsi makan secara bertahap, Tambahkan snack bergizi di antara waktu makan, Perbanyak sumber protein dan karbohidrat, Berikan makanan yang kaya vitamin dan mineral, Tambahkan minyak ikan atau zaitun ke makanan"
    elif bb_status == "Gizi Baik":
        special_note = "Pertahankan pola makan yang sehat, Jaga pola makan yang teratur, Perbanyak sumber protein dan karbohidrat, Berikan makanan yang kaya vitamin dan mineral, Tambahkan minyak ikan atau zaitun ke makanan"
    elif bb_status == "Gizi Lebih":
        special_note = "Kurangi porsi makan secara bertahap, Perbanyak aktivitas fisik, Kurangi makanan tinggi kalori dan lemak, Berikan makanan rendah kalori dan lemak, Perbanyak sumber protein dan karbohidrat"
    else:
        special_note = "Tidak ada catatan khusus"



    target_carbs = 0.45 * target_calories  
    target_fat = 0.35 * target_calories  
    target_protein = 0.15 * target_calories  
    target_fiber = 0.05 * target_calories

    meal_plan, best_fitness = generate_meal_plan(food_data, target_calories, target_carbs, target_fat, target_protein, target_fiber)

    num_meals = 3
    meals = [[] for _ in range(num_meals)]

    for i, food in enumerate(meal_plan):
        meal_index = i % num_meals
        meals[meal_index].append(food)

    listDf = []
    for i in meals:
        menu_df = pd.DataFrame(columns=['Nama Bahan', 'Berat (g)', 'Energi (kal)', 'Karbo (g)', 'Lemak (g)', 'Protein (g)', 'Serat (g)', 'Food Group'])
        for j in i:
            menu_df.loc[len(menu_df)] = j
        listDf.append(menu_df)

    listNutritionTarget = [
        round(target_carbs, 1), round(target_fat, 1), 
        round(target_protein, 1), round(target_fiber, 1), 
        round(target_calories, 1)
    ]



    return listDf, listNutritionTarget, best_fitness, bb_status, special_note
