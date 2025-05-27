from enum import Enum
from typing import List
from google import genai
from google.genai import types
import pathlib
import json

# Klucz API do usługi Gemini
GENAI_API_KEY = "KLUCZ_API_GENAI"

# Inicjalizacja klienta Gemini
client = genai.Client(api_key=GENAI_API_KEY)

# Słownik z promptami dla poszczególnych kategorii analizy posta
PromptsDict = {
    "jednostronny": (
        "Czy treść posta stanowi przekaz jednostronny?\n"
        "ODPOWIEDŹ 'TAK' – jeśli post prezentuje wyłącznie jednostronną komunikację, bez zachęty do interakcji.\n"
        "ODPOWIEDŹ 'NIE' – jeśli post zawiera prośbę o wyrażenie opinii przez odbiorców lub bezpośrednie pytanie skierowane do nich.\n"
    ),

    "dialog": (
        "Czy w treści posta znajduje się bezpośrednie pytanie skierowane do odbiorców?\n"
        "ODPOWIEDŹ 'TAK' – jeśli post zawiera wyraźne pytanie do odbiorców.\n"
        "ODPOWIEDŹ 'NIE' – jeśli post nie zawiera takiego pytania.\n"
    ),

    "angazowanie": (
        "Czy post ma na celu aktywizację odbiorców do określonego działania?\n"
        "ODPOWIEDŹ 'TAK' – jeśli post zachęca odbiorców do podjęcia konkretnej aktywności.\n"
        "ODPOWIEDŹ 'NIE' – jeśli post nie zawiera elementów aktywizujących.\n"
    ),

    "wspoltworzenie": (
        "Czy w materiałach wizualnych posta występują studenci SGH?\n"
        "ODPOWIEDŹ 'TAK' – jeśli studenci SGH są jednoznacznie obecni w materiałach.\n"
        "ODPOWIEDŹ 'NIE' – jeśli nie występują lub ich obecność jest jedynie domniemana, bądź występują wyłącznie pracownicy SGH.\n"
    ),
}

# Funkcja zwracająca pełny prompt dla wybranej kategorii
def get_prompt(category: str) -> str:
    FullPrompt = (
        "Jesteś ekspertem w analizie treści postów z mediów społecznościowych. Twoim zadaniem jest przypisać zamieszczonemu postowi dokładnie jedną wartość do ponizszej kategorii.\n"
        "Odpowiadaj na podstawie zmieszczonych danych: opisu posta, klatek z wideo/zdjęć z posta oraz ścieżki audio.\n"
        "Odpowiedz z usasadnieniem (do 500 słów) musi być zapisana w tym formacie JSON:\n"
        '{"uzasadnienie":"...", "odpowiedz":"..."}\n\n'
        f'PYTANIE:\n {PromptsDict[category]}\n'
    )
    return FullPrompt

# Funkcja przygotowująca obrazy do wysłania do API
def prepare_images(image_paths: List[str]) -> List[types.Part]:
    images = []
    for path in image_paths:
        if path.endswith(".jpg"):
            full_path = pathlib.Path(path)
            images.append(types.Part.from_bytes(data=full_path.read_bytes(), mime_type="image/jpeg"))
    return images

# Funkcja przygotowująca plik audio do wysłania do API
def prepare_audio(audio_path: str) -> types.Part:
    if audio_path.endswith(".mp3"):
        full_path = pathlib.Path(audio_path)
        return types.Part.from_bytes(data=full_path.read_bytes(), mime_type="audio/mpeg")
    raise ValueError("Only .mp3 files are supported")

# Funkcja przygotowująca opis posta do wysłania do API
def prepare_description(description: str):
    description_prompt = (
        "Opis treści na Instagramie:\n"
        f"{description}"
    )
    return description_prompt

# Główna funkcja wywołująca API Gemini z przygotowanymi danymi
def api_call(image_paths: List[str], audio_path: str, content_desc: str, category: str) -> str:
    images = prepare_images(image_paths)  # Przygotowanie obrazów
    contents = [
        *images,
    ]
    description = prepare_description(content_desc)  # Przygotowanie opisu
    contents.append(description)
    if audio_path != "":
        audio=prepare_audio(audio_path),
        contents.append(audio)
    
    # Wywołanie modelu Gemini z odpowiednią konfiguracją
    response = client.models.generate_content(
        model='gemini-2.0-flash-lite',
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=get_prompt(category),
            temperature=0.0,
            response_mime_type="application/json"
        ),
    )
    print(response.text)  # Wyświetlenie odpowiedzi modelu
    return json.loads(response.text)  # Zwrócenie odpowiedzi jako słownik Python