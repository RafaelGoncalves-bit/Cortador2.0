import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from emailSender import enviarEmail

LINK_SHEETS = "https://docs.google.com/spreadsheets/d/1ktXVa6_N-J9OEYAN_b_gKqs9UA2MZxl1Zelg6SP6dOM"

def disparar_automacao():
    data_selecionada = dataInput.get().strip()
    
    if not data_selecionada:
        messagebox.showwarning("Atenção", "Por favor, insira a data da pasta (ex: 03/2026)")
        return

    try:
        url_csv = LINK_SHEETS.replace('/edit', '/export?format=csv') if "/edit" in LINK_SHEETS else LINK_SHEETS + '/export?format=csv'
        df = pd.read_csv(url_csv)
        
        sucessos = 0
        for _, linha in df.iterrows():
            # Passamos a data como novo parâmetro para o emailSender
            res = enviarEmail(
                str(linha['empresa']), 
                linha['email'], 
                linha['nome'], 
                linha['link'],
                data_selecionada
            )
            if res: sucessos += 1
        
        messagebox.showinfo("Sucesso", f"Processo concluído!\n{sucessos} pastas criadas e e-mails enviados.")

    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"Falha ao processar: {e}")

# --- Interface Gráfica ---
window = tk.Tk()
window.title("Cortador 2.0 - Agille & Melo")
window.geometry("350x250")

# Campo para a Data
ttk.Label(window, text="Digite o Mês/Ano da Pasta:").pack(pady=10)
dataInput = ttk.Entry(window, width=20, justify="center")
dataInput.insert(0, "03-2026") # Valor padrão sugestivo
dataInput.pack(pady=5)

label_info = ttk.Label(window, text="Ao iniciar, o sistema criará uma subpasta\nno Drive de cada colaborador com a data acima.", justify="center")
label_info.pack(pady=15)

botao_start = ttk.Button(window, text="CRIAR PASTAS E ENVIAR", command=disparar_automacao)
botao_start.pack(pady=10)

window.mainloop()