import os
import re
import subprocess
from datetime import datetime

def formatar_slug(titulo):
    """Gera um slug amigável em kebab-case a partir do título."""
    slug = titulo.lower()
    # Remove caracteres especiais (mantendo espaços e hífens)
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    # Substitui espaços por hífens e remove hífens extras
    slug = re.sub(r'[\s]+', '-', slug).strip('-')
    return slug

def coletar_linhas(prompt_text):
    """Coleta múltiplas linhas curtas de texto (útil para prós e contras)."""
    print(f"\n{prompt_text}")
    print("Digite um item por linha. Para finalizar, digite 'FIM' sozinho em uma linha.")
    linhas = []
    while True:
        try:
            linha = input("- ").strip()
            if linha == "FIM":
                break
            if linha:
                linhas.append(linha)
        except EOFError:
            break
    return linhas

def coletar_conteudo():
    """Coleta o conteúdo multilinhas do artigo até o usuário digitar 'FIM'."""
    print("\n[Cole ou digite o conteúdo do post em Markdown/MDX]")
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
    print("🚀 GERADOR DE POSTS (ASTRO) - NIKEZIN INDICA 🚀")
    print("=" * 60)
    
    # 1. Coleta e Validação Básica
    titulo = input("👉 Título do post (Obrigatório): ").strip()
    if not titulo:
        print("Erro: O título é obrigatório!")
        return
        
    descricao = input("👉 Descrição SEO (Obrigatória): ").strip()
    if not descricao:
        print("Erro: A descrição é obrigatória!")
        return
        
    categoria = input("👉 Categoria (Opcional): ").strip()
    tags_input = input("👉 Tags (separadas por vírgula, Opcional): ").strip()
    
    # 2. Imagem e Validação FÍSICA na pasta assets
    imagem_input = input("👉 Nome da imagem de capa (ex: capa-b450m.jpg) [Deixe em branco para nenhuma]: ").strip()
    if imagem_input:
        caminho_img_check = os.path.join("src", "assets", imagem_input)
        if not os.path.exists(caminho_img_check):
             print(f"Erro de Arquitetura: A imagem '{imagem_input}' não foi encontrada em '{caminho_img_check}'.")
             print("A imagem deve existir na pasta src/assets/ ANTES de rodar este gerador!")
             return
    
    # 3. Prós e Contras
    incluir_pros_contras = input("👉 Deseja adicionar Prós e Contras? (s/n): ").strip().lower()
    pros = []
    cons = []
    if incluir_pros_contras == 's':
        pros = coletar_linhas("👉 Digite os Prós:")
        cons = coletar_linhas("👉 Digite os Contras:")
        
    # 4. Review
    incluir_review = input("👉 Deseja adicionar Sistema de Notas (Review)? (s/n): ").strip().lower()
    review = {}
    if incluir_review == 's':
        try:
            print("\nDeixe em branco para pular os critérios secundários.")
            c_b = input("   Custo-Benefício (0 a 10): ")
            review['custoBeneficio'] = float(c_b) if c_b else -1
            
            des = input("   Desempenho (0 a 10): ")
            review['desempenho'] = float(des) if des else -1
            
            const = input("   Construção (0 a 10): ")
            review['construcao'] = float(const) if const else -1
            
            rec = input("   Recursos (0 a 10): ")
            review['recursos'] = float(rec) if rec else -1
            
            nf = input("   Nota Final (0 a 10) (Obrigatório): ")
            if not nf:
                print("Erro: A Nota Final é obrigatória quando o review é ativado.")
                return
            review['notaFinal'] = float(nf)
        except ValueError:
            print("Erro: As notas devem ser numéricas (use ponto para decimais, ex: 8.5).")
            return
            
    # 5. Processamento Automático e Validação de Slug
    slug = formatar_slug(titulo)
    caminho_arquivo = os.path.join("src", "content", "blog", f"{slug}.mdx")
    
    if os.path.exists(caminho_arquivo):
         print(f"Erro Crítico: O arquivo '{caminho_arquivo}' já existe! Um slug duplicado quebrará o Astro.")
         print("Por favor, escolha outro título ou exclua o artigo antigo.")
         return
         
    # Data SEMPRE real (Garante a Regra de não criar datas retroativas automáticas)
    data_atual = datetime.now().strftime("%b %d %Y")
    tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
    
    # 6. Coleta de Conteúdo
    conteudo = coletar_conteudo()
    
    # 7. Montagem do Frontmatter YAML seguro
    yaml = ["---"]
    # Escapar aspas simples no título e descrição
    t_safe = titulo.replace("'", "''")
    d_safe = descricao.replace("'", "''")
    
    yaml.append(f"title: '{t_safe}'")
    yaml.append(f"description: '{d_safe}'")
    yaml.append(f"pubDate: '{data_atual}'")
    
    if imagem_input:
        yaml.append(f"heroImage: '../../assets/{imagem_input}'")
    
    if categoria:
        yaml.append(f"category: '{categoria}'")
    
    if tags:
        yaml.append("tags:")
        for tag in tags:
            yaml.append(f"  - '{tag}'")
            
    if pros:
        yaml.append("pros:")
        for p in pros:
            # Escapar aspas
            p_safe = p.replace("'", "''")
            yaml.append(f"  - '{p_safe}'")
            
    if cons:
        yaml.append("cons:")
        for c in cons:
            c_safe = c.replace("'", "''")
            yaml.append(f"  - '{c_safe}'")
            
    if incluir_review == 's' and 'notaFinal' in review:
        yaml.append("review:")
        if review['custoBeneficio'] >= 0: yaml.append(f"  custoBeneficio: {review['custoBeneficio']}")
        if review['desempenho'] >= 0: yaml.append(f"  desempenho: {review['desempenho']}")
        if review['construcao'] >= 0: yaml.append(f"  construcao: {review['construcao']}")
        if review['recursos'] >= 0: yaml.append(f"  recursos: {review['recursos']}")
        yaml.append(f"  notaFinal: {review['notaFinal']}")

    yaml.append("---")
    
    conteudo_completo = "\n".join(yaml) + "\n\n" + conteudo
    
    # 8. Criação Física
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo_completo)
        
    print("\n" + "=" * 60)
    print(f"✅ Artigo gerado e salvo com sucesso!")
    print(f"📁 Arquivo criado: {caminho_arquivo}")
    print("=" * 60)
    
    # 9. Verificação Automática (Regra de Validação de Build)
    print("\n🚀 Executando validação e build (npx astro check & astro build)...")
    try:
        # Usa-se ; no PowerShell do Windows ou bash padrão.
        # Estamos executando o npm run build do próprio package.json (que inclui check dependendo da sua preferência, 
        # mas aqui forçamos o check primeiro pra garantir que o Zod Schema aprove o frontmatter)
        comando_validacao = "npx astro check ; npx astro build" if os.name == 'nt' else "npx astro check && npx astro build"
        subprocess.run(comando_validacao, shell=True, check=True, encoding="utf-8")
        print("\n✅ Build e Validação concluídos com sucesso! Nenhum erro de frontmatter ou quebra de tipagem detectada.")
        print("\n👉 Para testar no navegador, rode: npm run dev")
    except subprocess.CalledProcessError as e:
        print("\n❌ ERRO DE ARQUITETURA NO BUILD OU NA VALIDAÇÃO DO ZOD!")
        print("Isso geralmente significa que algum campo no seu Frontmatter não bate com o 'content.config.ts'.")
        print("O arquivo foi salvo, mas você precisa corrigir os erros mostrados acima antes do site funcionar.")

if __name__ == "__main__":
    gerar_post()
