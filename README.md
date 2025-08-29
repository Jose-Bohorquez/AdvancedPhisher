# AdvancedPhisher 🎣

**Framework Avanzado de Phishing para Pruebas de Penetración y Concienciación en Seguridad**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/security-educational-yellow.svg)]()

## ⚠️ AVISO LEGAL IMPORTANTE

**ESTE FRAMEWORK ES EXCLUSIVAMENTE PARA FINES EDUCATIVOS Y DE PRUEBAS DE PENETRACIÓN AUTORIZADAS**

El uso de AdvancedPhisher para actividades maliciosas, no autorizadas o ilegales está **ESTRICTAMENTE PROHIBIDO**. Los desarrolladores no se hacen responsables del mal uso de esta herramienta. Al usar este software, usted acepta:

- Usar la herramienta únicamente para pruebas de penetración autorizadas
- Obtener consentimiento explícito por escrito antes de realizar cualquier prueba
- Cumplir con todas las leyes locales, nacionales e internacionales
- No usar la herramienta para actividades maliciosas o fraudulentas
- Asumir toda la responsabilidad legal por el uso de esta herramienta

## 📋 Descripción

AdvancedPhisher es un framework completo y avanzado diseñado para profesionales de seguridad, investigadores y equipos de red team que necesitan realizar pruebas de phishing controladas y autorizadas. La herramienta incluye:

### 🚀 Características Principales

- **Templates Realistas**: Réplicas exactas de sitios populares (Facebook, Google, Instagram, LinkedIn, TikTok)
- **Sistema de Logging Avanzado**: Registro detallado de todas las actividades con análisis de datos
- **Deployment Automático**: Despliegue a múltiples servidores y dominios
- **Técnicas de Evasión**: Anti-detección y bypass de sistemas de seguridad
- **Reportes Detallados**: Generación de reportes en HTML, JSON y CSV con gráficos
- **Interfaz Interactiva**: Consola avanzada con menús intuitivos
- **Configuración SSL**: Soporte completo para HTTPS y certificados
- **Análisis Geográfico**: Filtrado por países y análisis de geolocalización

## 🛠️ Instalación

### Requisitos del Sistema

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Sistema operativo: Windows, Linux, macOS
- Conexión a internet para descargar dependencias

### Instalación Automática (Recomendada)

Para una instalación completamente automatizada, usa uno de estos scripts:

#### Windows:
```cmd
git clone https://github.com/tu-usuario/AdvancedPhisher.git
cd AdvancedPhisher
install.bat
```

#### Linux/macOS:
```bash
git clone https://github.com/tu-usuario/AdvancedPhisher.git
cd AdvancedPhisher
chmod +x install.sh
./install.sh
```

### Instalación Manual

Si prefieres instalar manualmente:

1. **Clonar el repositorio:**
```bash
git clone https://github.com/tu-usuario/AdvancedPhisher.git
cd AdvancedPhisher
```

2. **Crear entorno virtual (recomendado):**
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Linux/macOS:
source venv/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Crear directorios necesarios:**
```bash
mkdir logs reports ssl_certs uploads
```

5. **Configuración inicial:**
```bash
python install.py
```

## 🚀 Uso Rápido

### Inicio Básico

#### Método 1: Script de inicio rápido (Recomendado)
```bash
# Windows
start_advancedphisher.bat

# Linux/macOS
./start_advancedphisher.sh
```

#### Método 2: Comando directo
```bash
# Ejecutar con configuración por defecto
python main.py

# Ejecutar en puerto específico
python main.py --port 8080

# Ejecutar con SSL
python main.py --ssl --cert cert.pem --key key.pem

# Usar configuración personalizada
python main.py --config custom_settings.json

# Modo silencioso
python main.py --quiet

# Mostrar ayuda
python main.py --help
```

### Ejemplo de Uso

```python
from core.phisher import AdvancedPhisher
from core.config import PhisherConfig

# Configuración básica
config = PhisherConfig(
    port=5000,
    template='facebook',
    target_url='https://facebook.com',
    enable_logging=True
)

# Inicializar framework
phisher = AdvancedPhisher(config)

# Iniciar servidor
phisher.start_server()
```

## 📁 Estructura del Proyecto

```
AdvancedPhisher/
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias de Python
├── README.md              # Este archivo
├── LICENSE                # Licencia del proyecto
├── config/
│   ├── config.json        # Configuración principal
│   ├── domains.json       # Configuración de dominios
│   └── ssl/               # Certificados SSL
├── core/
│   ├── __init__.py
│   ├── phisher.py         # Clase principal del framework
│   ├── config.py          # Gestión de configuración
│   ├── logger.py          # Sistema de logging avanzado
│   ├── reports.py         # Generación de reportes
│   ├── deployment.py      # Sistema de deployment
│   └── evasion.py         # Técnicas de evasión
├── templates/
│   ├── facebook.html      # Template de Facebook
│   ├── google.html        # Template de Google
│   ├── instagram.html     # Template de Instagram
│   ├── linkedin.html      # Template de LinkedIn
│   ├── tiktok.html        # Template de TikTok
│   └── base.html          # Template base
├── static/
│   ├── css/               # Archivos CSS
│   ├── js/                # Archivos JavaScript
│   └── images/            # Imágenes y recursos
├── logs/                  # Archivos de log
├── reports/               # Reportes generados
├── deployments/           # Paquetes de deployment
└── docs/                  # Documentación adicional
```