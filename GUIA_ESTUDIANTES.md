# 📚 Guía para Estudiantes - AdvancedPhisher

## 🎯 Introducción

Esta guía está diseñada específicamente para estudiantes que están aprendiendo sobre ciberseguridad y phishing ético. AdvancedPhisher es una herramienta educativa que simula ataques de phishing para enseñar sobre:

- Técnicas de ingeniería social
- Vulnerabilidades en la autenticación web
- Métodos de detección y prevención
- Análisis de comportamiento de usuarios

## ⚠️ IMPORTANTE: Uso Ético Obligatorio

**ANTES DE CONTINUAR, LEA ESTO CUIDADOSAMENTE:**

✅ **PERMITIDO:**
- Usar en laboratorios controlados
- Practicar en redes propias
- Demostrar vulnerabilidades a colegas con consentimiento
- Investigación académica autorizada
- Entrenamientos de concientización empresarial autorizados

❌ **PROHIBIDO:**
- Usar contra personas sin consentimiento
- Atacar sistemas que no te pertenecen
- Recopilar credenciales reales sin autorización
- Usar para actividades maliciosas
- Distribuir credenciales obtenidas

## 🚀 Primeros Pasos

### 1. Verificar la Instalación

Después de ejecutar el instalador, verifica que todo esté funcionando:

```bash
# Verificar que Python puede importar los módulos
python -c "import flask, requests; print('✅ Dependencias OK')"

# Verificar que el archivo principal existe
ls main.py  # Linux/macOS
dir main.py  # Windows
```

### 2. Primera Ejecución

#### Opción A: Script de Inicio Rápido
```bash
# Windows
start_advancedphisher.bat

# Linux/macOS
./start_advancedphisher.sh
```

#### Opción B: Comando Directo
```bash
python main.py
```

### 3. Interfaz de Consola

Al iniciar, verás un menú como este:

```
╔══════════════════════════════════════════════════════════════╗
║                    ADVANCEDPHISHER v1.0                     ║
║                Framework de Phishing Ético                  ║
╚══════════════════════════════════════════════════════════════╝

[1] Gestionar Templates
[2] Configurar Dominios
[3] Iniciar Servidor
[4] Ver Reportes
[5] Configuración
[0] Salir

Seleccione una opción:
```

## 📋 Guía Paso a Paso

### Paso 1: Configuración Inicial

1. **Selecciona opción [5] Configuración**
2. **Revisa la configuración básica:**
   - Puerto del servidor (por defecto: 8080)
   - Modo stealth (recomendado: activado)
   - Logging (recomendado: activado)

### Paso 2: Seleccionar Template

1. **Selecciona opción [1] Gestionar Templates**
2. **Elige una plataforma:**
   - Facebook (más realista)
   - Google (incluye 2FA)
   - Instagram (diseño moderno)
   - LinkedIn (profesional)
   - TikTok (juvenil)

3. **Personaliza el template si es necesario**

### Paso 3: Configurar Dominio (Opcional)

1. **Selecciona opción [2] Configurar Dominios**
2. **Para práctica local, usa:**
   - `localhost:8080`
   - `127.0.0.1:8080`

### Paso 4: Iniciar el Servidor

1. **Selecciona opción [3] Iniciar Servidor**
2. **El servidor se iniciará y mostrará:**
   ```
   🚀 Servidor iniciado en: http://localhost:8080
   📊 Panel de control: http://localhost:8080/admin
   📝 Logs en tiempo real: logs/phisher.log
   ```

### Paso 5: Probar la Simulación

1. **Abre tu navegador web**
2. **Visita:** `http://localhost:8080`
3. **Observa el template cargado**
4. **Prueba introducir credenciales de prueba**

### Paso 6: Analizar Resultados

1. **Regresa a la consola**
2. **Selecciona opción [4] Ver Reportes**
3. **Revisa:**
   - Intentos de login capturados
   - Información del navegador
   - Geolocalización (si está habilitada)
   - Timestamps de acceso

## 🔧 Configuración Avanzada

### Personalizar Templates

```bash
# Los templates están en:
cd templates/

# Estructura:
templates/
├── facebook/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── google/
├── instagram/
└── ...
```

### Modificar Configuración

Edita el archivo `config/settings.json`:

```json
{
  "general": {
    "port": 8080,
    "ssl_enabled": false,
    "stealth_mode": true
  },
  "logging": {
    "level": "INFO",
    "log_to_file": true,
    "log_to_console": true
  },
  "security": {
    "rate_limiting": true,
    "max_requests_per_minute": 60
  }
}
```

## 📊 Interpretando Resultados

### Logs del Sistema

Los logs se guardan en `logs/phisher.log`:

```
2024-01-15 10:30:15 - INFO - Servidor iniciado en puerto 8080
2024-01-15 10:31:22 - INFO - Acceso desde 192.168.1.100 - Chrome/120.0
2024-01-15 10:31:45 - WARNING - Intento de login capturado
2024-01-15 10:31:45 - INFO - Usuario: test@example.com
```

### Reportes Detallados

Los reportes se generan en `reports/`:

- `session_YYYYMMDD_HHMMSS.json` - Datos de sesión
- `analytics_YYYYMMDD.html` - Reporte visual
- `summary.txt` - Resumen de actividad

## 🛡️ Detección y Prevención

### Señales de Phishing que Debes Enseñar

1. **URL sospechosas:**
   - Dominios similares pero incorrectos
   - Uso de HTTP en lugar de HTTPS
   - Subdominios extraños

2. **Diseño inconsistente:**
   - Logos de baja calidad
   - Errores ortográficos
   - Colores o fuentes incorrectas

3. **Comportamiento anómalo:**
   - Redirecciones inesperadas
   - Solicitudes urgentes
   - Falta de verificación 2FA

### Medidas de Protección

1. **Para usuarios:**
   - Verificar siempre la URL
   - Usar autenticación de dos factores
   - No hacer clic en enlaces sospechosos
   - Verificar certificados SSL

2. **Para organizaciones:**
   - Filtros de email avanzados
   - Entrenamiento regular de empleados
   - Políticas de seguridad claras
   - Monitoreo de dominios similares

## 🔍 Ejercicios Prácticos

### Ejercicio 1: Análisis de Template
1. Ejecuta el template de Facebook
2. Compáralo con el sitio real
3. Identifica 5 diferencias
4. Documenta cómo mejorar la detección

### Ejercicio 2: Personalización
1. Modifica el template de Google
2. Añade tu logo institucional
3. Cambia los colores
4. Prueba la efectividad

### Ejercicio 3: Análisis de Logs
1. Genera 10 intentos de login
2. Analiza los logs generados
3. Crea un reporte de incidentes
4. Propón medidas preventivas

## 🚨 Solución de Problemas

### Error: "Puerto ya en uso"
```bash
# Cambiar puerto
python main.py --port 8081

# O matar proceso existente
# Windows:
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Linux/macOS:
lsof -ti:8080 | xargs kill -9
```

### Error: "Módulo no encontrado"
```bash
# Reinstalar dependencias
pip install -r requirements.txt

# Verificar entorno virtual
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### Error: "Permisos denegados"
```bash
# Linux/macOS - dar permisos
chmod +x start_advancedphisher.sh
sudo chown -R $USER:$USER .

# Windows - ejecutar como administrador
```

## 📚 Recursos Adicionales

### Documentación
- `README.md` - Información general
- `docs/ethical_usage_guide.md` - Guía de uso ético
- `docs/api_reference.md` - Referencia de API

### Comunidad y Soporte
- Issues en GitHub para reportar bugs
- Discusiones para preguntas generales
- Wiki para documentación extendida

### Lecturas Recomendadas
1. "The Art of Deception" - Kevin Mitnick
2. "Social Engineering: The Science of Human Hacking" - Christopher Hadnagy
3. OWASP Testing Guide - Web Application Security
4. NIST Cybersecurity Framework

## ✅ Lista de Verificación Final

Antes de usar AdvancedPhisher en clase:

- [ ] He leído y entendido las implicaciones éticas
- [ ] Tengo autorización para usar la herramienta
- [ ] He configurado un entorno controlado
- [ ] He probado todas las funcionalidades
- [ ] He preparado ejercicios específicos
- [ ] He documentado los objetivos de aprendizaje
- [ ] Tengo un plan para la discusión post-ejercicio

---

**Recuerda:** El objetivo es educar sobre ciberseguridad, no enseñar a atacar. Siempre enfatiza la importancia de la ética y la responsabilidad en el uso de estas herramientas.

¡Feliz aprendizaje! 🎓🔒