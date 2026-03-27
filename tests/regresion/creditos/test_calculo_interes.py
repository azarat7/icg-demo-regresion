import pytest
from pathlib import Path

EVIDENCIAS = Path('evidencias')
EVIDENCIAS.mkdir(exist_ok=True)
BASE = 'http://localhost:8080'

@pytest.mark.xray('PRB-16')   # Descomentar cuando Xray esté activo
def test_PRB_16_calculo_interes_simple_retorna_valor_correcto(page):
    # Screenshot 1: Dashboard inicial
    page.goto(f'{BASE}/dashboard.html')
    page.screenshot(path=str(EVIDENCIAS / 'PRB16_01_dashboard.png'))

    # Ingresar datos: Q10,000 al 5% por 2 años = Q1,000.00
    page.fill('#capital', '10000')
    page.fill('#tasa', '5')
    page.fill('#tiempo', '2')
    page.screenshot(path=str(EVIDENCIAS / 'PRB16_02_datos.png'))

    page.click('button:has-text("Calcular")')
    page.wait_for_timeout(500)
    resultado = page.locator('#res-calculo').text_content()

    # Screenshot 3: Resultado obtenido
    page.screenshot(path=str(EVIDENCIAS / 'PRB16_03_resultado.png'))

    # CORRIDA 1 — FALLA intencional: cambiar 1000.00 por 9999.00
    # CORRIDA 2 — PASS: dejar 1000.00
    assert 'Q 1000.00' in resultado, f'Resultado incorrecto: {resultado}'
    page.wait_for_timeout(1000) 