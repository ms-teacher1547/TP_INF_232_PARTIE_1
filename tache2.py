import csv
import math

# Fonction pour lire le fichier CSV généré
def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        data = [row for row in reader]
    return data

# Fonction pour calculer la moyenne
def mean(data):
    return sum(data) / len(data)

# Fonction pour préparer les données pour la régression linéaire
def prepare_data(data):
    X = []
    y = []
    for row in data:
        y.append(int(row['2022']))
        X.append([int(row[str(year)]) for year in range(2012, 2022)])
    return X, y

# Fonction pour centrer les données
def center_data(data, means):
    centered = []
    for row in data:
        centered_row = [row[i] - means[i] for i in range(len(row))]
        centered.append(centered_row)
    return centered

# Fonction pour transposer une matrice
def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

# Fonction pour multiplier deux matrices
def multiply_matrices(A, B):
    result = [[0] * len(B[0]) for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

# Fonction pour calculer l'inverse d'une matrice 2x2
def inverse_matrix_2x2(matrix):
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if determinant == 0:
        raise ValueError("La matrice n'est pas inversible.")
    return [
        [matrix[1][1] / determinant, -matrix[0][1] / determinant],
        [-matrix[1][0] / determinant, matrix[0][0] / determinant]
    ]

# Fonction pour construire et évaluer le modèle de régression linéaire
def linear_regression(X, y):
    # Calcul des moyennes
    X_mean = [mean(col) for col in transpose(X)]
    y_mean = mean(y)

    # Centrage des données
    X_centered = center_data(X, X_mean)
    y_centered = [yi - y_mean for yi in y]

    # Calcul des coefficients de régression (beta)
    X_centered_T = transpose(X_centered)
    X_centered_T_X_centered = multiply_matrices(X_centered_T, X_centered)
    X_centered_T_y_centered = [sum(X_centered_T[i][j] * y_centered[j] for j in range(len(y_centered))) for i in range(len(X_centered_T))]
    beta = multiply_matrices(inverse_matrix_2x2(X_centered_T_X_centered), [[X_centered_T_y_centered[0]], [X_centered_T_y_centered[1]]])
    beta = [b[0] for b in beta]
    
    # Prédiction
    y_pred = [sum(beta[j] * X_centered[i][j] for j in range(len(beta))) + y_mean for i in range(len(X_centered))]

    # Calcul du coefficient de détermination (R²)
    ss_total = sum((yi - y_mean) ** 2 for yi in y)
    ss_residual = sum((y[i] - y_pred[i]) ** 2 for i in range(len(y)))
    r2 = 1 - (ss_residual / ss_total)
    return r2

# Exécution de la tâche 2
if __name__ == "__main__":
    nom_fichier = "DARA_GUERI_EPL.csv"
    data = read_csv(nom_fichier)

    # Préparation des données pour la régression linéaire
    X, y = prepare_data(data)

    # Construction et évaluation du modèle
    r2 = linear_regression(X, y)
    print(f"Coefficient de determination (R^2) : {r2}")
