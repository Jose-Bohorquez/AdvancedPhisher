#!/bin/bash

# AdvancedPhisher - Script de Instalación para Linux/macOS
# Este script automatiza la instalación completa del framework

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar mensajes con colores
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Banner de inicio
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ADVANCEDPHISHER v1.0                     ║"
echo "║                Instalador para Linux/macOS                  ║"
echo "║                                                              ║"
echo "║  🎯 Framework Educativo de Phishing para Ciberseguridad     ║"
echo "║  ⚠️  SOLO PARA USO ÉTICO Y EDUCATIVO                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo
echo "Iniciando instalación automática..."
echo

# Verificar si el script se ejecuta desde el directorio correcto
if [ ! -f "main.py" ] || [ ! -f "requirements.txt" ]; then
    print_error "Error: Este script debe ejecutarse desde el directorio raíz de AdvancedPhisher"
    print_info "Asegúrese de estar en el directorio que contiene main.py y requirements.txt"
    exit 1
fi

# [1/7] Verificar Python
echo "[1/7] Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
else
    print_error "Python no está instalado"
    echo
    echo "Para instalar Python:"
    echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"
    echo "  CentOS/RHEL:   sudo yum install python3 python3-pip"
    echo "  macOS:         brew install python3"
    echo "  O visite: https://python.org/downloads/"
    echo
    exit 1
fi

print_success "Python $PYTHON_VERSION detectado"
echo

# [2/7] Verificar pip
echo "[2/7] Verificando pip..."
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    print_error "pip no está disponible"
    echo "Intentando instalar pip..."
    $PYTHON_CMD -m ensurepip --upgrade
    if [ $? -eq 0 ]; then
        PIP_CMD="$PYTHON_CMD -m pip"
    else
        print_error "No se pudo instalar pip automáticamente"
        echo "Instale pip manualmente y ejecute este script nuevamente"
        exit 1
    fi
fi

print_success "pip disponible"
echo

# [3/7] Verificar permisos de escritura
echo "[3/7] Verificando permisos..."
if [ -w "." ]; then
    print_success "Permisos de escritura verificados"
else
    print_warning "Permisos de escritura limitados"
    print_info "Es posible que necesite ejecutar con sudo para algunas operaciones"
fi
echo

# [4/7] Actualizar pip
echo "[4/7] Actualizando pip..."
$PIP_CMD install --upgrade pip --user &> /dev/null
if [ $? -eq 0 ]; then
    print_success "pip actualizado"
else
    print_warning "No se pudo actualizar pip (continuando...)"
fi
echo

# [5/7] Crear entorno virtual (opcional pero recomendado)
echo "[5/7] Configurando entorno virtual..."
if [ ! -d "venv" ]; then
    print_info "Creando entorno virtual..."
    $PYTHON_CMD -m venv venv
    if [ $? -eq 0 ]; then
        print_success "Entorno virtual creado"
    else
        print_warning "No se pudo crear entorno virtual, continuando sin él"
    fi
else
    print_info "Entorno virtual ya existe"
fi

# Activar entorno virtual si existe
if [ -d "venv" ] && [ -f "venv/bin/activate" ]; then
    print_info "Activando entorno virtual..."
    source venv/bin/activate
    print_success "Entorno virtual activado"
    PIP_CMD="pip"  # Dentro del venv, usar pip directamente
fi
echo

# [6/7] Instalar dependencias
echo "[6/7] Instalando dependencias de Python..."
echo "    Esto puede tomar varios minutos..."
$PIP_CMD install -r requirements.txt
if [ $? -eq 0 ]; then
    print_success "Dependencias instaladas correctamente"
else
    print_error "Error instalando dependencias"
    print_info "Verifique su conexión a internet y ejecute nuevamente"
    exit 1
fi
echo

# [7/7] Ejecutar instalador Python
echo "[7/7] Ejecutando configuración avanzada..."
$PYTHON_CMD install.py
if [ $? -ne 0 ]; then
    print_warning "El instalador Python reportó algunos problemas"
    print_info "Pero continuaremos con la verificación final..."
fi
echo

# Verificación final
echo "Verificación final..."
if [ -f "main.py" ]; then
    print_success "Archivo principal encontrado"
else
    print_error "main.py no encontrado"
fi

if [ -d "templates" ]; then
    print_success "Directorio de templates encontrado"
else
    print_warning "Directorio templates no encontrado"
fi

if [ -d "core" ]; then
    print_success "Módulos del core encontrados"
else
    print_error "Directorio core no encontrado"
fi
echo

# Crear script de inicio rápido
echo "[EXTRA] Creando script de inicio rápido..."
cat > start_advancedphisher.sh << 'EOF'
#!/bin/bash
echo "Iniciando AdvancedPhisher..."

# Activar entorno virtual si existe
if [ -d "venv" ] && [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Ejecutar la aplicación
if command -v python3 &> /dev/null; then
    python3 main.py "$@"
elif command -v python &> /dev/null; then
    python main.py "$@"
else
    echo "Error: Python no encontrado"
    exit 1
fi
EOF

chmod +x start_advancedphisher.sh
print_success "Script de inicio creado: start_advancedphisher.sh"
echo

# Mostrar resumen final
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    INSTALACIÓN COMPLETADA                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo
print_success "¡AdvancedPhisher está listo para usar!"
echo
echo "Para iniciar la aplicación:"
echo "  1. Ejecute: $PYTHON_CMD main.py"
echo "  2. O ejecute: ./start_advancedphisher.sh"
echo
echo "Para obtener ayuda:"
echo "  $PYTHON_CMD main.py --help"
echo
if [ -d "venv" ]; then
    print_info "Entorno virtual creado en ./venv"
    echo "  Para activarlo manualmente: source venv/bin/activate"
    echo "  Para desactivarlo: deactivate"
    echo
fi

print_warning "RECORDATORIO IMPORTANTE:"
echo "    Esta herramienta es SOLO para uso educativo y ético."
echo "    Lea la documentación ética antes de usar."
echo
echo "Documentación disponible en:"
echo "  - README.md"
echo "  - docs/ethical_usage_guide.md"
echo
print_success "¡Disfrute aprendiendo sobre ciberseguridad de forma ética!"
echo