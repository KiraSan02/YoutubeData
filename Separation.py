import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Charger les données équilibrées
df = pd.read_csv('balanced_annotated_comments.csv')

# Séparer les features (commentaires) et les labels
X = df['comment']
y = df['label']

# Séparer en jeux d'entraînement et de test (80% entraînement, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

# Définir les métriques d'évaluation
def evaluate_model(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, pos_label='positive')
    recall = recall_score(y_true, y_pred, pos_label='positive')
    f1 = f1_score(y_true, y_pred, pos_label='positive')
    return accuracy, precision, recall, f1
