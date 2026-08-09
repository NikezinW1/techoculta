import os
import re
from datetime import datetime

def formatar_slug(titulo):
    """Gera um slug amigável em kebab-case a partir do título."""
    slug = titulo.lower()
    # Remove caracteres especiais (mantendo espaços e hífens)
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    # Substitui espaços por hífens e remove hífens extras
    slug = re.sub(r'[\s]+', '-', slug).strip('-')
    return slug

def coletar_conteudo():
    """Coleta o conteúdo multilinhas até o usuário digitar 'FIM'."""
    print("\n[Cole ou digite o conteúdo do post em Markdown]")
    print("Para finalizar, digite a palavra 'FIM' sozinha em uma nova linha e aperte Enter.\n")
    
    linhas = []
    while True:
        try:
            linha = input()
            if linha.strip() == "FIM":
                break
            linhas.append(linha)
        except EOFError:
            break
            
    return "\n".join(linhas)

def gerar_post():
    print("=" * 60)
    print("🚀 GERADOR AUTOMÁTICO DE POSTS (ASTRO) - TECH OCULTA 🚀")
    print("=" * 60)
    
    # 1. Coleta interativa de metadados
    titulo = input("👉 Título do post: ").strip()
    if not titulo:
        print("Erro: O título é obrigatório!")
        return
        
    descricao = input("👉 Descrição curta (SEO): ").strip()
    tags_input = input("👉 Tags (separadas por vírgula): ").strip()
    imagem_input = input("👉 Nome da imagem de capa (ex: capa-b450m.jpg) [Pressione Enter para usar o padrão]: ").strip()
    
    
    # 2. Processamento automático
    slug = formatar_slug(titulo)
    # Formato exigido pelo template do Astro: "Aug 08 2026"
    data_atual = datetime.now().strftime("%b %d %Y")
    
    # Formatação das tags para o Frontmatter YAML
    tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
    
    # 3. Entrada do Corpo do Texto
    conteudo = coletar_conteudo()
    
    # 4. Formatação e Injeção
    
    # Definição da Imagem
    caminho_imagem = f"../../assets/{imagem_input}" if imagem_input else "../../assets/blog-placeholder-about.jpg"
    
    # Montagem do Frontmatter
    frontmatter = f"---\ntitle: '{titulo}'\ndescription: '{descricao}'\npubDate: '{data_atual}'\nheroImage: '{caminho_imagem}'"
    
    # Se houver tags, adicionamos no formato de lista YAML
    if tags:
        frontmatter += "\ntags:\n"
        frontmatter += "\n".join([f"  - '{tag}'" for tag in tags])
        
    frontmatter += "\n---\n"

    # Junta as partes
    conteudo_completo = frontmatter + conteudo
    
    # Salvando no diretório nativo do Astro
    pasta_destino = os.path.join("src", "content", "blog")
    os.makedirs(pasta_destino, exist_ok=True)
    
    caminho_arquivo = os.path.join(pasta_destino, f"{slug}.md")
    
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo_completo)
        
    print("\n" + "=" * 60)
    print(f"✅ Post gerado e salvo com sucesso!")
    print(f"📁 Caminho: {caminho_arquivo}")
    
    # Fazendo o push para o GitHub automaticamente para trigar o Deploy
    print("🚀 Sincronizando com o GitHub para deploy automático...")
    
    comando_add = f'git add "{caminho_arquivo}"'
    comando_commit = f'git commit -m "docs(blog): novo artigo - {titulo}"'
    comando_push = 'git push'
    
    os.system(comando_add)
    os.system(comando_commit)
    status_push = os.system(comando_push)
    
    if status_push == 0:
         print("✅ Publicado no GitHub! A Vercel/Render já deve iniciar o build.")
    else:
         print("⚠️ O arquivo foi salvo localmente, mas houve um erro ao enviar para o GitHub.")
         
    print("=" * 60)

if __name__ == "__main__":
    gerar_post()
