import customtkinter as ctk
from tkinter import filedialog
import yaml
import os
import subprocess
import sys

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def carregar_config():
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def selecionar_diretorio():
    pasta = filedialog.askdirectory()
    if pasta:
        nome_var.set(pasta)

def criar_projeto():
    tipo = tipo_var.get()
    caminho = nome_var.get().strip()

    if not caminho:
        status_label.configure(text="⚠️ Diretório do projeto é obrigatório", text_color="red")
        return

    nome_projeto = os.path.basename(caminho)
    os.makedirs(caminho, exist_ok=True)
    os.chdir(caminho)

    estrutura = config["estruturas"][tipo]

    for d in estrutura.get("diretorios", []):
        os.makedirs(d, exist_ok=True)

    for a in estrutura.get("arquivos", []):
        with open(a, "w", encoding="utf-8") as f:
            if a == "README.md":
                f.write(config["templates"]["readme"].get(tipo, ""))
            elif a == ".gitignore":
                f.write(config["templates"]["gitignore"].get(tipo, ""))

    if config["opcionais"].get("criar_venv"):
        subprocess.run([sys.executable, "-m", "venv", "venv"])

    os.chdir("..")
    status_label.configure(text=f"✅ Projeto '{nome_projeto}' criado com sucesso!", text_color="green")

# GUI
config = carregar_config()
janela = ctk.CTk()
janela.title("Criador de Estrutura de Projeto")
janela.geometry("500x270")

ctk.CTkLabel(janela, text="Tipo de projeto").pack(pady=(20, 5))
tipo_var = ctk.StringVar(value=list(config["estruturas"].keys())[0])
ctk.CTkOptionMenu(janela, variable=tipo_var, values=list(config["estruturas"].keys())).pack()

ctk.CTkLabel(janela, text="Pasta onde o projeto será criado").pack(pady=(20, 5))

frame = ctk.CTkFrame(janela)
frame.pack()

nome_var = ctk.StringVar()
ctk.CTkEntry(frame, textvariable=nome_var, width=380).pack(side="left", padx=5)
ctk.CTkButton(frame, text="📁 Procurar", command=selecionar_diretorio).pack(side="left")

ctk.CTkButton(janela, text="Criar Projeto", command=criar_projeto).pack(pady=(30, 10))
status_label = ctk.CTkLabel(janela, text="")
status_label.pack()

janela.mainloop()
