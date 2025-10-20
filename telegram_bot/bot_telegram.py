import joblib
import re
import unicodedata
import numpy as np
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔹 Carregar modelo e vetorizar
model = joblib.load("models/modelo_golpe.pkl")
vectorizer = joblib.load("models/vectorizer_golpe.pkl")

# 🔹 Função de limpeza
def limpar_texto(texto):
    texto = str(texto).lower()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto)
                    if unicodedata.category(c) != 'Mn')
    texto = re.sub(r"http\S+|www\S+|https\S+", '', texto)
    texto = re.sub(r"[^a-zA-Z\s]", '', texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

# 🔹 Função de previsão com confiança
def prever_com_confianca(texto, limiar_indeciso=0.65):
    texto_limpo = limpar_texto(texto)
    texto_vec = vectorizer.transform([texto_limpo])
    probs = model.predict_proba(texto_vec)[0]
    classes = model.classes_
    max_prob = np.max(probs)
    if max_prob < limiar_indeciso:
        return "indeciso", max_prob
    else:
        return classes[np.argmax(probs)], max_prob

# 🔹 Resposta amigável
def gerar_resposta(resultado):
    if resultado == "falsa":
        return "⚠️ Atenção! Essa mensagem parece ser um golpe."
    elif resultado == "veridica":
        return "✅ Essa mensagem parece verídica."
    else:
        return "🤔 Não tenho certeza sobre essa mensagem. Pode ser indecisa."

# 🔹 Handler de mensagens
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = update.message.text.strip().lower()
    
    # Se a mensagem for "oi" ou variação, envia a mensagem de boas-vindas
    if mensagem in ["oi", "olá", "ola", "hello", "hi"]:
        await update.message.reply_text(
            "Olá! Mande uma mensagem e eu direi se é falsa, verídica ou indecisa."
        )
        return
    
    # Caso contrário, classifica normalmente
    resultado, confianca = prever_com_confianca(update.message.text)
    resposta_amigavel = gerar_resposta(resultado)
    resposta_completa = f"{resposta_amigavel} (Confiança: {confianca:.2f})"
    await update.message.reply_text(resposta_completa)

# 🔹 Handler de start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Mande uma mensagem e eu direi se é falsa, verídica ou indecisa."
    )

# 🔹 Criar e rodar o bot
if __name__ == "__main__":
    TOKEN = "8184284628:AAH0yhMSVaAUzEUZ-C-lFdRd0Ar8Z54fOH8"
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    
    print("Bot rodando...")
    app.run_polling()
