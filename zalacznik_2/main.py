from src import file_support as fs
from src import gemini_api as gapi
from src import data_transformations as dt
import random
import threading

# Wczytaj dane z pliku CSV
data = fs.load_csv('downloaded_posts.csv')
print("Loaded data:", len(data))

# Zawęź dane do określonego zakresu dat
data = dt.narrow_date_range(data, '2017-01-01', '2025-05-15')
print("Date narrowed data:", len(data))

# Wyczyść dane z wartości odstających (outliers)
data = dt.clean_outliers(data)
print("Cleaned outliers data:", len(data))

# Przelicz zaangażowanie i zamień dane na listę
data_as_list = dt.calculate_engagement(data).values.tolist()

import concurrent.futures

# Utwórz blokadę do zapisu do pliku CSV (wielowątkowość)
csv_lock = threading.Lock()

def process_row(index_row):
    index, row = index_row
    # Pobierz ścieżki plików powiązanych z danym folderem/postem
    files_paths = fs.get_file_paths_by_folder_id(row[0])
    print(f"Thread {index+1} classifying post: {row[0]}")
    audio_path = ""
    images = []
    # Rozdziel pliki na obrazy i audio
    for f in files_paths:
        if f.endswith(".mp3"):
            audio_path = f
        elif f.endswith(".jpg"):
            images.append(f)
        else:
            print(f"Unsupported file type: {f}")

    # Wywołaj API Gemini do klasyfikacji posta
    resp_dict = gapi.api_call(
        image_paths=images,
        audio_path=audio_path,
        content_desc=row[5],
        category="zmienna",
    )

    # Przygotuj nowy wiersz do zapisu
    new_row = [
        str(row[0]),
        str(row[1]),
        str(row[2]),
        str(resp_dict.get("odpowiedz", "")).lower(),
        str(row[10]),
    ]
    # Zapisz wiersz do pliku CSV z użyciem blokady
    with csv_lock:
        fs.append_to_csv(new_row, file_name="zmienna_data.csv", variable="Zmienna")

# Przetwarzaj dane równolegle w 5 wątkach
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(process_row, enumerate(data_as_list))
