# scripts/adjuntar_screenshots.py
import os
import requests
from pathlib import Path

TOKEN   = os.environ.get('XRAY_TOKEN', '')
BASE    = 'https://xray.cloud.getxray.app/api/v2'
CARPETA = Path('evidencias')

def obtener_ultima_ejecucion():
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    r = requests.get(
        f'{BASE}/testexecutions?projectKey=PRB3103&limit=1',
        headers=headers
    )
    
    print(f'Status: {r.status_code}')
    print(f'Respuesta: {r.text[:200]}')
    
    if r.status_code != 200 or not r.text.strip():
        print('⚠️ Respuesta vacía o error de autenticación')
        return None
        
    data = r.json()
    if data and len(data) > 0:
        return data[0].get('id')
    return None

def adjuntar_video(ejecucion_id, archivo):
    headers = {'Authorization': f'Bearer {TOKEN}'}
    with open(archivo, 'rb') as f:
        requests.post(
            f'{BASE}/testexecutions/{ejecucion_id}/attachment',
            headers=headers,
            files={'file': (archivo.name, f, 'video/webm')}
        )
    print(f'🎞️ Video adjuntado: {archivo.name}')

if __name__ == '__main__':
    if not TOKEN:
        print('⚠️ XRAY_TOKEN no disponible')
        exit(0)

    eid = obtener_ultima_ejecucion()
    if not eid:
        print('⚠️ No se encontró Test Execution')
        exit(0)
        
    videos = list(CARPETA.glob('*.webm'))
    if not videos:
        print('⚠️ No se encontraron videos en evidencias/')
        exit(0)

    for vid in sorted(videos):
        adjuntar_video(eid, vid)
        
    print('✅ Todos los videos adjuntados en Xray')