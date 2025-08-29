#!/data/data/com.termux/files/usr/bin/bash

# AdvancedPhisher - Script de Instalación para Termux (Android)
# Este script maneja las limitaciones específicas de Android/Termux

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

print_step() {
    echo -e "${PURPLE}🔧 $1${NC}"
}

# Banner de inicio
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ADVANCEDPHISHER v1.0                     ║"
echo "║                 Instalador para Termux                      ║"
echo "║                                                              ║"
echo "║  🎯 Framework Educativo de Phishing para Ciberseguridad     ║"
echo "║  📱 Optimizado para Android/Termux                          ║"
echo "║  ⚠️  SOLO PARA USO ÉTICO Y EDUCATIVO                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo
print_info "Iniciando instalación optimizada para Termux..."
echo

# Verificar que estamos en Termux
if [ ! -d "/data/data/com.termux" ]; then
    print_warning "Este script está optimizado para Termux"
    print_info "Si estás en un sistema Linux normal, usa install.sh"
    echo
fi

# Verificar si el script se ejecuta desde el directorio correcto
if [ ! -f "main.py" ] || [ ! -f "requirements.txt" ]; then
    print_error "Error: Este script debe ejecutarse desde el directorio raíz de AdvancedPhisher"
    print_info "Asegúrese de estar en el directorio que contiene main.py"
    exit 1
fi

print_step "[1/8] Actualizando paquetes de Termux..."
echo "    Esto puede tomar varios minutos la primera vez..."
pkg update -y > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Paquetes de Termux actualizados"
else
    print_warning "Algunos paquetes no se pudieron actualizar (continuando...)"
fi
echo

print_step "[2/8] Instalando dependencias del sistema..."
echo "    Instalando Python, git, y herramientas de compilación..."
pkg install -y python python-pip git build-essential libffi openssl > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Dependencias del sistema instaladas"
else
    print_error "Error instalando dependencias del sistema"
    print_info "Intente ejecutar manualmente: pkg install python python-pip git"
    exit 1
fi
echo

print_step "[3/8] Verificando Python..."
if command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION detectado"
else
    print_error "Python no está disponible después de la instalación"
    exit 1
fi
echo

print_step "[4/8] Verificando pip..."
if command -v pip &> /dev/null; then
    print_success "pip disponible"
else
    print_error "pip no está disponible"
    print_info "Intentando instalar pip..."
    python -m ensurepip --upgrade
    if [ $? -ne 0 ]; then
        print_error "No se pudo instalar pip"
        exit 1
    fi
fi
echo

print_step "[5/8] Actualizando pip y herramientas..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "pip y herramientas actualizadas"
else
    print_warning "No se pudieron actualizar todas las herramientas (continuando...)"
fi
echo

print_step "[6/8] Instalando dependencias optimizadas para Termux..."
echo "    Usando requirements_termux.txt (sin dependencias problemáticas)..."
echo "    Esto puede tomar 10-15 minutos..."

if [ -f "requirements_termux.txt" ]; then
    pip install -r requirements_termux.txt
    if [ $? -eq 0 ]; then
        print_success "Dependencias optimizadas instaladas correctamente"
    else
        print_warning "Algunas dependencias fallaron, intentando instalación básica..."
        # Instalación mínima de emergencia
        pip install flask requests pandas matplotlib colorama
        if [ $? -eq 0 ]; then
            print_success "Instalación básica completada"
        else
            print_error "Error en instalación básica"
            print_info "Verifique su conexión a internet"
            exit 1
        fi
    fi
else
    print_warning "requirements_termux.txt no encontrado, usando requirements.txt estándar..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        print_error "Error con requirements.txt estándar"
        print_info "Algunas dependencias pueden no ser compatibles con Termux"
    fi
fi
echo

print_step "[7/8] Configuración específica para Termux..."

# Crear directorios necesarios
mkdir -p logs reports ssl_certs uploads data
print_success "Directorios creados"

# Configurar permisos
chmod +x *.py 2>/dev/null
chmod +x *.sh 2>/dev/null
print_success "Permisos configurados"

# Ejecutar instalador Python si existe
if [ -f "install.py" ]; then
    print_info "Ejecutando configuración avanzada..."
    python install.py
    if [ $? -ne 0 ]; then
        print_warning "Configuración avanzada reportó algunos problemas"
    fi
fi
echo

print_step "[8/8] Creando scripts de inicio para Termux..."

# Script de inicio optimizado para Termux
cat > start_termux.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "🚀 Iniciando AdvancedPhisher en Termux..."
echo

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py no encontrado"
    echo "   Asegúrese de estar en el directorio de AdvancedPhisher"
    exit 1
fi

# Mostrar información del sistema
echo "📱 Sistema: $(uname -o)"
echo "🐍 Python: $(python --version 2>&1)"
echo "📍 Directorio: $(pwd)"
echo

# Ejecutar la aplicación
echo "▶️  Ejecutando AdvancedPhisher..."
python main.py "$@"
EOF

chmod +x start_termux.sh
print_success "Script de inicio para Termux creado: start_termux.sh"

# Script para verificar la instalación
cat > check_termux.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "🔍 Verificando instalación de AdvancedPhisher en Termux..."
echo

# Verificar Python
if command -v python &> /dev/null; then
    echo "✅ Python: $(python --version 2>&1)"
else
    echo "❌ Python no encontrado"
fi

# Verificar pip
if command -v pip &> /dev/null; then
    echo "✅ pip disponible"
else
    echo "❌ pip no encontrado"
fi

# Verificar módulos críticos
echo "📦 Verificando módulos Python:"
for module in flask requests pandas matplotlib colorama; do
    if python -c "import $module" 2>/dev/null; then
        echo "  ✅ $module"
    else
        echo "  ❌ $module (faltante)"
    fi
done

# Verificar archivos del proyecto
echo "📁 Verificando archivos del proyecto:"
for file in main.py requirements.txt; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (faltante)"
    fi
done

# Verificar directorios
echo "📂 Verificando directorios:"
for dir in templates core logs; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir/"
    else
        echo "  ⚠️  $dir/ (faltante)"
    fi
done

echo
echo "🎯 Para iniciar AdvancedPhisher: ./start_termux.sh"
EOF

chmod +x check_termux.sh
print_success "Script de verificación creado: check_termux.sh"
echo

# Verificación final
print_step "Verificación final..."
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
    print_warning "Directorio core no encontrado"
fi
echo

# Mostrar resumen final
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              INSTALACIÓN TERMUX COMPLETADA                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo
print_success "¡AdvancedPhisher está listo para usar en Termux!"
echo
echo "📱 Para iniciar la aplicación:"
echo "   ./start_termux.sh"
echo
echo "🔍 Para verificar la instalación:"
echo "   ./check_termux.sh"
echo
echo "📋 Para obtener ayuda:"
echo "   python main.py --help"
echo
print_info "💡 Consejos para Termux:"
echo "   • Usa 'termux-wake-lock' para evitar que se suspenda"
echo "   • El servidor estará disponible en http://localhost:8080"
echo "   • Usa Ctrl+C para detener el servidor"
echo
print_warning "⚠️  RECORDATORIO IMPORTANTE:"
echo "    Esta herramienta es SOLO para uso educativo y ético."
echo "    Lea la documentación ética antes de usar."
echo
echo "📚 Documentación disponible en:"
echo "   - README.md"
echo "   - GUIA_ESTUDIANTES.md"
echo "   - docs/ethical_usage_guide.md"
echo
print_success "¡Disfrute aprendiendo sobre ciberseguridad de forma ética en Android! 📱🔒"
echo