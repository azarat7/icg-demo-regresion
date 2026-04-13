import os
import sys
import requests
from pathlib import Path
from requests.auth import HTTPBasicAuth

JIRA_EMAIL      = os.environ.get('JIRA_EMAIL', '')
JIRA_API_TOKEN  = os.environ.get('JIRA_API_TOKEN', '')
EXECUTION_KEY   = os.environ.get('XRAY_EXECUTION_KEY', '')
XRAY_CLIENT_ID  = os.environ.get('XRAY_CLIENT_ID', '')
XRAY_CLIENT_SECRET = os.environ.get('XRAY_CLIENT_SECRET', '')
BASE_JIRA       = 'https://gticg.atlassian.net/rest/api/3'
BASE_XRAY       = 'https://xray.cloud.getxray.app/api/v2'
CARPETA         = Path('evidencias')
TEST_PLAN_KEY   = 'PRB3103-65'

AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

def obtener_xray_token():
    r = requests.post(
        f'{BASE_XRAY}/authenticate',
        json={'client_id': XRAY_CLIENT_ID, 'client_secret': XRAY_CLIENT_SECRET}
    )
    if r.status_code == 200:
        return r.text.strip().strip('"')
    print(f'❌ Error autenticando en Xray — HTTP {r.status_code}: {r.text[:200]}')
    return None

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

def obtener_issue_id_xray(key, token):
    """Obtiene el issueId interno de Xray usando GraphQL"""
    query = f'{{"query":"{{ getTestPlan(issueId: \\"{key}\\") {{ issueId }} }}"}}'
    r = requests.post(
        'https://xray.cloud.getxray.app/api/v2/graphql',
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        data=query
    )
    if r.status_code == 200:
        data = r.json()
        return data.get('data', {}).get('getTestPlan', {}).get('issueId')
    print(f'❌ Error obteniendo ID del Test Plan — HTTP {r.status_code}: {r.text[:200]}')
    return None

def vincular_al_test_plan(token):
    print(f'🔗 Vinculando {EXECUTION_KEY} al Test Plan {TEST_PLAN_KEY}...')

    tp_issue_id = obtener_issue_id_xray(TEST_PLAN_KEY, token)
    te_issue_id = obtener_issue_id_xray(EXECUTION_KEY, token)

    if not tp_issue_id or not te_issue_id:
        print('❌ No se pudieron obtener los IDs internos')
        return

    mutation = f'{{"query":"mutation {{ addTestExecutionsToTestPlan(issueId: \\"{tp_issue_id}\\", testExecIssueIds: [\\"{ te_issue_id}\\"]) {{ addedTestExecutions warning }} }}"}}'
    r = requests.post(
        'https://xray.cloud.getxray.app/api/v2/graphql',
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        data=mutation
    )
    if r.status_code == 200 and 'errors' not in r.json():
        print(f'  ✅ Vinculado correctamente al Test Plan')
    else:
        print(f'  ❌ Error al vincular — HTTP {r.status_code}: {r.text[:300]}')

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

    xray_token = obtener_xray_token()
    if xray_token:
        vincular_al_test_plan(xray_token)

    print('✅ Todas las evidencias adjuntadas correctamente')