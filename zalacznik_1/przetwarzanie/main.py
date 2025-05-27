from src import files_support as fs
from src import video_compresser as vc

# Wczytaj listę pobranych postów z pliku CSV
downloaded_posts = fs.load_csv('downloaded_posts.csv')

# Przetwarzaj każdy post z listy
for p in downloaded_posts:
    folder_path = f'downloaded/{p[0]}'  # Utwórz ścieżkę folderu na podstawie ID posta
    fs.create_folder(folder_path)        # Utwórz folder, jeśli nie istnieje
    
    if p[1] == 'GraphVideo':
        # Pobierz plik wideo i zapisz jako 'video.mp4'
        fs.download_post_file(p[8], folder_path, 'video.mp4')
        print(f"File loaded successfully: {folder_path}")
        # Skompresuj pobrane wideo
        vc.process_video(folder_path, 'video.mp4')
        print(f"File loaded successfully compressed: {folder_path}")

    elif p[1] == 'GraphImage':
        # Pobierz pojedynczy obraz i zapisz jako '0.jpg'
        fs.download_post_file(p[8], folder_path, '0.jpg')

    elif p[1] == 'GraphSidecar':
        # Pobierz listę obrazów (karuzela zdjęć)
        imgs_list = p[8].split(',')
        for i, x in enumerate(imgs_list):
            fs.download_post_file(x, folder_path, f'{i}.jpg')