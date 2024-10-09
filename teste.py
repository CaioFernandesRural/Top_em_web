import re
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

# Lista de stopwords em português (preposições, pronomes, etc.)
STOPWORDS = [
    'a', 'o', 'e', 'de', 'do', 'da', 'em', 'para', 'com', 'se', 'por', 'na', 'no', 'os', 'as',
    'um', 'uma', 'uns', 'umas', 'que', 'é', 'foi', 'tem', 'ser', 'não', 'sim', 'como', 'ele', 'ela', 
    'você', 'eles', 'elas', 'nos', 'nós', 'eu', 'me', 'te', 'tu', 'lhe', 'minha', 'meu', 'sua', 'seu',
    'isso', 'isto', 'este', 'esta', 'estes', 'estas', 'aquele', 'aquela', 'aqueles', 'aquelas', 'mídia', 'oculta'
]


# Função para processar cada linha de mensagem
def process_message(line):
    # Padrão atualizado para suportar mensagens de criação de grupo, entrada e saída
    pattern = r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - ([^:]+): (.+)'
    match = re.match(pattern, line)
    if match:
        date, sender, message = match.groups()
        return date, sender, clean_message(message)  # Limpa a mensagem antes de retornar
    return None, None, None

# Função para limpar mensagens, removendo stopwords
def clean_message(message):
    # Substituir caracteres não alfanuméricos por espaço e converter para minúsculas
    words = re.sub(r'\W+', ' ', message).lower().split()
    # Remove palavras com menos de 2 caracteres e stopwords
    cleaned_words = [word for word in words if len(word) > 2 and word not in STOPWORDS]
    return ' '.join(cleaned_words).strip()


# Função para processar o arquivo
def process_file(file_path):
    messages = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            date, sender, message = process_message(line.strip())
            if date and sender and message:
                messages.append((date, sender, message))
    return pd.DataFrame(messages, columns=['Date', 'Sender', 'Message'])

# Função para contar mensagens por remetente
def count_messages_by_sender(df):
    return df['Sender'].value_counts()

# Função para contagem de palavras
def get_most_common_words(df, num_words=10):
    words = ' '.join(df['Message']).lower().split()
    counter = Counter(words)
    return counter.most_common(num_words)

# Função para gerar um gráfico de participação
def plot_message_distribution(df):
    message_counts = count_messages_by_sender(df)
    if message_counts.empty:
        print("Nenhuma mensagem para plotar.")
        return
    plt.figure(figsize=(10,6))
    message_counts.plot(kind='bar')
    plt.title('Distribuição de Mensagens por Participante')
    plt.ylabel('Número de Mensagens')
    plt.xlabel('Participantes')
    plt.xticks(rotation=45)
    # Salvar o gráfico em vez de exibir
    plt.savefig('message_distribution.png')  
    print("Gráfico de distribuição de mensagens salvo como 'message_distribution.png'.")

# Função para gerar uma wordcloud (nuvem de palavras)
def generate_wordcloud(df):
    text = ' '.join(df['Message'])
    # Adicione suas stopwords personalizadas à lista de stopwords do WordCloud
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(text)
    
    plt.figure(figsize=(10,6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    # Salvar o gráfico em vez de exibir
    plt.savefig('wordcloud.png')  
    print("Nuvem de palavras salva como 'wordcloud.png'.")

# Carregando o arquivo e processando
df = process_file('./amostra.txt')

# Exibir as 5 primeiras mensagens processadas
print(df.head())

# Contagem de mensagens por remetente
print(count_messages_by_sender(df))

# Gerar gráfico de distribuição de mensagens por participante
plot_message_distribution(df)

# Exibir as 10 palavras mais comuns
print(get_most_common_words(df, 10))

# Gerar wordcloud
generate_wordcloud(df)
