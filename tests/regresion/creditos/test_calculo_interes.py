import pytest
from pathlib import Path

EVIDENCIAS = Path('evidencias')
EVIDENCIAS.mkdir(exist_ok=True)
BASE = 'http://localhost:8080'

@pytest.mark.xray('PRB-16')   #comentario
def test_PRB_16_calculo_interes_simple_retorna_valor_correcto(page):
    page.goto(f'{BASE}/dashboard.html')
    page.screenshot(path=str(EVIDENCIAS / 'PRB16_01_dashboard.png'))

    page.fill('#capital', '10000')
    page.fill('#tasa', '5')
    page.fill('#tiempo', '2')
    page.screenshot(path=str(EVIDENCIAS / 'PRB16_02_datos.png'))

    page.click('button:has-text("Calcular")')
    page.wait_for_timeout(500)
    resultado = page.locator('#res-calculo').text_content()

    page.screenshot(path=str(EVIDENCIAS / 'PRB16_03_resultado.png'))

    # VALIDACION CORRECTA
    assert 'Q 999.00' in resultado, f'Resultado incorrecto: {resultado}'
    page.wait_for_timeout(1000)