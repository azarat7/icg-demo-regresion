import os
import requests
from pathlib import Path
from requests.auth import HTTPBasicAuth

JIRA_EMAIL     = os.environ.get('JIRA_EMAIL', '')
JIRA_API_TOKEN = os.environ.get('JIRA_API_TOKEN', '')
EXECUTION_KEY  = os.environ.get('XRAY_EXECUTION_KEY', '')
BASE_JIRA      = 'https://gticg.atlassian.net/rest/api/2'
CARPETA        = Path('evidencias')

AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

def obtener_issue_id(key):
    r = requests.get(f'{BASE_JIRA}/issue/{key}', auth=AUTH)
    print(f'Status issue lookup: {r.status_code}')
    if r.status_code == 200:
        return r.json().get('id')
    print(f'Respuesta: {r.text[:200]}')
    return None

def adjuntar_video(issue_id, archivo):
    headers = {'X-Atlassian-Token': 'no-check'}
    with open(archivo, 'rb') as f:
        r = requests.post(
            f'{BASE_JIRA}/issue/{issue_id}/attachments',
            auth=AUTH,
            headers=headers,
            files={'file': (archivo.name, f, 'video/webm')}
        )
    print(f'Adjuntado {archivo.name} — status: {r.status_code}')

if __name__ == '__main__':
    if not JIRA_EMAIL or not JIRA_API_TOKEN:
        print('⚠️ JIRA_EMAIL o JIRA_API_TOKEN no disponibles')
        exit(0)

    if not EXECUTION_KEY:
        print('⚠️ XRAY_EXECUTION_KEY no disponible')
        exit(0)

    print(f'Adjuntando evidencias a {EXECUTION_KEY}')

    issue_id = obtener_issue_id(EXECUTION_KEY)
    if not issue_id:
        print('⚠️ No se pudo obtener el ID del issue')
        exit(0)

    videos = list(CARPETA.glob('*.webm'))
    if not videos:
        print('⚠️ No se encontraron videos en evidencias/')
        exit(0)

    for vid in sorted(videos):
        adjuntar_video(issue_id, vid)

    print('✅ Todos los videos adjuntados en Xray')