# Projeto de Agendamento de Test Drive

## Descrição do Problema

Este projeto implementa um sistema simples de agendamento de test drive para uma concessionária de carros, com interface gráfica em Tkinter e envio de notificações via Telegram.

---

## Casos de Uso

- O usuário insere seus dados (nome, chat ID do Telegram, data e horário desejados) e seleciona um carro.
- O sistema valida as informações e agenda o test drive.
- Uma mensagem é enviada para o chat ID informado via bot do Telegram confirmando o agendamento.
- O usuário pode fechar a aplicação após o agendamento.

---

## Estrutura do Projeto

- **main.py**: rotina principal que inicia a interface gráfica.
- **package/**: pasta para pacotes do sistema (ainda vazia, mas serve para organizar futuras classes e módulos).
- **README.md**: documentação do projeto.

---

## Modelagem e Conceitos de Orientação a Objetos Aplicados

### Herança

- `BotAgendador` herda da classe base `BotBase`, reaproveitando funcionalidades e sobrescrevendo métodos para personalização (polimorfismo).

### Polimorfismo

- O método `responder` é sobrescrito em `BotAgendador` para responder de forma específica quando a mensagem contém a palavra "agendar".

### Mixins

- A classe `LoggerMixin` adiciona a funcionalidade de logging para as classes que a utilizam, demonstrando reutilização de código via mixins.

### Composição Forte

- A classe `Interface` cria e mantém uma instância do bot (`BotAgendador`), demonstrando composição forte.

### Associação Fraca

- A classe `Sistema` recebe uma instância de bot criada externamente, mostrando associação fraca (uso sem propriedade exclusiva).

---

## Como Rodar o Projeto

1. Instale as dependências:

```bash
pip install python-telegram-bot tkinter

## Autor 

PEDRO HENRIQUE GOMES RODRIGUGES - pedrohgr2005@gmail.com - 241025828(matricula)