import pytest
from pathlib import Path

EVIDENCIAS = Path('evidencias')
EVIDENCIAS.mkdir(exist_ok=True)
BASE = 'http://localhost:8080'

@pytest.mark.xray('PRB3103-41')
def test_PRB3103_41_calculo_interes_simple_retorna_valor_correcto(page):
    page.goto(f'{BASE}/dashboard.html')
    page.screenshot(path=str(EVIDENCIAS / 'PRB3103_01_dashboard.png'))

    page.fill('#capital', '10000')
    page.fill('#tasa', '5')
    page.fill('#tiempo', '2')
    page.screenshot(path=str(EVIDENCIAS / 'PRB3103_02_datos.png'))

    page.click('button:has-text("Calcular")')
    page.wait_for_timeout(500)
    resultado = page.locator('#res-calculo').text_content()

    page.screenshot(path=str(EVIDENCIAS / 'PRB3103_03_resultado.png'))

    # VALIDACION CORRECTA 1000.00 Incorrecta 999.99
    assert 'Q 1000.00' in resultado, f'Resultado incorrecto: {resultado}'
    page.wait_for_timeout(2000)