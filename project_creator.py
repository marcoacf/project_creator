import os
import subprocess
import sys
import yaml

def carregar_configuracao(caminho_arquivo="config.yaml"):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def criar_estrutura(nome_projeto, estrutura):
    print(f"\n🔧 Criando estrutura para: {nome_projeto}")
    os.makedirs(nome_projeto, exist_ok=True)
    os.chdir(nome_projeto)

    for pasta in estrutura.get("diretorios", []):
        os.makedirs(pasta, exist_ok=True)
        print(f"📁 Diretório criado: {pasta}")

    for arquivo in estrutura.get("arquivos", []):
        open(arquivo, "a").close()
        print(f"📄 Arquivo criado: {arquivo}")

def criar_gitignore():
    conteudo = """
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
.env
    """
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(conteudo.strip())
    print("✅ .gitignore criado")

def criar_venv(nome="venv"):
    subprocess.run([sys.executable, "-m", "venv", nome])
    print(f"✅ Ambiente virtual '{nome}' criado")

def instalar_requirements():
    if os.path.exists("requirements.txt"):
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("📦 Requisitos instalados")

def criar_readme(template_texto=None):
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(template_texto or "# Projeto\n\nDescrição do projeto.")
    print("✅ README.md criado com template")

def main():
    config = carregar_configuracao()

    print("Tipos de projeto disponíveis:")
    for i, key in enumerate(config["estruturas"], 1):
        print(f"{i}. {key}")

    escolha = int(input("Escolha o tipo de projeto (número): "))
    tipo_escolhido = list(config["estruturas"].keys())[escolha - 1]

    nome_projeto = input("Digite o nome do novo projeto: ").strip()
    estrutura = config["estruturas"][tipo_escolhido]

    criar_estrutura(nome_projeto, estrutura)

    os.chdir(nome_projeto)

    if config["opcionais"].get("criar_gitignore"):
        criar_gitignore()

    if config["opcionais"].get("criar_venv"):
        criar_venv()

    if config["opcionais"].get("instalar_requisitos"):
        instalar_requirements()

    template_readme = config.get("templates", {}).get("readme", {}).get(tipo_escolhido)
    if "README.md" in estrutura.get("arquivos", []):
        criar_readme(template_readme)

    print("\n🎉 Projeto criado com sucesso!")

if __name__ == "__main__":
    main()
