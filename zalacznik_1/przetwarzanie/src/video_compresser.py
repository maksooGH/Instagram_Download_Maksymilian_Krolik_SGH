import os
import cv2

import moviepy.editor as mp

def process_video(folder_path, file_name):
    video_path = os.path.join(folder_path, file_name)
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"File {video_path} does not exist.")
    
    # Wyodrębnij audio i zapisz jako audio.mp3
    try:
        audio_output_path = os.path.join(folder_path, "audio.mp3")
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_output_path)
    except Exception as e:
        audio_output_path = None
        print(f"Wystąpił błąd podczas wyodrębniania audio: {e} UWAGA: Wyodrębnianie audio nie powiodło się.")
    
    # Wyodrębnij klatki co 2 sekundy
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_interval = 2 * fps  # odstęp 2 sekundy
    
    frame_count = 0
    saved_frame_count = 0
    success, frame = cap.read()
    
    while success:
        if frame_count % frame_interval == 0:
            frame_path = os.path.join(folder_path, f"{saved_frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            saved_frame_count += 1
        frame_count += 1
        success, frame = cap.read()
    
    cap.release()
    
    # Usuń oryginalny plik mp4
    os.remove(video_path)
    
    print(f"Audio zapisano do {audio_output_path}")
    print(f"Klatki zapisano do {folder_path}")
    print(f"Oryginalny plik wideo {file_name} został usunięty.")
