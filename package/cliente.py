class Cliente:
    def __init__(self, nome):
        self.nome = nome
        self.agendamentos = []

    def agendar(self, carro, data, horario):
        self.agendamentos.append((carro, data, horario))
