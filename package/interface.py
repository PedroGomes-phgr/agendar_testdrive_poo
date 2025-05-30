from .bot_agendador import BotAgendador

class Interface:
    def __init__(self, token):
        self.bot = BotAgendador(token)