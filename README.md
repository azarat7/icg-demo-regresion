# 🚀 Proyecto de demostración para las pruebas de Regresión Automatizacidas ICG

Este repositorio contiene la suite de pruebas automatizadas para el sistema ICG, desarrollada con **Python 3.12** y **Playwright**.

## 🛠️ Stack Tecnológico
- **Lenguaje:** Python 3.12
- **Framework de Pruebas:** Pytest
- **Herramienta de Automatización:** Playwright (Chromium)
- **CI/CD:** GitHub Actions
- **Gestión de Pruebas:** Jira + Xray Cloud

## 📂 Estructura del Repositorio

```text
icg-demo-regresion/
├── .github/workflows/       # Configuración de CI/CD (GitHub Actions)
│   └── regresion.yml             # Pipeline de ejecución y envío a Xray
├── evidencias/              # Capturas (.png) y videos (.webm) de los tests
├── scripts/                 # Scripts auxiliares
│   └── adjuntar_screenshots.py # Lógica para subir videos y vincular test a Jira 
├── tests/                   # Suite de pruebas automatizadas
│   └── regresion/
│       ├── autenticacion/   # Test de Login (PRB3103-42)
│       ├── clientes/        # Test de Visualización (PRB3103-44)
│       └── creditos/        # Test de Cálculos (PRB3103-41)
├── conftest.py              # Configuración global de Playwright y Hooks
├── pytest.ini               # Optimización de reportes y logs
└── requirements.txt         # Librerías necesarias (Pytest, Playwright) v.01