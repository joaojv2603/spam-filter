import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib
import numpy as np

# Lê CSV limpo
df = pd.read_csv("data/dataset_limpo.csv")
X_train, X_test, y_train, y_test = train_test_split(
    df["clean_text"], df["label"], test_size=0.2, random_state=42
)

# Vetorização
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Treino
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Avaliação
y_pred = model.predict(X_test_vec)
print("Acurácia:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Salvar modelo e vetorizador
joblib.dump(model, "models/modelo_golpe.pkl")
joblib.dump(vectorizer, "models/vectorizer_golpe.pkl")
print("Modelo e vetorizador salvos!")
