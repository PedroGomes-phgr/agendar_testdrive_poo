from telegram import Bot

class BotAgendador:
    def __init__(self, token):
        self.bot = Bot(token=token)

    def enviar_mensagem(self, chat_id, texto):
        self.bot.send_message(chat_id=chat_id, text=texto)