import os
import subprocess
import sys
import yaml
import PySimpleGUI as sg
from time import sleep

LOG = []

def log(msg):
    LOG.append(msg)
    window["log"].update("\n".join(LOG))

def carregar_configuracao(caminho="config/config.yaml"):
    with open(caminho, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def criar_estrutura(nome, estrutura, readme_tpl, gitignore_tpl, usar_gitignore, usar_venv, instalar_req, tipo):
    total_passos = 5
    passo = 0
    sg.one_line_progress_meter("Criando projeto...", passo, total_passos, "criar_proj")

    os.makedirs(nome, exist_ok=True)
    os.chdir(nome)
    passo += 1
    sg.one_line_progress_meter("Criando projeto...", passo, total_passos, "criar_proj")
    log(f"📁 Criando diretórios de {tipo}...")

    for pasta in estrutura.get("diretorios", []):
        os.makedirs(pasta, exist_ok=True)
        log(f"📁 {pasta}")

    for arquivo in estrutura.get("arquivos", []):
        open(arquivo, "a").close()
        log(f"📄 {arquivo}")

    passo += 1
    sg.one_line_progress_meter("Criando projeto...", passo, total_passos, "criar_proj")

    if usar_gitignore:
        with open(".gitignore", "w", encoding="utf-8") as f:
            f.write(gitignore_tpl or "")
        log("✅ .gitignore criado")

    passo += 1
    sg.one_line_progress_meter("Criando projeto...", passo, total_passos, "criar_proj")

    if "README.md" in estrutura.get("arquivos", []):
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_tpl or "# Projeto\n\nDescrição do projeto.")
        log("✅ README.md criado")

    if usar_venv:
        log("⚙️ Criando ambiente virtual...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        log("✅ venv criado")

    passo += 1
    sg.one_line_progress_meter("Criando projeto...", passo, total_passos, "criar_proj")

    if instalar_req and os.path.exists("requirements.txt"):
        log("📦 Instalando pacotes do requirements.txt...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        log("✅ Pacotes instalados")

    sg.one_line_progress_meter("Criando projeto...", total_passos, total_passos, "criar_proj")
    log("🎉 Projeto criado com sucesso!")

def main():
    global window
    config = carregar_configuracao()
    tipos = list(config["estruturas"].keys())

    layout = [
        [sg.Text("Tipo de projeto:"), sg.Combo(tipos, key="tipo", readonly=True)],
        [sg.Text("Nome do projeto:"), sg.Input(key="nome")],
        [sg.Checkbox("Criar .gitignore", default=True, key="git")],
        [sg.Checkbox("Criar venv", default=True, key="venv")],
        [sg.Checkbox("Instalar requirements.txt", default=False, key="req")],
        [sg.Button("Criar Projeto"), sg.Button("Sair")],
        [sg.Multiline("", size=(80, 15), key="log", disabled=True)]
    ]

    window = sg.Window("Criador de Projetos Python", layout, finalize=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Sair"):
            break

        if event == "Criar Projeto":
            LOG.clear()
            window["log"].update("")

            tipo = values["tipo"]
            nome = values["nome"].strip()

            if not tipo or not nome:
                sg.popup_error("Por favor, preencha todos os campos.")
                continue

            estrutura = config["estruturas"][tipo]
            readme_tpl = config.get("templates", {}).get("readme", {}).get(tipo)
            gitignore_tpl = config.get("templates", {}).get("gitignore", {}).get(tipo)

            try:
                criar_estrutura(
                    nome=nome,
                    estrutura=estrutura,
                    readme_tpl=readme_tpl,
                    gitignore_tpl=gitignore_tpl,
                    usar_gitignore=values["git"],
                    usar_venv=values["venv"],
                    instalar_req=values["req"],
                    tipo=tipo
                )
            except Exception as e:
                log(f"❌ Erro: {e}")
                sg.popup_error("Erro ao criar projeto.\nVeja o log para detalhes.")
                continue

            sg.popup("✅ Projeto criado com sucesso!")

    window.close()

if __name__ == "__main__":
    main()
