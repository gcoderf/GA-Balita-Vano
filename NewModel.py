import pandas as pd

def read_data():
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