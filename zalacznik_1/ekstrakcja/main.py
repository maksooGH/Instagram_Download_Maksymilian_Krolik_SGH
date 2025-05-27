from src import instagram as insta_support
from src import data_structure as data_struct
from src import file_support as file_support

SGH_INSTAGRAM_ID = "1234144800"  # ID Instagrama SGH

head_posts_list = []  # Lista wszystkich pobranych postów
client_session = insta_support.get_tls_session()  # Utworzenie sesji TLS do komunikacji z Instagramem

current_cursor = ""  # Początkowy kursor do paginacji
current_list_count = 12  # Liczba postów pobieranych na raz

# Pętla pobierająca posty dopóki zwracana jest pełna paczka (12 postów)
while current_list_count == 12:
    data = insta_support.get_publications(SGH_INSTAGRAM_ID, current_cursor, 12, client_session)  # Pobranie danych o postach
    current_cursor = data_struct.extract_cursor(data)  # Wyciągnięcie kursora do następnej strony
    posts_list = data_struct.parse_response(data)  # Parsowanie odpowiedzi na listę postów
    current_list_count = len(posts_list)  # Aktualizacja liczby pobranych postów
    head_posts_list += posts_list  # Dodanie nowych postów do głównej listy
    file_support.update_downloaded_posts("downloaded_posts.csv", posts_list)  # Aktualizacja pliku CSV z pobranymi postami
    print(f"Pobrano {len(posts_list)} postów, łącznie: {len(head_posts_list)}")  # Informacja o postępie pobierania
