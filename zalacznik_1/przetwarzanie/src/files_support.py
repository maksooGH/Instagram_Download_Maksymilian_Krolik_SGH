import os
import requests
import pandas as pd

def create_folder(path):
    # Tworzy folder o podanej ścieżce, jeśli nie istnieje
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Folder utworzony pomyślnie: {path}")
    except Exception as e:
        print(f"Wystąpił błąd podczas tworzenia folderu: {e}")

def download_post_file(url, folder_path, file_name=None):
    # Pobiera plik JPG lub MP4 z podanego URL do wskazanego folderu
    try:       
        if file_name is None:
            file_name = url.split("/")[-1]  # Wyodrębnia nazwę pliku z URL
        if '.jpg' not in file_name.lower() and '.mp4' not in file_name.lower():
            print(f"Nieprawidłowy typ pliku dla URL: {url}. Obsługiwane są tylko pliki '.jpg' lub '.mp4'.")
            return
        file_path = os.path.join(folder_path, file_name)
        
        if not os.path.exists(file_path):
            response = requests.get(url, stream=True)
            response.raise_for_status()
                    
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print(f"Plik JPG/MP4 pobrany pomyślnie: {file_path}")
        else:
            print(f"Plik już istnieje: {file_path}")
    except Exception as e:
        print(f"Wystąpił błąd podczas pobierania pliku JPG/MP4: {e}")  

def load_csv(file_name):
    # Ładuje plik CSV i zwraca jego zawartość jako listę
    try:
        file_path = os.path.join(os.path.dirname(__file__), '..', file_name)
        data = pd.read_csv(file_path)
        print(f"Plik CSV załadowany pomyślnie: {file_path}")
        return data.values.tolist() 
    except Exception as e:
        print(f"Wystąpił błąd podczas ładowania pliku CSV: {e}")
        return None