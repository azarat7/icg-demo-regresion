import pytest
from pathlib import Path

EVIDENCIAS = Path('evidencias')
EVIDENCIAS.mkdir(exist_ok=True)
BASE = 'http://localhost:8080'

@pytest.mark.xray('PRB3103-15')
def test_PRB_15_login_exitoso_con_credenciales_validas(page):
    # 1. Ir a la pantalla de login
    page.goto(f'{BASE}/index.html')
    page.wait_for_timeout(1000) # Pausa visual para el video
    page.screenshot(path=str(EVIDENCIAS / 'PRB15_01_inicio.png'))

    # 2. Ingresar credenciales
    page.fill('#usuario', 'analista@icg.com')
    page.fill('#password', 'Demo2026')
    page.wait_for_timeout(1000) # Pausa visual para el video
    page.screenshot(path=str(EVIDENCIAS / 'PRB15_02_credenciales.png'))

    # 3. Clic en Ingresar
    page.click('#btn-login')
    
    # 4. Esperar navegación y validar
    page.wait_for_url('**/dashboard.html', timeout=5000)
    page.screenshot(path=str(EVIDENCIAS / 'PRB15_03_dashboard.png'))
    
    assert 'Dashboard' in page.title()
    
    page.wait_for_timeout(1000) 