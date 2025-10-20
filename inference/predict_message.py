import joblib
import re
import unicodedata
import numpy as np

# 1️⃣ Carregar modelo e vetorizar salvos
model = joblib.load("models/modelo_golpe.pkl")
vectorizer = joblib.load("models/vectorizer_golpe.pkl")

# 2️⃣ Função para limpar texto
def limpar_texto(texto):
    texto = str(texto).lower()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto)
                    if unicodedata.category(c) != 'Mn')
    texto = re.sub(r"http\S+|www\S+|https\S+", '', texto)
    texto = re.sub(r"[^a-zA-Z\s]", '', texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

# 3️⃣ Função de previsão
def prever_mensagem(texto, limiar_indeciso=0.6):
    texto_limpo = limpar_texto(texto)
    texto_vec = vectorizer.transform([texto_limpo])
    probs = model.predict_proba(texto_vec)[0]  # probabilidades para cada classe
    classes = model.classes_
    max_prob = np.max(probs)
    
    if max_prob < limiar_indeciso:
        return "indeciso"
    else:
        return classes[np.argmax(probs)]

# 🔹 Teste
mensagem = "Parabéns, você ganhou um prêmio! Clique aqui."
print("Classificação:", prever_mensagem(mensagem))
