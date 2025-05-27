import pandas as pd

def calculate_engagement(data):
    # Sprawdzenie, czy dane zawierają wymagane kolumny
    if 'Likes Count' not in data.columns or 'Comments Count' not in data.columns:
        raise ValueError("Data must contain 'Likes Count' and 'Comments Count' columns.")
    # Obliczanie zaangażowania jako suma polubień i 5x liczba komentarzy
    data['Engagement'] = (data['Likes Count'] + 5 * data['Comments Count'])
    return data

def clean_outliers(data):
    # Usuwanie postów z wyłączonymi komentarzami
    data = data[data['Comments Disabled'] == False].copy()
    # Usuwanie postów z zerową liczbą polubień
    data = data[data['Likes Count'] > 0].copy()
    return data

def narrow_date_range(data, start_date, end_date):
    # Konwersja znacznika czasu na datę
    data['date'] = pd.to_datetime(data['Creation Timestamp'], unit='s')
    # Filtrowanie danych w zadanym zakresie dat
    data = data[(data['date'] >= start_date) & (data['date'] <= end_date)].copy()
    return data