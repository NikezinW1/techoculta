import os
import datetime
import re

# ==========================================
# CONFIGURAÇÕES DA POSTAGEM
# ==========================================
NICHO_PRODUTO = "Notebooks Gamer Custo-Benefício 2026"
LINK_TELEGRAM = "https://t.me/seu_grupo_vip"
TAG_AMAZON = "suatag-20"

# ==========================================
# DADOS FAKE (Placeholder Inteligente)
# ==========================================
TITULO_SEO = "Qual o Melhor Notebook Gamer Custo-Benefício em 2026? Acer Nitro, Legion ou Dell G15?"
DESCRICAO = "Descubra qual notebook gamer entrega a melhor performance pelo menor preço. Comparamos os modelos mais buscados: Acer Nitro, Lenovo Legion e Dell G15."

PRODUTO_VENCEDOR = "Lenovo Legion 5i"
LINK_AFILIADO_VENCEDOR = f"https://www.amazon.com.br/dp/B00EXEMPLO/?tag={TAG_AMAZON}"

# Tabela de Comparação
PRODUTOS = [
    {"nome": "Acer Nitro 5", "processador": "Intel Core i5-12450H", "preco": "R$ 4.299,00"},
    {"nome": "Lenovo Legion 5i", "processador": "Intel Core i7-13700H", "preco": "R$ 5.499,00"},
    {"nome": "Dell G15", "processador": "Ryzen 7 6800H", "preco": "R$ 4.899,00"}
]

def formatar_nome_arquivo(titulo):
    """Converte o título para um slug amigável (kebab-case)"""
    slug = titulo.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    return f"{slug}.md"

def gerar_markdown():
    data_atual = datetime.datetime.now().strftime("%b %d %Y")
    
    # Montando a tabela em Markdown
    tabela_md = "| Modelo | Processador / Destaque | Preço Médio |\n"
    tabela_md += "|--------|------------------------|-------------|\n"
    for p in PRODUTOS:
        tabela_md += f"| {p['nome']} | {p['processador']} | {p['preco']} |\n"

    # Montando o conteúdo do arquivo Markdown
    conteudo = f"""---
title: "{TITULO_SEO}"
description: "{DESCRICAO}"
pubDate: "{data_atual}"
heroImage: "/blog-placeholder-about.jpg"
---

Se você está em dúvida sobre qual notebook gamer comprar, nós analisamos as melhores opções do mercado para ajudar na sua decisão. Testamos os modelos mais populares para descobrir qual entrega mais FPS pelo seu dinheiro.

> 🚨 **Atenção!** Os preços de eletrônicos mudam diariamente na Amazon. [Entre no nosso Grupo VIP do Telegram]({LINK_TELEGRAM}) para receber alertas de quedas de preço em tempo real!

## 🏆 A Escolha do Editor

Após extensos testes de temperatura e performance em jogos pesados, nosso grande vencedor é o **{PRODUTO_VENCEDOR}**. 

Ele apresenta o melhor sistema de resfriamento da categoria e garante que sua taxa de quadros não caia no meio da partida.

👉 [**Clique aqui para conferir o {PRODUTO_VENCEDOR} na Amazon com desconto**]({LINK_AFILIADO_VENCEDOR})

## 📊 Comparativo Direto

Aqui está o resumo rápido das principais especificações dos modelos analisados:

{tabela_md}

## Análise Detalhada dos Concorrentes

### 1. Acer Nitro 5
O Acer Nitro continua sendo o rei do orçamento apertado. Embora sua construção seja em plástico, o desempenho térmico surpreende na faixa dos quatro mil reais.

### 2. Dell G15
O Dell G15 é robusto e possui uma tela de excelente qualidade para a categoria, mas é o modelo mais pesado e sua bateria não dura muito longe da tomada.

### 3. Lenovo Legion (O Vencedor)
Construção premium que não parece "gamer demais", ideal para levar ao trabalho ou faculdade. A tela entrega 100% sRGB e as ventoinhas são silenciosas.

---

📢 **Não perca a próxima promoção!**
Notebooks gamers entram em promoção relâmpago constantemente. [Participe do nosso canal no Telegram]({LINK_TELEGRAM}) e não perca a chance de economizar até R$ 1.000 na sua próxima compra!
"""

    # Definir pasta de destino (compatível com a estrutura padrão do template de blog do Astro)
    pasta_destino = os.path.join("src", "content", "blog")
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Criamos um nome fixo baseado no nicho, mas na prática você pode usar o TITULO_SEO
    nome_arquivo = formatar_nome_arquivo("melhor notebook gamer 2026")
    caminho_completo = os.path.join(pasta_destino, nome_arquivo)
    
    with open(caminho_completo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
        
    print(f"✅ Arquivo Markdown gerado com sucesso em: {caminho_completo}")

if __name__ == "__main__":
    gerar_markdown()
