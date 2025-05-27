import csv
import os
from src import data_structure as data_struct

def update_downloaded_posts(file_path, downloaded_posts):
    # Sprawdzenie, czy plik istnieje; jeśli nie, utworzenie z nagłówkiem
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Shortcode", "Typename", "Creation Timestamp", "Likes Count", "Comments Count", "Captions", "Comments Disabled", "View Count", "Source Urls"])

    # Dodanie nowych danych do pliku
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        for post in downloaded_posts:
            # Obsługa postów wideo
            if isinstance(post, data_struct.VideoPost):
                writer.writerow([post.shortcode, post.typename, post.creation_timestamp, post.likes, post.comments, post.captions, post.comments_disabled, post.video_view_count, post.video_url])
            # Obsługa postów ze zdjęciem
            elif isinstance(post, data_struct.ImagePost):
                writer.writerow([post.shortcode, post.typename, post.creation_timestamp, post.likes, post.comments, post.captions, post.comments_disabled, "", post.image_url])
            # Obsługa postów typu sidecar (wiele zdjęć/wideo)
            elif isinstance(post, data_struct.SidecarPost):
                writer.writerow([post.shortcode, post.typename, post.creation_timestamp, post.likes, post.comments, post.captions, post.comments_disabled, "", ", ".join(post.sidecar_url_list)])