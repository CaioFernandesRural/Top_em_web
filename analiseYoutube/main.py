import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Substitua 'YOUR_API_KEY' pela sua chave de API do YouTube
API_KEY = 'AIzaSyDyPDn7hs9V06HYhuktd_1emitX5MioGaA'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Função para obter threads de comentários com paginação
def get_comment_threads(video_id, comment_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    next_page_token = None
    body = {'items': []}  # Inicialize como um dicionário com uma chave 'items' que é uma lista
    while True:
        request = youtube.comments().list(
            part='snippet',
            maxResults=100,
            parentId=comment_id,
            pageToken=next_page_token
        )
        response = request.execute()
        
        for item in response['items']:
            # hasComments = item['snippet']['totalReplyCount']
            # if(hasComments):
                # item['comments'] = get_comment_threads(video_id, item['id'])
            body['items'].append(item)    

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break        
    return body    

def get_video_comments(video_id, max_results=5):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    request = youtube.commentThreads().list(
      part="snippet",
      videoId=video_id,
      maxResults=max_results
    )

    body = {'items': []}  # Inicialize como um dicionário com uma chave 'items' que é uma lista
    # Execute the request.
    response = request.execute()
    
    for item in response['items']:
        hasComments = item['snippet']['totalReplyCount']
        if(hasComments):
            item['comments'] = get_comment_threads(video_id, item['id'])
        body['items'].append(item)  
    
    # adicionar os comentários ao body
    while (1 == 1):
        try:
            nextPageToken = response['nextPageToken']
        except KeyError:
            break
        nextPageToken = response['nextPageToken']
        nextRequest = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=100, pageToken=nextPageToken)
        response = nextRequest.execute()
        for item in response['items']:
            hasComments = item['snippet']['totalReplyCount']
            if(hasComments):
                item['comments'] = get_comment_threads(video_id, item['id'])
            body['items'].append(item)  
        
    return body

def get_video_statistics(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    try:
        # Obter estatísticas do vídeo
        response = youtube.videos().list(
            part='contentDetails,id,liveStreamingDetails,localizations,player,recordingDetails,snippet,statistics,status,topicDetails',
            id=video_id
        ).execute()
        return response
    except HttpError as e:
        print(f"Erro HTTP: {e}")
        return None

def save_to_file(data, filename='resultado.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(f"{item}\n")

def save_comments_to_json(comments, filename='comments.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(comments, f, ensure_ascii=False)

if __name__ == "__main__":
    video_id = 'zjBBKgYEd6U'  # Substitua pelo ID do vídeo desejado
    statistics = get_video_statistics(video_id)
    comments = get_video_comments(video_id)
    body = {
        "statistics": statistics,
        "comments": comments
    }    
    filename = video_id+'_estatistica.json'
    save_comments_to_json(body, filename)
    print(f"Comentários salvos em '{filename}'")