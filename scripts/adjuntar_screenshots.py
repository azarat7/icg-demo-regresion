import os
import sys
import requests
from pathlib import Path
from requests.auth import HTTPBasicAuth

JIRA_EMAIL     = os.environ.get('JIRA_EMAIL', '')
JIRA_API_TOKEN = os.environ.get('JIRA_API_TOKEN', '')
EXECUTION_KEY  = os.environ.get('XRAY_EXECUTION_KEY', '')
BASE_JIRA      = 'https://gticg.atlassian.net/rest/api/3'
CARPETA        = Path('evidencias')

AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

def obtener_issue_id(key):
    r = requests.get(f'{BASE_JIRA}/issue/{key}', auth=AUTH)
    print(f'Status issue lookup: {r.status_code}')
    if r.status_code == 200:
        return r.json().get('id')
    print(f'Respuesta: {r.text[:300]}')
    return None

def adjuntar_archivo(issue_id, archivo, mime_type):
    headers = {'X-Atlassian-Token': 'no-check'}
    with open(archivo, 'rb') as f:
        r = requests.post(
            f'{BASE_JIRA}/issue/{issue_id}/attachments',
            auth=AUTH,
            headers=headers,
            files={'file': (archivo.name, f, mime_type)}
        )
    if r.status_code in (200, 201):
        print(f'  ✅ {archivo.name} adjuntado')
    else:
        print(f'  ❌ {archivo.name} — HTTP {r.status_code}: {r.text[:300]}')
    return r.status_code in (200, 201)

if __name__ == '__main__':
    if not JIRA_EMAIL or not JIRA_API_TOKEN:
        print('⚠️  JIRA_EMAIL o JIRA_API_TOKEN no disponibles')
        sys.exit(0)

    if not EXECUTION_KEY:
        print('⚠️  XRAY_EXECUTION_KEY no disponible')
        sys.exit(0)

    print(f'📎 Adjuntando evidencias a {EXECUTION_KEY}')

    issue_id = obtener_issue_id(EXECUTION_KEY)
    if not issue_id:
        print('❌ No se pudo obtener el ID del issue')
        sys.exit(1)

    videos   = sorted(CARPETA.glob('*.webm'))
    imagenes = sorted(CARPETA.glob('*.png'))

    if not videos and not imagenes:
        print('⚠️  No se encontraron evidencias en evidencias/')
        sys.exit(0)

    print(f'📹 Videos encontrados: {len(videos)}')
    errores = 0
    for vid in videos:
        if not adjuntar_archivo(issue_id, vid, 'video/webm'):
            errores += 1

    print(f'🖼️  Imágenes encontradas: {len(imagenes)}')
    for img in imagenes:
        if not adjuntar_archivo(issue_id, img, 'image/png'):
            errores += 1

    if errores:
        print(f'❌ {errores} archivo(s) no se pudieron adjuntar')
        sys.exit(1)

    print('✅ Todas las evidencias adjuntadas correctamente')