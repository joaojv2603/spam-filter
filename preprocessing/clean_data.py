import pandas as pd
import re

def limpar_texto(texto):
    texto = str(texto).lower()

    texto = re.sub(r"[^\w\s.,!?@:/%&=-]", '', texto)

    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


def preprocessar_csv():
    caminho_entrada = "data/dataset_spamfilter.csv" 
    caminho_saida = "data/dataset_limpo.csv"

    df = pd.read_csv(caminho_entrada)

    df["label"] = df["label"].map({"golpe": "falsa", "veridico": "veridica"})

    df["clean_text"] = df["message"].apply(limpar_texto)

    df.to_csv(caminho_saida, index=False, encoding="utf-8")
    print(f"? CSV limpo salvo em {caminho_saida}")


if __name__ == "__main__":
    preprocessar_csv()
