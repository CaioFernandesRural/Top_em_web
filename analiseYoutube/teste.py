import json
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
    'isso', 'isto', 'este', 'esta', 'estes', 'estas', 'aquele', 'aquela', 'aqueles', 'aquelas', 'mídia', 'oculta',
    'null', 'omitted'
]
CUSTOM_STOPWORDS = [
    'kkk', 'rs', 'vai', 'vem', 'tá', 'po', 'mano', 'tipo', 'pq', 'pô', 'mt', 'ai', 'tbm', 'ah', 'oq', 'eh', 'sim', 'não',
    'kk', 'kkkk', 'acho', 'né', 'só', 'pro', 'vai', 'foi', 'to', 'mais', 'vai', 'tá', 'pq', 'vou', 'aqui', 'essa', 'bom', 
    'era', 'tem', 'vou', 'tá', 'tem', 'pode', 'sempre', 'deve', 'nunca', 'cada', 'todo', 'ser', 'ter', 'pra', 'mas',
    'aí', 'já', 'mensagem apagada', 'dia', 'nem', 'gente', 'até', 'mensagem', 'ainda', 'apagada', 'esse', 'muito', 'tava',
    'quem',
]
STOPWORDS = STOPWORDS + CUSTOM_STOPWORDS

# Função para extrair mensagens do JSON
def extract_text_from_json(json_data):
    messages = []
    
    # Função recursiva para encontrar o campo textOriginal
    def find_text(node):
        if isinstance(node, dict):
            if 'textOriginal' in node:
                messages.append(node['textOriginal'])
            for value in node.values():
                find_text(value)
        elif isinstance(node, list):
            for item in node:
                find_text(item)

    find_text(json_data)
    return messages

# Função para limpar mensagens, removendo stopwords
def clean_message(message):
    message = re.sub(r'\b(k+)\b', 'kkkkk', message, flags=re.IGNORECASE)
    words = re.sub(r'\W+', ' ', message).lower().split()
    cleaned_words = [word for word in words if len(word) > 3 and word not in STOPWORDS]
    return ' '.join(cleaned_words).strip()

# Função para processar as mensagens extraídas
def process_messages(messages):
    cleaned_messages = [clean_message(msg) for msg in messages]
    return pd.DataFrame(cleaned_messages, columns=['Message'])

# Função para gerar wordcloud
def generate_wordcloud(df):
    text = ' '.join(df['Message'])
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(text)
    
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('wordcloud.png')
    print("Nuvem de palavras salva como 'wordcloud.png'.")

def plot_most_common_messages(df, num_messages=20):
    # Contar a frequência das mensagens no DataFrame
    message_counter = Counter(df['Message'])

    # Selecionar as `num_messages` mensagens mais comuns
    most_common_messages = message_counter.most_common(num_messages)

    # Separar as mensagens e suas contagens
    messages, counts = zip(*most_common_messages)

    # Criar o gráfico de barras
    plt.figure(figsize=(12, 8))
    plt.barh(messages, counts, color='skyblue')
    plt.xlabel('Frequência')
    plt.title(f'Top {num_messages} Mensagens Mais Comuns')
    plt.gca().invert_yaxis()  # Inverter a ordem para mostrar a mensagem mais comum no topo
    plt.tight_layout()

    # Salvar o gráfico
    plt.savefig('most_common_messages.png')
    print(f"Gráfico das {num_messages} mensagens mais comuns salvo como 'most_common_messages.png'.")

# Carregar o arquivo JSON
with open('zjBBKgYEd6U_estatistica.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extrair mensagens do JSON
messages = extract_text_from_json(data)

# Processar as mensagens
df = process_messages(messages)

# Exibir as 5 primeiras mensagens processadas
print(df.head())

# Gerar wordcloud
generate_wordcloud(df)

# Exemplo de uso da função
plot_most_common_messages(df)