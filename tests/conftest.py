import pytest
import subprocess
import time
import os

@pytest.fixture(scope='session', autouse=True)
def servidor_icg():
    # Encuentra la carpeta 'sistema-demo' subiendo un nivel desde 'tests'
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

@pytest.fixture(scope='session')
def browser_type_launch_args(browser_type_launch_args):
    # CI es una variable que GitHub Actions pone en True automáticamente
    es_ci = os.environ.get('GITHUB_ACTIONS') == 'true' or os.environ.get('CI') is True
    
    return {
        **browser_type_launch_args,
        "headless": es_ci,  # Si es CI, NO levanta ventana. Si es prueba local, SÍ la levanta.
        "slow_mo": 0 if es_ci else 800 # Sin esperas en el pipeline para ir más rápido
    }

