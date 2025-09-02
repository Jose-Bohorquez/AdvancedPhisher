#!/data/data/com.termux/files/usr/bin/bash

# AdvancedPhisher - Script de Verificación Post-Instalación para Termux
# Este script verifica que la instalación sea correcta y funcional

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

print_header() {
    echo -e "${PURPLE}🔍 $1${NC}"
}

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           VERIFICACIÓN DE INSTALACIÓN TERMUX                ║"
echo "║                 AdvancedPhisher v1.0                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo

# Variables para el reporte
ERRORS=0
WARNINGS=0

# Función para incrementar contadores
log_error() {
    ERRORS=$((ERRORS + 1))
    print_error "$1"
}

log_warning() {
    WARNINGS=$((WARNINGS + 1))
    print_warning "$1"
}

# 1. Verificar entorno Termux
print_header "[1/8] Verificando entorno Termux"
if [ -d "/data/data/com.termux" ]; then
    print_success "Ejecutándose en Termux"
    print_info "Directorio Termux: /data/data/com.termux"
else
    log_warning "No se detectó entorno Termux estándar"
fi
echo

# 2. Verificar Python
print_header "[2/8] Verificando Python"
if command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1)
    print_success "Python disponible: $PYTHON_VERSION"
    
    # Verificar versión mínima
    PYTHON_MAJOR=$(python -c "import sys; print(sys.version_info.major)")
    PYTHON_MINOR=$(python -c "import sys; print(sys.version_info.minor)")
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
        print_success "Versión de Python compatible (3.8+)"
    else
        log_error "Versión de Python incompatible. Se requiere Python 3.8+"
    fi
else
    log_error "Python no encontrado"
fi
echo

# 3. Verificar pip
print_header "[3/8] Verificando pip"
if command -v pip &> /dev/null; then
    PIP_VERSION=$(pip --version 2>&1)
    print_success "pip disponible: $PIP_VERSION"
else
    log_error "pip no encontrado"
fi
echo

# 4. Verificar estructura del proyecto
print_header "[4/8] Verificando estructura del proyecto"
REQUIRED_FILES=("main.py" "requirements_termux.txt" "install_termux.sh")
OPTIONAL_FILES=("README.md" "TERMUX_GUIDE.md" "GUIA_ESTUDIANTES.md")
REQUIRED_DIRS=("core" "templates")
OPTIONAL_DIRS=("logs" "docs" "ssl_certs")

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "Archivo requerido: $file"
    else
        log_error "Archivo requerido faltante: $file"
    fi
done

for file in "${OPTIONAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "Archivo opcional: $file"
    else
        log_warning "Archivo opcional faltante: $file"
    fi
done

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        print_success "Directorio requerido: $dir/"
    else
        log_error "Directorio requerido faltante: $dir/"
    fi
done

for dir in "${OPTIONAL_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        print_success "Directorio opcional: $dir/"
    else
        log_warning "Directorio opcional faltante: $dir/"
    fi
done
echo

# 5. Verificar dependencias críticas
print_header "[5/8] Verificando dependencias críticas"
CRITICAL_MODULES=("flask" "requests" "colorama" "yaml")

for module in "${CRITICAL_MODULES[@]}"; do
    if python -c "import $module" 2>/dev/null; then
        # Obtener versión si es posible
        VERSION=$(python -c "import $module; print(getattr($module, '__version__', 'unknown'))" 2>/dev/null)
        print_success "$module (versión: $VERSION)"
    else
        log_error "Módulo crítico faltante: $module"
    fi
done
echo

# 6. Verificar dependencias opcionales
print_header "[6/8] Verificando dependencias opcionales"
OPTIONAL_MODULES=("fake_useragent" "jinja2" "werkzeug")

for module in "${OPTIONAL_MODULES[@]}"; do
    if python -c "import $module" 2>/dev/null; then
        VERSION=$(python -c "import $module; print(getattr($module, '__version__', 'unknown'))" 2>/dev/null)
        print_success "$module (versión: $VERSION)"
    else
        log_warning "Módulo opcional faltante: $module"
    fi
done
echo

# 7. Verificar funcionalidad básica
print_header "[7/8] Verificando funcionalidad básica"

# Test de importación del módulo principal
if python -c "import sys; sys.path.append('.'); import main" 2>/dev/null; then
    print_success "Módulo principal importable"
else
    log_error "No se puede importar el módulo principal"
fi

# Test de Flask
if python -c "from flask import Flask; app = Flask(__name__)" 2>/dev/null; then
    print_success "Flask funcional"
else
    log_error "Flask no funcional"
fi

# Test de requests
if python -c "import requests; print('Requests OK')" 2>/dev/null; then
    print_success "Requests funcional"
else
    log_error "Requests no funcional"
fi
echo

# 8. Verificar permisos y scripts
print_header "[8/8] Verificando permisos y scripts"

SCRIPTS=("install_termux.sh" "start_termux.sh" "check_termux.sh")
for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            print_success "Script ejecutable: $script"
        else
            log_warning "Script sin permisos de ejecución: $script"
            print_info "Ejecute: chmod +x $script"
        fi
    else
        log_warning "Script faltante: $script"
    fi
done
echo

# Reporte final
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    REPORTE FINAL                            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    print_success "🎉 ¡Instalación perfecta! Todo está funcionando correctamente."
    echo
    print_info "Para iniciar AdvancedPhisher:"
    echo "   ./start_termux.sh"
elif [ $ERRORS -eq 0 ]; then
    print_success "✅ Instalación funcional con $WARNINGS advertencias menores."
    echo
    print_info "Para iniciar AdvancedPhisher:"
    echo "   ./start_termux.sh"
    echo
    print_warning "Las advertencias no afectan la funcionalidad básica."
else
    print_error "❌ Instalación con problemas: $ERRORS errores, $WARNINGS advertencias."
    echo
    print_info "Acciones recomendadas:"
    echo "   1. Ejecute nuevamente: ./install_termux.sh"
    echo "   2. Verifique su conexión a internet"
    echo "   3. Actualice Termux: pkg update && pkg upgrade"
    echo "   4. Consulte TERMUX_GUIDE.md para soluciones"
fi

echo
print_info "📚 Documentación disponible:"
echo "   - README.md (información general)"
echo "   - TERMUX_GUIDE.md (guía específica para Termux)"
echo "   - GUIA_ESTUDIANTES.md (uso ético y educativo)"
echo
print_warning "⚠️  Recuerde: Esta herramienta es SOLO para uso educativo y ético."
echo