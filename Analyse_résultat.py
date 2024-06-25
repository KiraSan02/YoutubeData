import matplotlib.pyplot as plt

# Visualisation des résultats
results_df.plot(kind='bar', figsize=(12, 8))
plt.title('Comparison of Classifiers')
plt.xlabel('Classifier')
plt.ylabel('Score')
plt.xticks(rotation=45)
plt.legend(loc='best')
plt.tight_layout()
plt.show()
