# 📱 Guía de Instalación y Uso en Termux (Android)

## 🎯 Introducción

Esta guía te ayudará a instalar y usar AdvancedPhisher en Termux (Android). Termux tiene algunas limitaciones específicas que hemos optimizado para ti.

## ⚠️ Problema Identificado

El error que experimentaste es común en Termux debido a:

```
Unsupported platform: 312
Rust not found, installing into a temporary directory
```

**Causa:** La librería `cryptography` requiere compilación de Rust, que no está disponible en Android/Termux para Python 3.12.

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

## 📋 Diferencias del Requirements Termux

### ❌ Dependencias Removidas (Problemáticas en Termux)
- `cryptography>=41.0.4` → Reemplazada por `pycryptodome`
- `netifaces>=0.11.0` → Reemplazada por `ifaddr`
- `paramiko>=3.3.1` → Removida (SSH opcional)
- `scapy>=2.5.0` → Removida (requiere privilegios root)
- `dnspython>=2.4.2` → Removida (funcionalidad opcional)

### ✅ Dependencias Optimizadas
- `pycryptodome==3.19.0` → Criptografía sin Rust
- `ifaddr==0.2.0` → Información de red básica
- `fake-useragent==1.4.0` → User agents sin dependencias pesadas
- `httpx==0.25.0` → Cliente HTTP moderno y ligero

## 🔧 Scripts Específicos para Termux

### Iniciar AdvancedPhisher
```bash
./start_termux.sh
```

### Verificar Instalación
```bash
./check_termux.sh
```

### Inicio Manual
```bash
python main.py
```

## 🚨 Solución de Problemas Comunes

### Error: "cryptography compilation failed"
**Solución:**
```bash
# Usar el requirements optimizado
pip uninstall cryptography
pip install -r requirements_termux.txt
```

### Error: "netifaces build failed"
**Solución:**
```bash
# Instalar alternativa ligera
pip install ifaddr
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
# Verificar instalación
./check_termux.sh

# Reinstalar dependencias básicas
pip install flask requests pandas colorama
```

### Error: "Port already in use"
**Solución:**
```bash
# Usar puerto diferente
python main.py --port 8081

# O matar procesos existentes
pkill -f "python.*main.py"
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