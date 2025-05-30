import tkinter as tk
from tkinter import messagebox, font
from telegram import Bot
from package.cliente import Cliente
from package.carro import Carro
from package.bot_agendador import BotAgendador


# ----- CONFIGURAÇÕES -----
TOKEN = "8083323084:AAHXRyt6sAPg7CxrqYpDV0v6ttHvFBdTylw"

# ----- MIXIN PARA LOG -----
class LoggerMixin:
    def log(self, msg):
        print(f"[LOG] {msg}")

# ----- CLASSE BASE DO BOT -----
class BotBase(LoggerMixin):
    def __init__(self, token):
        self.bot = Bot(token=token)

    def enviar_mensagem(self, chat_id, texto):
        self.log(f"Enviando mensagem para {chat_id}: {texto}")
        self.bot.send_message(chat_id=chat_id, text=texto)

    def responder(self, msg):
        return "Resposta padrão do bot"

# ----- BOT AGENDADOR QUE HERDA BOTBASE (HERANÇA + POLIMORFISMO) -----
class BotAgendador(BotBase):
    def responder(self, msg):
        if "agendar" in msg.lower():
            return "Claro! Por favor, informe seu nome, data e horário para agendar."
        return super().responder(msg)

# ----- CLASSES DE DOMÍNIO -----
class Carro:
    def __init__(self, modelo, ano, preco):
        self.modelo = modelo
        self.ano = ano
        self.preco = preco

class Cliente:
    def __init__(self, nome):
        self.nome = nome
        self.agendamentos = []

    def agendar(self, carro, data, horario):
        self.agendamentos.append((carro, data, horario))

# ----- SISTEMA COM ASSOCIAÇÃO FRACA AO BOT -----
class Sistema:
    def __init__(self, bot):
        self.bot = bot  # associação fraca: recebe o bot, não cria

    def processar_mensagem(self, chat_id, msg):
        resposta = self.bot.responder(msg)
        self.bot.enviar_mensagem(chat_id, resposta)

# ----- INTERFACE GRÁFICA (COMPOSIÇÃO FORTE DO BOT) -----
class Interface:
    def __init__(self):
        self.bot = BotAgendador(TOKEN)  # composição forte: cria o bot
        self.sistema = Sistema(self.bot)  # passa o bot para o sistema (associação fraca)

        self.cliente = Cliente("Usuário")
        self.carros = [
            Carro("HB20", 2023, 75000),
            Carro("Creta", 2024, 120000),
            Carro("Onix", 2022, 68000)
        ]

        self.configurar_interface()

    def configurar_interface(self):
        self.janela = tk.Tk()
        self.janela.title("Agendamento de Test Drive")
        self.janela.geometry("800x650")
        self.janela.configure(bg="#2e2e2e")

        label_font = font.Font(family="Segoe UI", size=12)
        entry_font = font.Font(family="Segoe UI", size=11)

        fg_color = "#FFFFFF"
        entry_bg = "#3c3f41"
        entry_fg = "#e0e0e0"
        button_bg = "#4caf50"
        button_fg = "#FFFFFF"

        campos = [
            ("Nome do Cliente:", 'entry_nome'),
            ("Chat ID:", 'entry_chat_id'),
            ("Data (dd/mm/aaaa):", 'entry_data'),
            ("Horário (hh:mm):", 'entry_horario')
        ]

        self.entries = {}
        for label_text, var_name in campos:
            tk.Label(self.janela, text=label_text, font=label_font, bg="#2e2e2e", fg=fg_color).pack(pady=(10, 0))
            entry = tk.Entry(self.janela, font=entry_font, width=45, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
            entry.pack(pady=5)
            self.entries[var_name] = entry

        self.entry_nome = self.entries['entry_nome']
        self.entry_chat_id = self.entries['entry_chat_id']
        self.entry_data = self.entries['entry_data']
        self.entry_horario = self.entries['entry_horario']

        self.entry_data.bind("<KeyRelease>", self.mascara_data)
        self.entry_horario.bind("<KeyRelease>", self.mascara_horario)

        tk.Label(self.janela, text="Escolha um carro:", font=label_font, bg="#2e2e2e", fg=fg_color).pack(pady=(20, 0))
        self.lista_carros = tk.Listbox(self.janela, width=60, height=8, font=entry_font, bg=entry_bg, fg=entry_fg,
                                      selectbackground="#6a95ff", selectforeground="#fff")
        self.lista_carros.pack(pady=10)
        for carro in self.carros:
            self.lista_carros.insert(tk.END, f"{carro.modelo} ({carro.ano}) - R$ {carro.preco}")

        tk.Button(self.janela, text="Agendar Test Drive",
                  font=font.Font(family="Segoe UI", size=14, weight="bold"),
                  bg=button_bg, fg=button_fg, activebackground="#45a049",
                  activeforeground=button_fg, width=30, height=2,
                  command=self.agendar_testdrive).pack(pady=15)

        self.label_result = tk.Label(self.janela, text="", font=font.Font(family="Segoe UI", size=13), bg="#2e2e2e", fg=fg_color)
        self.label_result.pack(pady=10)

        self.janela.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.janela.mainloop()

    # --- Máscaras para entrada ---
    def mascara_data(self, event):
        texto = self.entry_data.get().replace('/', '')
        novo = ''
        for i, c in enumerate(texto):
            if i in [2, 4]:
                novo += '/'
            novo += c
            if len(novo) >= 10:
                break
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, novo)

    def mascara_horario(self, event):
        texto = self.entry_horario.get().replace(':', '')
        novo = ''
        for i, c in enumerate(texto):
            if i == 2:
                novo += ':'
            novo += c
            if len(novo) >= 5:
                break
        self.entry_horario.delete(0, tk.END)
        self.entry_horario.insert(0, novo)

    # --- Método para agendar o test drive ---
    def agendar_testdrive(self):
        nome_cliente = self.entry_nome.get().strip()
        chat_id_input = self.entry_chat_id.get().strip()
        data = self.entry_data.get().strip()
        horario = self.entry_horario.get().strip()
        selecionado = self.lista_carros.curselection()

        # Validações
        if not nome_cliente:
            messagebox.showwarning("Aviso", "Digite o nome do cliente.")
            return
        if not chat_id_input.isdigit():
            messagebox.showwarning("Aviso", "Chat ID inválido. Digite só números.")
            return
        if len(data) != 10:
            messagebox.showwarning("Aviso", "Data inválida. Use o formato dd/mm/aaaa.")
            return
        if len(horario) != 5:
            messagebox.showwarning("Aviso", "Horário inválido. Use o formato hh:mm.")
            return
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um carro para agendar.")
            return

        carro = self.carros[selecionado[0]]
        self.cliente.nome = nome_cliente
        self.cliente.agendar(carro, data, horario)

        texto = f"{self.cliente.nome} agendou um test drive para o carro {carro.modelo} ({carro.ano}) - R$ {carro.preco}\nData: {data} Horário: {horario}"
        
        try:
            self.bot.enviar_mensagem(chat_id_input, texto)  # Usando o método do bot com log
            messagebox.showinfo("Sucesso", "Test drive agendado com sucesso!")
            self.janela.destroy()
        except Exception as e:
            self.label_result.config(text=f"Erro ao enviar mensagem: {e}", fg="#FF5555")

    def on_closing(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.janela.destroy()

# --- RODA A INTERFACE ---
if __name__ == "__main__":
    Interface()
