import pandas as pd
import re
import unicodedata

def limpar_texto(texto):
    texto = str(texto).lower()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto)
                    if unicodedata.category(c) != 'Mn')
    texto = re.sub(r"http\S+|www\S+|https\S+", '', texto)
    texto = re.sub(r"[^a-zA-Z0-9\s]", '', texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

def preprocessar_csv():
    caminho_entrada = "data/dataset_spamfilter.csv"  # arquivo original
    caminho_saida = "data/dataset_limpo.csv"        # arquivo que será salvo

    df = pd.read_csv(caminho_entrada)
    df["label"] = df["label"].map({"golpe": "falsa", "veridico": "veridica"})
    df["clean_text"] = df["message"].apply(limpar_texto)
    df.to_csv(caminho_saida, index=False)
    print(f"CSV limpo salvo em {caminho_saida}")

# 🔹 Chamada da função
preprocessar_csv()
