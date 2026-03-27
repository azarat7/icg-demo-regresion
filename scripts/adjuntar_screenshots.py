# scripts/adjuntar_screenshots.py
# Se activa cuando se descomenten los steps de Xray en el workflow
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
        f'{BASE}/testexecutions?projectKey=PRB&limit=1',
        headers=headers
    )
    data = r.json()
    if data and len(data) > 0:
        return data[0].get('id')
    return None

def adjuntar_screenshot(ejecucion_id, archivo):
    headers = {'Authorization': f'Bearer {TOKEN}'}
    with open(archivo, 'rb') as f:
        requests.post(
            f'{BASE}/testexecutions/{ejecucion_id}/attachment',
            headers=headers,
            files={'file': (archivo.name, f, 'image/png')}
        )
    print(f'Screenshot adjunto: {archivo.name}')

if __name__ == '__main__':
    eid = obtener_ultima_ejecucion()
    if not eid:
        print('No se encontro Test Execution — verificar cuando Xray este activo')
        exit(0)
    for png in sorted(CARPETA.glob('*.png')):
        adjuntar_screenshot(eid, png)
    print('Todos los screenshots adjuntados en Xray')