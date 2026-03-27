# scripts/adjuntar_screenshots.py
import os
import requests
from pathlib import Path

TOKEN   = os.environ.get('XRAY_TOKEN', '')
BASE    = 'https://xray.cloud.getxray.app'
CARPETA = Path('evidencias')

def obtener_ultima_ejecucion():
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    # Asegúrate de que el projectKey coincida con tu proyecto de Jira
    r = requests.get(
        f'{BASE}/testexecutions?projectKey=PRB&limit=1', 
        headers=headers
    )
    data = r.json()
    if data and len(data) > 0:
        return data[0].get('id')
    return None

def adjuntar_video(ejecucion_id, archivo):
    headers = {'Authorization': f'Bearer {TOKEN}'}
    with open(archivo, 'rb') as f:
        # Enviamos el archivo con el tipo de contenido correcto para video
        requests.post(
            f'{BASE}/testexecutions/{ejecucion_id}/attachment',
            headers=headers,
            files={'file': (archivo.name, f, 'video/webm')}
        )
    print(f'🎞️ Video adjuntado: {archivo.name}')

if __name__ == '__main__':
    eid = obtener_ultima_ejecucion()
    if not eid:
        print('⚠️ No se encontró Test Execution — Verificar cuando Xray esté activo')
        exit(0)
        
    # Buscamos todos los archivos .webm generados por Playwright
    videos = list(CARPETA.glob('*.webm'))
    if not videos:
        print('⚠️ No se encontraron videos en la carpeta evidencias/')
        exit(0)

    for vid in sorted(videos):
        adjuntar_video(eid, vid)
        
    print('✅ Todos los videos han sido adjuntados en Xray')