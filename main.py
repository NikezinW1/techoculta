import os
import re
import hmac
import requests
import feedparser
from flask import Flask, jsonify

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
SECRET_KEY = os.environ.get("SECRET_KEY", "")
AMAZON_TAG = os.environ.get("AMAZON_TAG")

def enviar_mensagem_telegram(texto):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        raise ValueError("TELEGRAM_TOKEN e CHAT_ID não configurados.")
        
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erro ao enviar oferta: {e}")
        return {"ok": False, "description": str(e)}

def extrair_asin_amazon(url):
    """Procura o ASIN de 10 dígitos na URL da Amazon."""
    match = re.search(r'/([A-Z0-9]{10})(?:[/?]|$)', url)
    return match.group(1) if match else None

def buscar_oferta_automatica():
    """Lê o feed RSS, filtra pelo nicho e converte o link."""
    # Exemplo usando o feed de informática do Promobit
    url_feed = "https://www.promobit.com.br/rss/informatica"
    try:
        feed = feedparser.parse(url_feed)
    except Exception as e:
        print(f"Erro ao ler feed RSS: {e}")
        return None
    
    # Palavras-chave para filtrar apenas o que nos interessa
    palavras_alvo = ["b450m", "ddr4", "ssd", "monitor", "ryzen", "notebook", "gamer", "nvme"]
    
    for oferta in getattr(feed, 'entries', []):
        titulo = getattr(oferta, 'title', '').lower()
        
        # Verifica se o título tem alguma palavra do nosso nicho
        if any(palavra in titulo for palavra in palavras_alvo):
            link_original = getattr(oferta, 'link', '')
            
            # Se for oferta da Amazon, injeta nossa Tag
            if "amazon" in link_original.lower() and AMAZON_TAG:
                asin = extrair_asin_amazon(link_original)
                if asin:
                    link_final = f"https://www.amazon.com.br/dp/{asin}?tag={AMAZON_TAG}"
                else:
                    link_final = link_original
            else:
                link_final = link_original
            
            mensagem = (
                "🚨 <b>NOVA OFERTA TECH OCULTA</b> 🚨\n\n"
                f"💻 {oferta.title}\n\n"
                f"🛒 <a href='{link_final}'>Acessar Oferta</a>\n\n"
                "⏳ <i>Os preços podem mudar a qualquer momento!</i>"
            )
            return mensagem
            
    return None

@app.route('/')
def home():
    return "Serviço do Bot ativo."

@app.route('/keep-alive')
def keep_alive():
    return jsonify({"status": "ok", "message": "Estou acordado!"})

@app.route('/disparar-oferta/<token>')
def disparar_oferta(token):
    # BLINDAGEM DE SEGURANÇA: Restaurada a proteção contra Timing Attacks usando hmac
    if not SECRET_KEY or not hmac.compare_digest(token, SECRET_KEY):
        return jsonify({"erro": "Não autorizado"}), 403
        
    mensagem = buscar_oferta_automatica()
    
    if mensagem:
        resultado = enviar_mensagem_telegram(mensagem)
        if resultado.get("ok"):
            return jsonify({"status": "sucesso", "mensagem": "Oferta automática postada!"})
        else:
            return jsonify({"status": "erro_telegram", "detalhes": resultado}), 400
    else:
        return jsonify({"status": "aviso", "mensagem": "Nenhuma oferta nova encontrada nos filtros."})

if __name__ == '__main__':
    porta = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=porta)
