import csv

# Fonction pour charger les données
def load_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

# Fonction pour filtrer les années
def filter_years(data, start_season, end_season):
    filtered_data = [row for row in data if start_season <= row['Season'] <= end_season]
    return filtered_data

# Fonction pour compter les occurrences des clubs
def count_clubs(data):
    club_counts = {}
    for row in data:
        club = row['Team']
        if club in club_counts:
            club_counts[club] += 1
        else:
            club_counts[club] = 1
    sorted_clubs = sorted(club_counts.items(), key=lambda x: x[1], reverse=True)
    return [club for club, _ in sorted_clubs[:25]]

# Fonction pour générer le fichier CSV
def generate_csv(data, top_25_clubs, filename):
    final_data = []
    for club in top_25_clubs:
        club_data = [row for row in data if row['Team'] == club]
        points_per_year = {str(year): 0 for year in range(2012, 2023)}
        for row in club_data:
            year = '20' + row['Season'].split('-')[1][-3:]  # Ajustement pour extraire l'année correcte
            points_per_year[str(year)] = int(row['Pts'])
        final_data.append({'Club': club, **points_per_year})
    
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Club'] + [str(year) for year in range(2012, 2023)], delimiter=';')
        writer.writeheader()
        writer.writerows(final_data)

# Exécution de la tâche 1
if __name__ == "__main__":
    file_path = 'EPL_Standings_2000-2022.csv'
    data = load_data(file_path)

    # Filtrage des années de 2012 à 2022
    data_filtered = filter_years(data, '2011-12', '2021-22')

    # Sélection des clubs et comptage des occurrences
    top_25_clubs = count_clubs(data_filtered)

    # Génération du fichier CSV
    nom_fichier = "DARA_GUERI_EPL.csv"
    generate_csv(data_filtered, top_25_clubs, nom_fichier)
    print(f"Fichier genere : {nom_fichier}")
