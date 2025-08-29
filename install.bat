@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM AdvancedPhisher - Script de Instalación para Windows
REM Este script automatiza la instalación completa del framework

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    ADVANCEDPHISHER v1.0                     ║
echo ║                 Instalador para Windows                     ║
echo ║                                                              ║
echo ║  🎯 Framework Educativo de Phishing para Ciberseguridad     ║
echo ║  ⚠️  SOLO PARA USO ÉTICO Y EDUCATIVO                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Iniciando instalación automática...
echo.

REM Verificar si Python está instalado
echo [1/6] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo.
    echo Para instalar Python:
    echo 1. Vaya a https://python.org/downloads/
    echo 2. Descargue Python 3.8 o superior
    echo 3. Durante la instalación, marque "Add Python to PATH"
    echo 4. Reinicie el símbolo del sistema y ejecute este script nuevamente
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% detectado
echo.

REM Verificar pip
echo [2/6] Verificando pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: pip no está disponible
    echo Intentando instalar pip...
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo ❌ No se pudo instalar pip automáticamente
        pause
        exit /b 1
    )
)
echo ✅ pip disponible
echo.

REM Actualizar pip
echo [3/6] Actualizando pip...
python -m pip install --upgrade pip >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ pip actualizado
) else (
    echo ⚠️  Advertencia: No se pudo actualizar pip
)
echo.

REM Instalar dependencias
echo [4/6] Instalando dependencias de Python...
echo    Esto puede tomar varios minutos...
if exist requirements.txt (
    python -m pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo ✅ Dependencias instaladas correctamente
    ) else (
        echo ❌ Error instalando dependencias
        echo Verifique su conexión a internet y ejecute nuevamente
        pause
        exit /b 1
    )
) else (
    echo ❌ Error: Archivo requirements.txt no encontrado
    echo Asegúrese de estar en el directorio correcto de AdvancedPhisher
    pause
    exit /b 1
)
echo.

REM Ejecutar instalador Python
echo [5/6] Ejecutando configuración avanzada...
python install.py
if %errorlevel% neq 0 (
    echo ⚠️  El instalador Python reportó algunos problemas
    echo Pero continuaremos con la verificación final...
)
echo.

REM Verificación final
echo [6/6] Verificación final...
if exist main.py (
    echo ✅ Archivo principal encontrado
) else (
    echo ❌ Error: main.py no encontrado
)

if exist templates\ (
    echo ✅ Directorio de templates encontrado
) else (
    echo ⚠️  Directorio templates no encontrado
)

if exist core\ (
    echo ✅ Módulos del core encontrados
) else (
    echo ❌ Error: Directorio core no encontrado
)
echo.

REM Crear script de inicio rápido
echo [EXTRA] Creando script de inicio rápido...
echo @echo off > start_advancedphisher.bat
echo echo Iniciando AdvancedPhisher... >> start_advancedphisher.bat
echo python main.py >> start_advancedphisher.bat
echo pause >> start_advancedphisher.bat
echo ✅ Script de inicio creado: start_advancedphisher.bat
echo.

REM Mostrar resumen final
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    INSTALACIÓN COMPLETADA                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🎉 ¡AdvancedPhisher está listo para usar!
echo.
echo Para iniciar la aplicación:
echo   1. Ejecute: python main.py
echo   2. O haga doble clic en: start_advancedphisher.bat
echo.
echo Para obtener ayuda:
echo   python main.py --help
echo.
echo ⚠️  RECORDATORIO IMPORTANTE:
echo    Esta herramienta es SOLO para uso educativo y ético.
echo    Lea la documentación ética antes de usar.
echo.
echo Documentación disponible en:
echo   - README.md
echo   - docs/ethical_usage_guide.md
echo.
echo ¡Disfrute aprendiendo sobre ciberseguridad de forma ética!
echo.
pause