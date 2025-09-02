# 📱 Guía de Instalación y Uso en Termux (Android)

## 🎯 Introducción

Esta guía te ayudará a instalar y usar AdvancedPhisher en Termux (Android). Termux tiene algunas limitaciones específicas que hemos optimizado para ti.

## ⚠️ Problemas Identificados y Solucionados

### Problema Principal: Compilación Nativa en Termux

Los errores más comunes en Termux son:

```
clang++: error: invalid linker name in argument '-fuse-ld=gold'
Building wheel for ninja (pyproject.toml): finished with status 'error'
subprocess-exited-with-error
```

**Causas identificadas:**
1. **pandas/numpy:** Requieren `ninja` para compilación, que falla con el linker 'gold' no disponible en Termux
2. **cryptography:** Requiere compilación de Rust, no disponible en Android/Termux para Python 3.12
3. **matplotlib/seaborn:** Requieren compilación nativa de librerías gráficas
4. **Dependencias pesadas:** Muchas librerías requieren herramientas de compilación no disponibles

### ✅ Solución Implementada: Versión Ultra-Ligera

Hemos creado una versión **ultra-optimizada** que elimina TODAS las dependencias problemáticas:
- ❌ **Removido:** pandas, numpy, matplotlib, seaborn, pillow
- ❌ **Removido:** cryptography, pycryptodome, reportlab
- ❌ **Removido:** psutil, loguru, httpx, orjson
- ✅ **Mantenido:** Solo dependencias esenciales que funcionan en Termux

## 🚀 Solución Optimizada

Hemos creado una instalación específica para Termux que evita estas dependencias problemáticas.

### Instalación Rápida para Termux

```bash
# 1. Clonar el repositorio (si no lo has hecho)
git clone https://github.com/tu-usuario/AdvancedPhisher.git
cd AdvancedPhisher

# 2. Usar el instalador optimizado para Termux
chmod +x install_termux.sh
./install_termux.sh
```

### Instalación Manual (si el script falla)

#### Paso 1: Preparar Termux
```bash
# Actualizar paquetes
pkg update && pkg upgrade

# Instalar dependencias básicas
pkg install python python-pip git build-essential libffi openssl
```

#### Paso 2: Usar Requirements Optimizado
```bash
# Usar el archivo de dependencias optimizado para Termux
pip install -r requirements_termux.txt
```

#### Paso 3: Configuración Manual
```bash
# Crear directorios necesarios
mkdir -p logs reports ssl_certs uploads data

# Ejecutar configuración
python install.py
```

## 📋 Diferencias del Requirements Termux (Versión Ultra-Ligera)

### ❌ Dependencias Removidas (Requieren Compilación Nativa)

**Análisis de datos (problemáticas):**
- `pandas==2.1.1` → Requiere ninja, falla compilación
- `numpy==1.24.4` → Requiere ninja, falla compilación
- `matplotlib==3.7.2` → Requiere compilación gráfica nativa
- `seaborn==0.12.2` → Depende de matplotlib
- `pillow==10.0.1` → Requiere librerías de imagen nativas

**Criptografía y seguridad:**
- `cryptography>=41.0.4` → Requiere Rust, no disponible
- `pycryptodome==3.19.0` → Puede causar problemas de compilación
- `pyOpenSSL>=23.2.0` → Depende de cryptography

**Utilidades del sistema:**
- `psutil==5.9.5` → Puede causar problemas de compilación
- `netifaces>=0.11.0` → Problemas con interfaces de red
- `dnspython>=2.4.2` → No esencial, removida

**Logging y reportes:**
- `loguru==0.7.2` → Usar logging estándar de Python
- `reportlab==4.0.4` → Requiere compilación, usar alternativas
- `orjson==3.9.7` → Usar json estándar de Python

**HTTP y red:**
- `httpx==0.25.0` → requests es suficiente
- `scapy>=2.5.0` → Requiere privilegios root

### ✅ Dependencias Mantenidas (Core Esencial)

**Framework web (CRÍTICO):**
- `Flask==2.3.3` → Framework web principal
- `Werkzeug==2.3.7` → Servidor WSGI
- `Jinja2==3.1.2` → Motor de templates
- `MarkupSafe==2.1.3` → Seguridad de templates
- `click==8.1.7` → CLI interface
- `itsdangerous==2.1.2` → Seguridad de sesiones

**HTTP y red (ESENCIAL):**
- `requests==2.31.0` → Cliente HTTP básico
- `urllib3==2.0.7` → Utilidades HTTP
- `certifi==2023.7.22` → Certificados SSL
- `charset-normalizer==3.3.0` → Codificación de caracteres
- `idna==3.4` → Soporte de dominios internacionales

**Utilidades básicas:**
- `colorama==0.4.6` → Colores en terminal
- `termcolor==2.3.0` → Colores adicionales
- `python-dateutil==2.8.2` → Manejo de fechas
- `pytz==2023.3` → Zonas horarias
- `validators==0.22.0` → Validación de datos
- `pyyaml==6.0.1` → Configuración YAML
- `fake-useragent==1.4.0` → User agents (esencial para phishing)

### 🔄 Alternativas Implementadas

**En lugar de pandas/numpy:**
- Usar estructuras de datos nativas de Python (dict, list)
- JSON para almacenamiento de datos
- CSV básico para reportes

**En lugar de matplotlib:**
- Reportes en texto plano
- Estadísticas básicas en JSON
- Gráficos opcionales via web (Chart.js)

**En lugar de cryptography:**
- hashlib estándar de Python
- secrets estándar para generación segura
- SSL básico con certificados auto-firmados

**En lugar de psutil:**
- os y platform estándar de Python
- Información básica del sistema

## 🔧 Scripts Específicos para Termux

### Instalación Optimizada
```bash
# Script de instalación con manejo de errores mejorado
./install_termux.sh
```

### Verificación Completa Post-Instalación
```bash
# Nuevo script de verificación exhaustiva
./verify_termux_install.sh
```

### Iniciar AdvancedPhisher
```bash
./start_termux.sh
```

### Verificar Instalación (Básica)
```bash
./check_termux.sh
```

### Inicio Manual
```bash
python main.py
```

### Diagnóstico de Problemas
```bash
# Para diagnosticar problemas específicos
chmod +x verify_termux_install.sh
./verify_termux_install.sh
```

## 🚨 Solución de Problemas Comunes

### ❌ Error: "Building wheel for ninja failed" (NUEVO)
```bash
clang++: error: invalid linker name in argument '-fuse-ld=gold'
Building wheel for ninja (pyproject.toml): finished with status 'error'
```
**Solución:** Este error indica que pandas/numpy requieren ninja que no puede compilarse en Termux.
```bash
# Usar la versión ultra-ligera sin pandas/numpy
./install_termux.sh  # Ya optimizado para evitar este error
```

### ❌ Error: "pandas installation failed" (NUEVO)
```bash
subprocess-exited-with-error
× Building wheel for pandas (pyproject.toml) did not run successfully
```
**Solución:** pandas requiere compilación nativa no disponible en Termux.
```bash
# La nueva versión ya no incluye pandas
# Usar estructuras de datos nativas de Python en su lugar
```

### ❌ Error: "cryptography requires Rust" (CONOCIDO)
```bash
Rust not found, installing into a temporary directory
Unsupported platform: 312
```
**Solución:** Usar alternativas sin Rust.
```bash
# Usar hashlib y secrets estándar de Python
# La versión ultra-ligera ya no incluye cryptography
```

### ❌ Error: "matplotlib compilation failed" (NUEVO)
```bash
Building wheel for matplotlib failed
```
**Solución:** matplotlib requiere librerías gráficas nativas.
```bash
# Usar reportes en texto plano o gráficos web
# La versión ultra-ligera ya no incluye matplotlib
```

### Error: "Permission denied"
**Solución:**
```bash
# Dar permisos a los scripts
chmod +x *.sh
chmod +x *.py
```

### Error: "Module not found"
**Solución:**
```bash
# Verificar instalación completa
./verify_termux_install.sh

# Verificación básica
./check_termux.sh

# Reinstalar dependencias críticas
pip install flask requests colorama pyyaml fake-useragent
```

### Error: "Port already in use"
**Solución:**
```bash
# Usar puerto diferente
python main.py --port 8081

# O matar procesos existentes
pkill -f "python.*main.py"
```

### Error: "Import Error" después de instalación
**Solución:**
```bash
# Verificar qué módulos faltan específicamente
python -c "import flask, requests, colorama, yaml; print('Core modules OK')"

# Reinstalar módulos faltantes individualmente
pip install --no-cache-dir flask requests colorama pyyaml
```

## 📱 Optimizaciones para Android

### Rendimiento
```bash
# Evitar suspensión durante uso
termux-wake-lock

# Liberar lock cuando termines
termux-wake-unlock
```

### Acceso desde otros dispositivos
```bash
# Obtener IP local
ifconfig | grep inet

# Iniciar en todas las interfaces
python main.py --host 0.0.0.0 --port 8080
```

### Almacenamiento
```bash
# Acceder al almacenamiento del teléfono
termux-setup-storage

# Los archivos estarán en:
# ~/storage/shared/ (almacenamiento interno)
# ~/storage/external-1/ (SD card si existe)
```

## 🔒 Consideraciones de Seguridad en Android

### Permisos Limitados
- ✅ No requiere root
- ✅ Funciona en espacio de usuario
- ⚠️ Sin acceso a interfaces de red del sistema
- ⚠️ Sin capacidades de packet sniffing

### Funcionalidades Disponibles
- ✅ Servidor web local
- ✅ Templates de phishing
- ✅ Logging y reportes
- ✅ Análisis básico
- ❌ Monitoreo de red avanzado
- ❌ Inyección de paquetes

## 📊 Uso Típico en Termux

### Escenario 1: Demostración Local
```bash
# Iniciar servidor
./start_termux.sh

# Acceder desde el mismo dispositivo
# Abrir navegador en: http://localhost:8080
```

### Escenario 2: Demostración en Red Local
```bash
# Obtener IP del dispositivo
ip addr show wlan0 | grep inet

# Iniciar servidor en todas las interfaces
python main.py --host 0.0.0.0

# Otros dispositivos pueden acceder via:
# http://[IP-DEL-ANDROID]:8080
```

### Escenario 3: Desarrollo y Testing
```bash
# Modo desarrollo con logs detallados
python main.py --debug --verbose

# Ver logs en tiempo real
tail -f logs/phisher.log
```

## 🎓 Ejercicios Específicos para Termux

### Ejercicio 1: Setup Básico
1. Instalar AdvancedPhisher siguiendo esta guía
2. Verificar que todos los módulos funcionan
3. Iniciar el servidor y acceder localmente
4. Documentar cualquier error encontrado

### Ejercicio 2: Red Local
1. Configurar el servidor para acceso en red local
2. Conectar desde otro dispositivo (PC/móvil)
3. Probar diferentes templates
4. Analizar logs generados

### Ejercicio 3: Personalización
1. Modificar un template existente
2. Añadir elementos específicos para móviles
3. Probar la responsividad
4. Generar reportes de uso

## 📚 Recursos Adicionales

### Documentación Termux
- [Termux Wiki](https://wiki.termux.com/)
- [Termux Packages](https://packages.termux.org/)
- [Python en Termux](https://wiki.termux.com/wiki/Python)

### Comunidad
- [r/termux](https://reddit.com/r/termux)
- [Termux GitHub](https://github.com/termux/termux-app)

## ✅ Checklist de Instalación Exitosa

- [ ] Termux actualizado a la última versión
- [ ] Python 3.8+ instalado
- [ ] pip funcionando correctamente
- [ ] requirements_termux.txt instalado sin errores
- [ ] Directorios del proyecto creados
- [ ] Scripts de inicio con permisos correctos
- [ ] main.py ejecuta sin errores
- [ ] Servidor web accesible en localhost:8080
- [ ] Templates cargan correctamente
- [ ] Logs se generan en logs/

## 🆘 Soporte

Si sigues teniendo problemas:

1. **Ejecuta el diagnóstico:**
   ```bash
   ./check_termux.sh
   ```

2. **Verifica la versión de Termux:**
   ```bash
   pkg list-installed | grep termux
   ```

3. **Reinstalación limpia:**
   ```bash
   rm -rf venv/
   pip cache purge
   ./install_termux.sh
   ```

---

**¡Ahora deberías poder usar AdvancedPhisher sin problemas en Termux!** 📱✨

Recuerda siempre usar esta herramienta de forma ética y educativa. 🎓🔒