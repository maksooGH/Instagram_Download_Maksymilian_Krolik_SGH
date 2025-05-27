import os
import pandas as pd

# Ścieżka do pobranych treści (należy podmienić na właściwą)
posts_data_path = "SCIEZKA_DO_POBRANYCH_TRESCI"

def load_csv(file_name):
    # Ładuje plik CSV do DataFrame
    try:
        file_path = os.path.join(os.path.dirname(__file__), '..', file_name)
        data = pd.read_csv(file_path)
        print(f"CSV file loaded successfully: {file_path}")
        return data 
    except Exception as e:
        print(f"An error occurred while loading the CSV file: {e}")
        return None
    
def get_file_paths_by_folder_id(folder_id):
    # Zwraca listę ścieżek do plików w folderze o podanym ID
    try:
        folder_path = os.path.join(posts_data_path, folder_id)
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder with ID {folder_id} does not exist.")
            
        file_paths = [
            os.path.join(folder_path, file_name)
            for file_name in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, file_name))
        ]
        return file_paths
    except Exception as e:
        print(f"An error occurred while retrieving file paths: {e}")
        return []
    
def append_to_csv(row_data, file_name="classified_data.csv", variable=""):
    # Dodaje nowy wiersz do pliku CSV, tworzy plik jeśli nie istnieje
    try:
        file_path = os.path.join(os.path.dirname(__file__), '..', file_name)
        
        if not os.path.exists(file_path):
            # Tworzy plik z nagłówkami, jeśli nie istnieje
            headers = ["ID", "Format Treści", "Data (Timestamp)", variable, "Poziom Zaangazowania"]
            with open(file_path, 'w') as f:
                f.write(','.join(headers) + '\n')
            print(f"File created with headers: {file_path}")
        
        with open(file_path, 'a') as f:
            f.write(','.join(map(str, row_data)) + '\n')

        print(f"Row appended successfully to: {file_path}")
    except Exception as e:
        print(f"An error occurred while appending to the CSV file: {e}")    
