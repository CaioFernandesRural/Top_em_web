import pandas as pd
import matplotlib.pyplot as plt
import re

# Função para processar cada linha de mensagem
def process_message(line):
    # Padrão para identificar a data, remetente e mensagem
    pattern = r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - ([^:]+): (.+)'
    match = re.match(pattern, line)
    if match:
        date, sender, message = match.groups()
        return date, sender, message
    return None, None, None

# Função para processar o arquivo
def process_file(file_path):
    messages = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            date, sender, message = process_message(line.strip())
            if date and sender and message:
                messages.append((date, sender, message))
    return pd.DataFrame(messages, columns=['Date', 'Sender', 'Message'])

# Função para agrupar mensagens por data e gerar o gráfico
def plot_messages_over_time(df):
    # Converter a coluna 'Date' para o formato datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M')
    # Agrupar por dia e contar o número de mensagens
    messages_per_day = df.groupby(df['Date'].dt.date).size()

    # Plotar o gráfico linear
    plt.figure(figsize=(10,6))
    plt.plot(messages_per_day.index, messages_per_day.values, marker='o', linestyle='-', color='b')  # Linha contínua
    plt.title('Quantidade de Mensagens ao Longo do Tempo (Gráfico Linear)')
    plt.xlabel('Data')
    plt.ylabel('Número de Mensagens')
    plt.grid(True)  # Adiciona uma grade ao gráfico
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Salvar o gráfico em vez de exibir
    plt.savefig('messages_linear_over_time.png')
    print("Gráfico linear de mensagens ao longo do tempo salvo como 'messages_linear_over_time.png'.")

# Carregar o arquivo e processar
df = process_file('./pav9.txt')

# Gerar o gráfico linear
plot_messages_over_time(df)
