#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AdvancedPhisher - Framework avanzado de phishing para educación en ciberseguridad
Versión: 1.0
Autor: Security Research Team

⚠️ ADVERTENCIA: Esta herramienta está diseñada ÚNICAMENTE para:
- Educación en Ciberseguridad
- Pruebas de Penetración Autorizadas
- Investigación de Seguridad

El uso malicioso de esta herramienta es ILEGAL y está PROHIBIDO.
Los autores no se hacen responsables del mal uso de esta herramienta.
"""

import os
import sys
import json
from pathlib import Path
from colorama import Fore, Style, init

# Agregar el directorio core al path
sys.path.append(str(Path(__file__).parent / 'core'))

# Importar módulos del core
from core.domain_manager import DomainManager
from core.web_server import AdvancedWebServer
from core.logger import Logger
from core.console import ConsoleInterface

# Inicializar colorama para colores en terminal
init(autoreset=True)

class AdvancedPhisher:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.config = self.load_config()
        
        # Crear directorios necesarios
        self.create_directories()
        
        # Inicializar componentes
        self.logger = Logger(self.config.get('logging', {}))
        self.domain_manager = DomainManager()
        self.web_server = AdvancedWebServer(self.domain_manager, self.logger, self.config)
        self.console = ConsoleInterface(self.domain_manager, self.web_server, self.logger, self.config)
        
        # Log inicio de aplicación
        self.logger.system_event('APPLICATION_START', 'AdvancedPhisher iniciado', {
            'version': self.config.get('general', {}).get('version', '1.0'),
            'python_version': sys.version,
            'platform': sys.platform
        })
        
    def create_directories(self):
        """Crear estructura de directorios"""
        directories = [
            'templates',
            'logs',
            'reports',
            'certs',
            'config',
            'domains',
            'core',
            'utils'
        ]
        
        for directory in directories:
            dir_path = self.base_dir / directory
            dir_path.mkdir(exist_ok=True)
            
    def load_config(self):
        """Cargar configuración principal"""
        config_file = self.base_dir / 'config' / 'settings.json'
        
        # Configuración por defecto
        default_config = {
            "general": {
                "version": "1.0",
                "author": "Security Research Team",
                "default_port": 8080,
                "ssl_enabled": True,
                "auto_deploy": False,
                "stealth_mode": True,
                "session_timeout": 3600
            },
            "logging": {
                "level": "INFO",
                "console_output": True,
                "file_output": True,
                "max_log_size": "10MB",
                "log_format": "%(asctime)s - %(levelname)s - %(message)s",
                "console_logging": True,
                "max_logs_per_file": 10000
            },
            "security": {
                "rate_limiting": {
                    "enabled": True,
                    "requests_per_minute": 60,
                    "burst_limit": 10
                },
                "ip_blocking": {
                    "enabled": True,
                    "auto_block_suspicious": True,
                    "whitelist": ["127.0.0.1", "localhost"]
                },
                "honeypot": {
                    "enabled": False,
                    "fake_admin_panel": True
                }
            },
            "server": {
                "bind_address": "0.0.0.0",
                "worker_processes": 4,
                "custom_headers": {
                    "Server": "nginx/1.18.0",
                    "X-Powered-By": "PHP/7.4.3"
                }
            }
        }
        
        try:
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge con configuración por defecto
                    self._merge_config(default_config, loaded_config)
                    return default_config
            else:
                return default_config
        except Exception as e:
            print(f"{Fore.RED}Error cargando configuración: {str(e)}{Style.RESET_ALL}")
            return default_config
            
    def _merge_config(self, default, loaded):
        """Fusionar configuraciones recursivamente"""
        for key, value in loaded.items():
            if key in default:
                if isinstance(default[key], dict) and isinstance(value, dict):
                    self._merge_config(default[key], value)
                else:
                    default[key] = value
            else:
                default[key] = value
        
    def run(self):
        """Ejecutar aplicación principal"""
        try:
            # Ejecutar interfaz de consola
            self.console.run()
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Saliendo...{Style.RESET_ALL}")
            self.exit_application()
        except Exception as e:
            self.logger.critical(f"Error crítico en aplicación principal: {str(e)}")
            print(f"{Fore.RED}Error crítico: {str(e)}{Style.RESET_ALL}")
            sys.exit(1)
            
    def exit_application(self):
        """Salir de la aplicación"""
        # Detener servidor si está activo
        if self.web_server.is_running():
            self.web_server.stop_server()
            
        # Log cierre de aplicación
        self.logger.system_event('APPLICATION_STOP', 'AdvancedPhisher cerrado')
        
        print(f"{Fore.GREEN}¡Gracias por usar AdvancedPhisher!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Recuerde usar esta herramienta de forma ética y responsable.{Style.RESET_ALL}")
        sys.exit(0)

def check_dependencies():
    """Verificar dependencias requeridas"""
    required_modules = [
        'colorama', 'flask', 'requests', 'cryptography', 
        'rich', 'tabulate', 'jinja2', 'werkzeug'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
            
    if missing_modules:
        print(f"{Fore.RED}Error: Faltan dependencias requeridas:{Style.RESET_ALL}")
        for module in missing_modules:
            print(f"{Fore.YELLOW}  - {module}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Instale las dependencias con:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  pip install -r requirements.txt{Style.RESET_ALL}")
        return False
        
    return True

def show_legal_warning():
    """Mostrar advertencia legal"""
    print(f"{Fore.RED}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.RED}                        ⚠️  ADVERTENCIA LEGAL  ⚠️{Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Esta herramienta está diseñada ÚNICAMENTE para:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}• Educación en Ciberseguridad{Style.RESET_ALL}")
    print(f"{Fore.GREEN}• Pruebas de Penetración Autorizadas{Style.RESET_ALL}")
    print(f"{Fore.GREEN}• Investigación de Seguridad{Style.RESET_ALL}")
    print()
    print(f"{Fore.RED}El uso malicioso de esta herramienta es ILEGAL.{Style.RESET_ALL}")
    print(f"{Fore.RED}Los autores no se hacen responsables del mal uso.{Style.RESET_ALL}")
    print(f"{Fore.RED}Usted es completamente responsable de sus acciones.{Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*70}{Style.RESET_ALL}")
    print()
    
    # Solicitar confirmación
    confirm = input(f"{Fore.CYAN}¿Acepta usar esta herramienta de forma ética y legal? (s/N): {Style.RESET_ALL}")
    if not confirm.lower().startswith('s'):
        print(f"{Fore.YELLOW}Uso no autorizado. Saliendo...{Style.RESET_ALL}")
        return False
        
    return True

def main():
    """Función principal"""
    # Verificar Python 3.6+
    if sys.version_info < (3, 6):
        print(f"{Fore.RED}Error: Se requiere Python 3.6 o superior{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Versión actual: {sys.version}{Style.RESET_ALL}")
        sys.exit(1)
        
    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)
        
    # Mostrar advertencia legal
    if not show_legal_warning():
        sys.exit(0)
        
    try:
        # Iniciar aplicación
        app = AdvancedPhisher()
        app.run()
    except Exception as e:
        print(f"{Fore.RED}Error fatal iniciando aplicación: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()