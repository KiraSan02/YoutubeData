import pandas as pd
from sklearn.utils import resample

# Charger les commentaires annotés depuis un fichier CSV ou Excel
df = pd.read_csv('annotated_comments.csv')

# Supposons que le fichier annoté ait une colonne 'comment' et une colonne 'label' (positive/negative)

# Supprimer les commentaires neutres si existant
df = df[df['label'] != 'neutral']

# Séparer les commentaires positifs et négatifs
df_positive = df[df['label'] == 'positive']
df_negative = df[df['label'] == 'negative']

# Équilibrer les classes
df_positive_downsampled = resample(df_positive, replace=False, n_samples=len(df_negative), random_state=123)

# Concaténer les deux DataFrames
df_balanced = pd.concat([df_positive_downsampled, df_negative])

# Shuffle les données
df_balanced = df_balanced.sample(frac=1, random_state=123).reset_index(drop=True)

# Sauvegarder les données préparées
df_balanced.to_csv('balanced_annotated_comments.csv', index=False)
