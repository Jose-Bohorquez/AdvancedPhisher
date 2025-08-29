#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalación Automática - AdvancedPhisher
Instalador completo para estudiantes y usuarios nuevos

Uso:
    python install.py
    
Este script:
- Verifica requisitos del sistema
- Instala dependencias automáticamente
- Crea directorios necesarios
- Configura el entorno inicial
- Ejecuta pruebas básicas
"""

import os
import sys
import subprocess
import json
import platform
from pathlib import Path
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

class AdvancedPhisherInstaller:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.python_version = sys.version_info
        self.platform = platform.system()
        self.errors = []
        self.warnings = []
        
    def print_banner(self):
        """Mostrar banner de instalación"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    ADVANCEDPHISHER v1.0                     ║
║                  Instalador Automático                      ║
║                                                              ║
║  🎯 Framework Educativo de Phishing para Ciberseguridad     ║
║  ⚠️  SOLO PARA USO ÉTICO Y EDUCATIVO                        ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}Iniciando instalación automática...{Style.RESET_ALL}
"""
        print(banner)
        
    def check_python_version(self):
        """Verificar versión de Python"""
        print(f"{Fore.BLUE}[1/8] Verificando versión de Python...{Style.RESET_ALL}")
        
        if self.python_version < (3, 6):
            self.errors.append(f"Python 3.6+ requerido. Versión actual: {sys.version}")
            print(f"{Fore.RED}❌ Error: Se requiere Python 3.6 o superior{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   Versión actual: {sys.version}{Style.RESET_ALL}")
            return False
        elif self.python_version < (3, 8):
            self.warnings.append(f"Se recomienda Python 3.8+. Versión actual: {sys.version}")
            print(f"{Fore.YELLOW}⚠️  Advertencia: Se recomienda Python 3.8+{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✅ Python {sys.version.split()[0]} detectado (mínimo cumplido){Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}✅ Python {sys.version.split()[0]} detectado{Style.RESET_ALL}")
        
        return True
    
    def check_pip(self):
        """Verificar que pip esté disponible"""
        print(f"{Fore.BLUE}[2/8] Verificando pip...{Style.RESET_ALL}")
        
        try:
            subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                         check=True, capture_output=True)
            print(f"{Fore.GREEN}✅ pip disponible{Style.RESET_ALL}")
            return True
        except subprocess.CalledProcessError:
            self.errors.append("pip no está disponible")
            print(f"{Fore.RED}❌ Error: pip no está disponible{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   Instale pip: python -m ensurepip --upgrade{Style.RESET_ALL}")
            return False
    
    def install_dependencies(self):
        """Instalar dependencias desde requirements.txt"""
        print(f"{Fore.BLUE}[3/8] Instalando dependencias...{Style.RESET_ALL}")
        
        requirements_file = self.base_dir / 'requirements.txt'
        if not requirements_file.exists():
            self.errors.append("Archivo requirements.txt no encontrado")
            print(f"{Fore.RED}❌ Error: requirements.txt no encontrado{Style.RESET_ALL}")
            return False
        
        try:
            print(f"{Fore.YELLOW}   Instalando paquetes de Python...{Style.RESET_ALL}")
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"{Fore.GREEN}✅ Dependencias instaladas correctamente{Style.RESET_ALL}")
                return True
            else:
                self.errors.append(f"Error instalando dependencias: {result.stderr}")
                print(f"{Fore.RED}❌ Error instalando dependencias{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}   {result.stderr[:200]}...{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            self.errors.append(f"Excepción instalando dependencias: {str(e)}")
            print(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")
            return False
    
    def create_directories(self):
        """Crear directorios necesarios"""
        print(f"{Fore.BLUE}[4/8] Creando estructura de directorios...{Style.RESET_ALL}")
        
        directories = [
            'logs',
            'reports', 
            'deployments',
            'certs',
            'logs/screenshots',
            'reports/html',
            'reports/json',
            'reports/csv'
        ]
        
        created_count = 0
        for directory in directories:
            dir_path = self.base_dir / directory
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                created_count += 1
            except Exception as e:
                self.warnings.append(f"No se pudo crear directorio {directory}: {str(e)}")
        
        print(f"{Fore.GREEN}✅ {created_count}/{len(directories)} directorios creados{Style.RESET_ALL}")
        return True
    
    def setup_configuration(self):
        """Configurar archivos de configuración inicial"""
        print(f"{Fore.BLUE}[5/8] Configurando archivos iniciales...{Style.RESET_ALL}")
        
        # Verificar que existe el archivo de configuración
        config_file = self.base_dir / 'config' / 'settings.json'
        if config_file.exists():
            print(f"{Fore.GREEN}✅ Configuración encontrada: {config_file.name}{Style.RESET_ALL}")
        else:
            self.warnings.append("Archivo de configuración no encontrado")
            print(f"{Fore.YELLOW}⚠️  Configuración no encontrada, usando valores por defecto{Style.RESET_ALL}")
        
        # Crear archivo de log inicial
        log_file = self.base_dir / 'logs' / 'installation.log'
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"AdvancedPhisher - Log de Instalación\n")
                f.write(f"Fecha: {__import__('datetime').datetime.now()}\n")
                f.write(f"Python: {sys.version}\n")
                f.write(f"Plataforma: {platform.platform()}\n")
                f.write(f"Directorio: {self.base_dir}\n")
            print(f"{Fore.GREEN}✅ Log de instalación creado{Style.RESET_ALL}")
        except Exception as e:
            self.warnings.append(f"No se pudo crear log de instalación: {str(e)}")
        
        return True
    
    def test_imports(self):
        """Probar importaciones críticas"""
        print(f"{Fore.BLUE}[6/8] Probando importaciones críticas...{Style.RESET_ALL}")
        
        critical_modules = [
            ('colorama', 'Colores en terminal'),
            ('flask', 'Servidor web'),
            ('requests', 'Cliente HTTP'),
            ('jinja2', 'Motor de plantillas'),
            ('cryptography', 'Criptografía y SSL')
        ]
        
        success_count = 0
        for module_name, description in critical_modules:
            try:
                __import__(module_name)
                print(f"{Fore.GREEN}  ✅ {module_name} - {description}{Style.RESET_ALL}")
                success_count += 1
            except ImportError:
                print(f"{Fore.RED}  ❌ {module_name} - {description}{Style.RESET_ALL}")
                self.errors.append(f"Módulo {module_name} no disponible")
        
        if success_count == len(critical_modules):
            print(f"{Fore.GREEN}✅ Todas las importaciones exitosas{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.YELLOW}⚠️  {success_count}/{len(critical_modules)} importaciones exitosas{Style.RESET_ALL}")
            return success_count > len(critical_modules) // 2
    
    def test_core_modules(self):
        """Probar módulos del core"""
        print(f"{Fore.BLUE}[7/8] Probando módulos del core...{Style.RESET_ALL}")
        
        # Agregar directorio core al path temporalmente
        core_path = str(self.base_dir / 'core')
        if core_path not in sys.path:
            sys.path.insert(0, core_path)
        
        core_modules = [
            'logger',
            'domain_manager', 
            'web_server',
            'console'
        ]
        
        success_count = 0
        for module_name in core_modules:
            try:
                __import__(f'core.{module_name}')
                print(f"{Fore.GREEN}  ✅ core.{module_name}{Style.RESET_ALL}")
                success_count += 1
            except ImportError as e:
                print(f"{Fore.RED}  ❌ core.{module_name} - {str(e)[:50]}...{Style.RESET_ALL}")
                self.errors.append(f"Módulo core.{module_name} no disponible")
        
        if success_count == len(core_modules):
            print(f"{Fore.GREEN}✅ Todos los módulos del core disponibles{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.YELLOW}⚠️  {success_count}/{len(core_modules)} módulos del core disponibles{Style.RESET_ALL}")
            return success_count > 0
    
    def final_verification(self):
        """Verificación final y resumen"""
        print(f"{Fore.BLUE}[8/8] Verificación final...{Style.RESET_ALL}")
        
        # Verificar que main.py existe
        main_file = self.base_dir / 'main.py'
        if main_file.exists():
            print(f"{Fore.GREEN}✅ Archivo principal encontrado: main.py{Style.RESET_ALL}")
        else:
            self.errors.append("main.py no encontrado")
            print(f"{Fore.RED}❌ main.py no encontrado{Style.RESET_ALL}")
        
        # Verificar templates
        templates_dir = self.base_dir / 'templates'
        if templates_dir.exists():
            template_count = len(list(templates_dir.glob('*.html')))
            print(f"{Fore.GREEN}✅ {template_count} templates encontrados{Style.RESET_ALL}")
        else:
            self.warnings.append("Directorio templates no encontrado")
        
        return len(self.errors) == 0
    
    def show_summary(self):
        """Mostrar resumen de instalación"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}           RESUMEN DE INSTALACIÓN{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        if len(self.errors) == 0:
            print(f"{Fore.GREEN}🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!{Style.RESET_ALL}")
            print(f"\n{Fore.GREEN}✅ AdvancedPhisher está listo para usar{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}Para iniciar la aplicación:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}   python main.py{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}Para ver la ayuda:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}   python main.py --help{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ INSTALACIÓN COMPLETADA CON ERRORES{Style.RESET_ALL}")
            print(f"\n{Fore.RED}Errores encontrados:{Style.RESET_ALL}")
            for i, error in enumerate(self.errors, 1):
                print(f"{Fore.RED}  {i}. {error}{Style.RESET_ALL}")
        
        if len(self.warnings) > 0:
            print(f"\n{Fore.YELLOW}Advertencias:{Style.RESET_ALL}")
            for i, warning in enumerate(self.warnings, 1):
                print(f"{Fore.YELLOW}  {i}. {warning}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Información del sistema:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  Python: {sys.version.split()[0]}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  Plataforma: {platform.platform()}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  Directorio: {self.base_dir}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}⚠️  RECORDATORIO IMPORTANTE:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   Esta herramienta es SOLO para uso educativo y ético.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   Lea la documentación ética antes de usar.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    def run_installation(self):
        """Ejecutar proceso completo de instalación"""
        self.print_banner()
        
        steps = [
            self.check_python_version,
            self.check_pip,
            self.install_dependencies,
            self.create_directories,
            self.setup_configuration,
            self.test_imports,
            self.test_core_modules,
            self.final_verification
        ]
        
        for step in steps:
            if not step():
                if len(self.errors) > 0:
                    print(f"\n{Fore.RED}Instalación detenida debido a errores críticos.{Style.RESET_ALL}")
                    break
            print()  # Línea en blanco entre pasos
        
        self.show_summary()
        return len(self.errors) == 0

def main():
    """Función principal del instalador"""
    try:
        installer = AdvancedPhisherInstaller()
        success = installer.run_installation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Instalación cancelada por el usuario.{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Error fatal durante la instalación: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()