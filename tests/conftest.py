import pytest
import subprocess
import time
import os
from pathlib import Path

# 1. Servidor Local Automático
@pytest.fixture(scope='session', autouse=True)
def servidor_icg():
    ruta = os.path.join(os.path.dirname(__file__), '..', 'sistema-demo')
    ruta = os.path.abspath(ruta)
    
    proc = subprocess.Popen(
        ['python', '-m', 'http.server', '8080', '--directory', ruta],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1)
    yield 'http://localhost:8080'
    proc.terminate()

# 2. Configuración del Navegador (Modo Headless para CI/CD)
@pytest.fixture(scope='session')
def browser_type_launch_args(browser_type_launch_args):
    es_ci = os.environ.get('GITHUB_ACTIONS') == 'true' or os.environ.get('CI') == 'true'
    
    return {
        **browser_type_launch_args,
        "headless": es_ci,
        "slow_mo": 500 if es_ci else 1000
    }

# 3. Configuración de Grabación de Video (1 por test)
@pytest.fixture(scope='function')
def browser_context_args(browser_context_args):
    Path("evidencias").mkdir(exist_ok=True)
    return {
        **browser_context_args,
        "record_video_dir": "evidencias/",
        "record_video_size": {"width": 1280, "height": 720}
    }

# 4. Renombrar Video de forma segura (Esperando al cierre)
@pytest.fixture(scope='function', autouse=True)
def asignar_nombre_video(page, request):
    video = page.video
    nombre_test = request.node.name.replace("[chromium]", "")
    
    yield

    page.context.close()
    
    if video:
        ruta_original = video.path()
        nueva_ruta = os.path.join("evidencias", f"{nombre_test}.webm")
        
        for _ in range(5):
            try:
                if os.path.exists(ruta_original):
                    if os.path.exists(nueva_ruta):
                        os.remove(nueva_ruta)
                    os.rename(ruta_original, nueva_ruta)
                break
            except PermissionError:
                time.sleep(0.5)

# 5. Limpiar nombre del test en JUnit XML (quitar [chromium])
def pytest_collection_modifyitems(items):
    for item in items:
        item._nodeid = item.nodeid.replace("[chromium]", "")