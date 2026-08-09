import os
import requests
import hmac
from flask import Flask, jsonify

app = Flask(__name__)

# Configurações via variáveis de ambiente
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
SECRET_KEY = os.environ.get("SECRET_KEY", "")

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
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

@app.route('/', methods=['GET'])
def index():
    return "Serviço do Bot do Telegram Ativo e Rodando!", 200

@app.route('/keep-alive', methods=['GET'])
def keep_alive():
    return jsonify({"status": "ok"}), 200

@app.route('/disparar-oferta/<key>', methods=['GET'])
def disparar_oferta(key):
    # BLINDAGEM: hmac.compare_digest previne "Timing Attacks"
    if not SECRET_KEY or not hmac.compare_digest(key, SECRET_KEY):
        # Retorne sempre 403 genérico para não dar pistas ao atacante
        return jsonify({"erro": "Acesso não autorizado."}), 403
        
    mensagem_html = (
        "🔥 <b>OFERTA IMPERDÍVEL!</b> 🔥\n\n"
        "💻 <i>Notebook Gamer de Última Geração</i>\n"
        "💰 <b>De:</b> <s>R$ 7.999,00</s>\n"
        "✅ <b>Por:</b> R$ 4.599,00 à vista\n\n"
        "🔗 <a href='https://exemplo.com/oferta'>Clique aqui para comprar</a>\n\n"
        "⏳ <i>Oferta válida por tempo limitado!</i>"
    )
    
    try:
        resultado = enviar_mensagem_telegram(mensagem_html)
        return jsonify({
            "sucesso": True, 
            "mensagem": "Oferta disparada com sucesso!"
        }), 200
        
    except Exception as e:
        # BLINDAGEM: Não exponha os detalhes do erro interno para o client (Traceback)
        print(f"Erro ao enviar oferta: {e}") 
        return jsonify({"erro": "Erro interno no servidor."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
