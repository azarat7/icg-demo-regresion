import pytest
from pathlib import Path

EVIDENCIAS = Path('evidencias')
EVIDENCIAS.mkdir(exist_ok=True)
BASE = 'http://localhost:8080'

@pytest.mark.xray('PRB3103-17')
def test_PRB_17_total_clientes_visible_en_dashboard(page):
    # Screenshot 1: Login — punto de partida del flujo
    page.goto(f'{BASE}/index.html')
    page.screenshot(path=str(EVIDENCIAS / 'PRB17_01_login.png'))

    # Hacer login para llegar al dashboard
    page.fill('#usuario', 'analista@icg.com')
    page.fill('#password', 'Demo2026')
    page.click('#btn-login')
    page.wait_for_url('**/dashboard.html', timeout=5000)

    # Screenshot 2: Dashboard cargado — card de clientes con boton visible
    page.screenshot(path=str(EVIDENCIAS / 'PRB17_02_dashboard.png'))

    # Clic en Ver detalle para expandir la informacion
    page.click('#btn-ver-detalle')
    page.wait_for_selector('#detalle-clientes', state='visible')

    # Screenshot 3: Detalle expandido — activos, inactivos, nuevos este mes
    page.screenshot(path=str(EVIDENCIAS / 'PRB17_03_detalle.png'))

    # Validaciones
    total = page.locator('#total-clientes').text_content()
    assert '1430' in total, f'Total incorrecto: {total}'
    assert page.locator('#detalle-clientes').is_visible()
    page.wait_for_timeout(1000) 