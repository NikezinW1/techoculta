import os
import requests
import hmac
from flask import Flask, jsonify, request
from urllib.parse import urlparse, urlencode, parse_qsl

app = Flask(__name__)

# Configurações via variáveis de ambiente
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
SECRET_KEY = os.environ.get("SECRET_KEY", "")
AMAZON_TAG = os.environ.get("AMAZON_TAG", "") # Agora puxamos a sua tag do Render!

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

def embutir_tag_amazon(url, tag):
    """Função inteligente que injeta a sua tag de afiliado no link"""
    if not tag or "amazon" not in url.lower():
        return url # Se não tiver tag ou não for da Amazon, retorna normal
        
    parsed = urlparse(url)
    query_params = dict(parse_qsl(parsed.query))
    query_params['tag'] = tag # Sobrescreve ou adiciona a sua tag
    
    new_query = urlencode(query_params)
    return parsed._replace(query=new_query).geturl()

@app.route('/', methods=['GET'])
def index():
    return "Serviço do Bot do Telegram Ativo e Rodando!", 200

@app.route('/keep-alive', methods=['GET'])
def keep_alive():
    return jsonify({"status": "ok"}), 200

# Evoluímos a rota para aceitar POST também, assim você pode integrá-la com n8n/Make no futuro!
@app.route('/disparar-oferta/<key>', methods=['GET', 'POST'])
def disparar_oferta(key):
    # BLINDAGEM: hmac.compare_digest previne "Timing Attacks"
    if not SECRET_KEY or not hmac.compare_digest(key, SECRET_KEY):
        return jsonify({"erro": "Acesso não autorizado."}), 403
        
    # Pega os dados enviados por POST. Se for um GET comum (teste de navegador), usa os dados de placeholder
    dados = request.get_json(silent=True) or {}
    
    produto = dados.get("produto", "Notebook Gamer de Última Geração (TESTE)")
    preco_antigo = dados.get("preco_antigo", "R$ 7.999,00")
    preco_novo = dados.get("preco_novo", "R$ 4.599,00")
    link_original = dados.get("link", "https://www.amazon.com.br/dp/B00EXEMPLO")
    
    # Injeta automaticamente a sua AMAZON_TAG que está no painel do Render
    link_com_tag = embutir_tag_amazon(link_original, AMAZON_TAG)
        
    mensagem_html = (
        "🔥 <b>OFERTA IMPERDÍVEL!</b> 🔥\n\n"
        f"💻 <i>{produto}</i>\n"
        f"💰 <b>De:</b> <s>{preco_antigo}</s>\n"
        f"✅ <b>Por:</b> {preco_novo} à vista\n\n"
        f"🔗 <a href='{link_com_tag}'>Clique aqui para comprar</a>\n\n"
        "⏳ <i>Oferta válida por tempo limitado!</i>"
    )
    
    try:
        resultado = enviar_mensagem_telegram(mensagem_html)
        return jsonify({
            "sucesso": True, 
            "mensagem": "Oferta disparada com sucesso!",
            "link_afiliado_gerado": link_com_tag
        }), 200
        
    except Exception as e:
        print(f"Erro ao enviar oferta: {e}") 
        return jsonify({"erro": "Erro interno no servidor."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
