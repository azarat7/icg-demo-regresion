import pytest
from pathlib import Path

EVIDENCIAS = Path('evidencias')
EVIDENCIAS.mkdir(exist_ok=True)
BASE = 'http://localhost:8080'

@pytest.mark.xray('PRB-15')   # Descomentar cuando Xray esté activo
def test_PRB_15_login_exitoso_con_credenciales_validas(page):
    # Screenshot 1: Pantalla de login vacía
    page.goto(f'{BASE}/index.html')
    page.screenshot(path=str(EVIDENCIAS / 'PRB15_01_inicio.png'))

    # Screenshot 2: Credenciales ingresadas
    page.fill('#usuario', 'analista@icg.com')
    page.fill('#password', 'Demo2026')
    page.screenshot(path=str(EVIDENCIAS / 'PRB15_02_credenciales.png'))

    # Acción: clic en Ingresar
    page.click('#btn-login')
    page.wait_for_url('**/dashboard.html', timeout=5000)

    # Screenshot 3: Dashboard cargado correctamente
    page.screenshot(path=str(EVIDENCIAS / 'PRB15_03_dashboard.png'))

    assert 'Dashboard' in page.title()