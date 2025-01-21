import pandas as pd

def get_jumlah_data(file_path):
    """
    Membaca file CSV dan menghitung jumlah data.
    
    Args:
        file_path (str): Path ke file CSV.
    
    Returns:
        int: Jumlah baris dalam file CSV.
    """
    try:
        df = pd.read_csv(file_path)
        return len(df)
    except Exception as e:
        print(f"Error: {e}")
        return 0
