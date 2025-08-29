#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Reportes Avanzados para AdvancedPhisher
Genera reportes detallados en múltiples formatos con análisis de datos
"""

import os
import json
import csv
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template
import pandas as pd
from collections import Counter, defaultdict
import base64
from io import BytesIO

@dataclass
class ReportConfig:
    """Configuración para generación de reportes"""
    title: str = "Reporte AdvancedPhisher"
    period_hours: int = 24
    include_charts: bool = True
    include_raw_data: bool = False
    max_records: int = 1000
    output_format: str = "html"  # html, json, csv, pdf
    theme: str = "dark"  # dark, light

class ReportGenerator:
    """Generador de reportes avanzados"""
    
    def __init__(self, db_path: str, output_dir: str = "reports"):
        self.db_path = Path(db_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configurar matplotlib para generar gráficos
        plt.style.use('dark_background')
        sns.set_palette("husl")
        
    def generate_comprehensive_report(self, config: ReportConfig) -> Dict[str, Any]:
        """Generar reporte completo con análisis avanzado"""
        try:
            # Obtener datos de la base de datos
            data = self._fetch_data(config.period_hours, config.max_records)
            
            # Realizar análisis
            analysis = self._perform_analysis(data)
            
            # Generar gráficos si está habilitado
            charts = {}
            if config.include_charts:
                charts = self._generate_charts(data, analysis)
            
            # Compilar reporte
            report = {
                'metadata': {
                    'title': config.title,
                    'generated_at': datetime.now().isoformat(),
                    'period_hours': config.period_hours,
                    'total_records': len(data.get('visits', [])) + len(data.get('captures', []))
                },
                'summary': analysis['summary'],
                'detailed_analysis': analysis['detailed'],
                'charts': charts,
                'raw_data': data if config.include_raw_data else None
            }
            
            return report
            
        except Exception as e:
            raise Exception(f"Error generando reporte: {str(e)}")
    
    def _fetch_data(self, period_hours: int, max_records: int) -> Dict[str, List]:
        """Obtener datos de la base de datos"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        
        since = (datetime.now() - timedelta(hours=period_hours)).isoformat()
        
        # Obtener visitas
        visits_query = '''
            SELECT * FROM visits 
            WHERE timestamp > ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        '''
        visits = [dict(row) for row in conn.execute(visits_query, (since, max_records)).fetchall()]
        
        # Obtener capturas
        captures_query = '''
            SELECT * FROM captures 
            WHERE timestamp > ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        '''
        captures = [dict(row) for row in conn.execute(captures_query, (since, max_records)).fetchall()]
        
        # Obtener errores
        errors_query = '''
            SELECT * FROM errors 
            WHERE timestamp > ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        '''
        errors = [dict(row) for row in conn.execute(errors_query, (since, max_records)).fetchall()]
        
        conn.close()
        
        return {
            'visits': visits,
            'captures': captures,
            'errors': errors
        }
    
    def _perform_analysis(self, data: Dict[str, List]) -> Dict[str, Any]:
        """Realizar análisis avanzado de los datos"""
        visits = data['visits']
        captures = data['captures']
        errors = data['errors']
        
        # Análisis de resumen
        summary = {
            'total_visits': len(visits),
            'total_captures': len(captures),
            'total_errors': len(errors),
            'success_rate': (len(captures) / len(visits) * 100) if visits else 0,
            'unique_ips': len(set(v['ip'] for v in visits)),
            'most_active_hour': self._get_most_active_hour(visits),
            'top_template': self._get_top_template(captures),
            'error_rate': (len(errors) / (len(visits) + len(captures)) * 100) if (visits or captures) else 0
        }
        
        # Análisis detallado
        detailed = {
            'geographic_distribution': self._analyze_geographic_distribution(visits),
            'temporal_patterns': self._analyze_temporal_patterns(visits, captures),
            'user_agent_analysis': self._analyze_user_agents(visits),
            'template_performance': self._analyze_template_performance(captures),
            'ip_analysis': self._analyze_ip_patterns(visits, captures),
            'error_analysis': self._analyze_errors(errors),
            'security_insights': self._analyze_security_patterns(visits, captures)
        }
        
        return {
            'summary': summary,
            'detailed': detailed
        }
    
    def _get_most_active_hour(self, visits: List[Dict]) -> int:
        """Obtener la hora más activa"""
        if not visits:
            return 0
        
        hours = []
        for visit in visits:
            try:
                dt = datetime.fromisoformat(visit['timestamp'])
                hours.append(dt.hour)
            except:
                continue
        
        return Counter(hours).most_common(1)[0][0] if hours else 0
    
    def _get_top_template(self, captures: List[Dict]) -> str:
        """Obtener el template más exitoso"""
        if not captures:
            return "N/A"
        
        templates = [c.get('template', 'unknown') for c in captures]
        return Counter(templates).most_common(1)[0][0] if templates else "N/A"
    
    def _analyze_geographic_distribution(self, visits: List[Dict]) -> Dict:
        """Analizar distribución geográfica"""
        geo_data = defaultdict(int)
        
        for visit in visits:
            geo_info = visit.get('geo_info')
            if geo_info:
                try:
                    geo = json.loads(geo_info) if isinstance(geo_info, str) else geo_info
                    country = geo.get('country', 'Unknown')
                    geo_data[country] += 1
                except:
                    geo_data['Unknown'] += 1
            else:
                geo_data['Unknown'] += 1
        
        return dict(geo_data)
    
    def _analyze_temporal_patterns(self, visits: List[Dict], captures: List[Dict]) -> Dict:
        """Analizar patrones temporales"""
        hourly_visits = defaultdict(int)
        hourly_captures = defaultdict(int)
        daily_activity = defaultdict(int)
        
        for visit in visits:
            try:
                dt = datetime.fromisoformat(visit['timestamp'])
                hourly_visits[dt.hour] += 1
                daily_activity[dt.strftime('%Y-%m-%d')] += 1
            except:
                continue
        
        for capture in captures:
            try:
                dt = datetime.fromisoformat(capture['timestamp'])
                hourly_captures[dt.hour] += 1
            except:
                continue
        
        return {
            'hourly_visits': dict(hourly_visits),
            'hourly_captures': dict(hourly_captures),
            'daily_activity': dict(daily_activity)
        }
    
    def _analyze_user_agents(self, visits: List[Dict]) -> Dict:
        """Analizar User Agents"""
        browsers = defaultdict(int)
        os_systems = defaultdict(int)
        devices = defaultdict(int)
        
        for visit in visits:
            ua = visit.get('user_agent', '')
            if ua:
                # Análisis básico de User Agent
                if 'Chrome' in ua:
                    browsers['Chrome'] += 1
                elif 'Firefox' in ua:
                    browsers['Firefox'] += 1
                elif 'Safari' in ua:
                    browsers['Safari'] += 1
                elif 'Edge' in ua:
                    browsers['Edge'] += 1
                else:
                    browsers['Other'] += 1
                
                if 'Windows' in ua:
                    os_systems['Windows'] += 1
                elif 'Mac' in ua:
                    os_systems['macOS'] += 1
                elif 'Linux' in ua:
                    os_systems['Linux'] += 1
                elif 'Android' in ua:
                    os_systems['Android'] += 1
                elif 'iOS' in ua:
                    os_systems['iOS'] += 1
                else:
                    os_systems['Other'] += 1
                
                if 'Mobile' in ua:
                    devices['Mobile'] += 1
                elif 'Tablet' in ua:
                    devices['Tablet'] += 1
                else:
                    devices['Desktop'] += 1
        
        return {
            'browsers': dict(browsers),
            'operating_systems': dict(os_systems),
            'devices': dict(devices)
        }
    
    def _analyze_template_performance(self, captures: List[Dict]) -> Dict:
        """Analizar rendimiento de templates"""
        template_stats = defaultdict(lambda: {'captures': 0, 'domains': set()})
        
        for capture in captures:
            template = capture.get('template', 'unknown')
            domain = capture.get('domain', 'unknown')
            
            template_stats[template]['captures'] += 1
            template_stats[template]['domains'].add(domain)
        
        # Convertir sets a listas para serialización JSON
        result = {}
        for template, stats in template_stats.items():
            result[template] = {
                'captures': stats['captures'],
                'unique_domains': len(stats['domains']),
                'domains': list(stats['domains'])
            }
        
        return result
    
    def _analyze_ip_patterns(self, visits: List[Dict], captures: List[Dict]) -> Dict:
        """Analizar patrones de IPs"""
        ip_stats = defaultdict(lambda: {'visits': 0, 'captures': 0})
        
        for visit in visits:
            ip = visit.get('ip', 'unknown')
            ip_stats[ip]['visits'] += 1
        
        for capture in captures:
            ip = capture.get('ip', 'unknown')
            ip_stats[ip]['captures'] += 1
        
        # Identificar IPs más activas
        top_ips = sorted(
            ip_stats.items(),
            key=lambda x: x[1]['visits'] + x[1]['captures'],
            reverse=True
        )[:10]
        
        return {
            'total_unique_ips': len(ip_stats),
            'top_ips': dict(top_ips),
            'repeat_visitors': len([ip for ip, stats in ip_stats.items() if stats['visits'] > 1])
        }
    
    def _analyze_errors(self, errors: List[Dict]) -> Dict:
        """Analizar errores del sistema"""
        error_levels = defaultdict(int)
        error_modules = defaultdict(int)
        recent_errors = []
        
        for error in errors:
            level = error.get('level', 'UNKNOWN')
            module = error.get('module', 'unknown')
            
            error_levels[level] += 1
            error_modules[module] += 1
            
            if len(recent_errors) < 5:
                recent_errors.append({
                    'timestamp': error.get('timestamp'),
                    'level': level,
                    'message': error.get('message', '')[:100] + '...' if len(error.get('message', '')) > 100 else error.get('message', '')
                })
        
        return {
            'by_level': dict(error_levels),
            'by_module': dict(error_modules),
            'recent_errors': recent_errors
        }
    
    def _analyze_security_patterns(self, visits: List[Dict], captures: List[Dict]) -> Dict:
        """Analizar patrones de seguridad"""
        suspicious_patterns = {
            'multiple_attempts_same_ip': 0,
            'rapid_succession_visits': 0,
            'unusual_user_agents': 0,
            'potential_bots': 0
        }
        
        # Análisis de IPs con múltiples intentos
        ip_attempts = defaultdict(int)
        for capture in captures:
            ip_attempts[capture.get('ip', '')] += 1
        
        suspicious_patterns['multiple_attempts_same_ip'] = len(
            [ip for ip, count in ip_attempts.items() if count > 3]
        )
        
        # Análisis de User Agents sospechosos
        suspicious_ua_keywords = ['bot', 'crawler', 'spider', 'scraper']
        for visit in visits:
            ua = visit.get('user_agent', '').lower()
            if any(keyword in ua for keyword in suspicious_ua_keywords):
                suspicious_patterns['potential_bots'] += 1
        
        return suspicious_patterns
    
    def _generate_charts(self, data: Dict[str, List], analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generar gráficos en base64"""
        charts = {}
        
        try:
            # Gráfico de actividad temporal
            charts['temporal_activity'] = self._create_temporal_chart(
                analysis['detailed']['temporal_patterns']
            )
            
            # Gráfico de distribución geográfica
            charts['geographic_distribution'] = self._create_geographic_chart(
                analysis['detailed']['geographic_distribution']
            )
            
            # Gráfico de rendimiento de templates
            charts['template_performance'] = self._create_template_chart(
                analysis['detailed']['template_performance']
            )
            
            # Gráfico de análisis de navegadores
            charts['browser_analysis'] = self._create_browser_chart(
                analysis['detailed']['user_agent_analysis']['browsers']
            )
            
        except Exception as e:
            print(f"Error generando gráficos: {e}")
        
        return charts
    
    def _create_temporal_chart(self, temporal_data: Dict) -> str:
        """Crear gráfico de actividad temporal"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Gráfico de actividad por hora
        hourly_visits = temporal_data.get('hourly_visits', {})
        hourly_captures = temporal_data.get('hourly_captures', {})
        
        hours = list(range(24))
        visits_by_hour = [hourly_visits.get(h, 0) for h in hours]
        captures_by_hour = [hourly_captures.get(h, 0) for h in hours]
        
        ax1.plot(hours, visits_by_hour, label='Visitas', marker='o')
        ax1.plot(hours, captures_by_hour, label='Capturas', marker='s')
        ax1.set_title('Actividad por Hora del Día')
        ax1.set_xlabel('Hora')
        ax1.set_ylabel('Cantidad')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Gráfico de actividad diaria
        daily_activity = temporal_data.get('daily_activity', {})
        if daily_activity:
            dates = list(daily_activity.keys())
            values = list(daily_activity.values())
            
            ax2.bar(dates, values, alpha=0.7)
            ax2.set_title('Actividad Diaria')
            ax2.set_xlabel('Fecha')
            ax2.set_ylabel('Visitas')
            ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _create_geographic_chart(self, geo_data: Dict) -> str:
        """Crear gráfico de distribución geográfica"""
        if not geo_data:
            return ""
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        countries = list(geo_data.keys())[:10]  # Top 10 países
        counts = [geo_data[country] for country in countries]
        
        bars = ax.bar(countries, counts, alpha=0.8)
        ax.set_title('Distribución Geográfica (Top 10 Países)')
        ax.set_xlabel('País')
        ax.set_ylabel('Visitas')
        ax.tick_params(axis='x', rotation=45)
        
        # Añadir valores en las barras
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                   str(count), ha='center', va='bottom')
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _create_template_chart(self, template_data: Dict) -> str:
        """Crear gráfico de rendimiento de templates"""
        if not template_data:
            return ""
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        templates = list(template_data.keys())
        captures = [template_data[t]['captures'] for t in templates]
        
        bars = ax.bar(templates, captures, alpha=0.8)
        ax.set_title('Rendimiento de Templates')
        ax.set_xlabel('Template')
        ax.set_ylabel('Capturas')
        ax.tick_params(axis='x', rotation=45)
        
        # Añadir valores en las barras
        for bar, count in zip(bars, captures):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                   str(count), ha='center', va='bottom')
        
        plt.tight_layout()
        return self._fig_to_base64(fig)
    
    def _create_browser_chart(self, browser_data: Dict) -> str:
        """Crear gráfico de análisis de navegadores"""
        if not browser_data:
            return ""
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        browsers = list(browser_data.keys())
        counts = list(browser_data.values())
        
        ax.pie(counts, labels=browsers, autopct='%1.1f%%', startangle=90)
        ax.set_title('Distribución de Navegadores')
        
        return self._fig_to_base64(fig)
    
    def _fig_to_base64(self, fig) -> str:
        """Convertir figura matplotlib a base64"""
        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        return image_base64
    
    def export_html_report(self, report_data: Dict[str, Any], filename: str = None) -> str:
        """Exportar reporte en formato HTML"""
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        html_template = self._get_html_template()
        template = Template(html_template)
        
        html_content = template.render(
            report=report_data,
            generated_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)
    
    def export_json_report(self, report_data: Dict[str, Any], filename: str = None) -> str:
        """Exportar reporte en formato JSON"""
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
        
        return str(output_path)
    
    def export_csv_report(self, report_data: Dict[str, Any], filename: str = None) -> str:
        """Exportar reporte en formato CSV"""
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Escribir resumen
            writer.writerow(['Métrica', 'Valor'])
            summary = report_data.get('summary', {})
            for key, value in summary.items():
                writer.writerow([key, value])
            
            writer.writerow([])  # Línea vacía
            
            # Escribir datos detallados si están disponibles
            if report_data.get('raw_data'):
                raw_data = report_data['raw_data']
                
                # Visitas
                if raw_data.get('visits'):
                    writer.writerow(['=== VISITAS ==='])
                    visits = raw_data['visits']
                    if visits:
                        headers = visits[0].keys()
                        writer.writerow(headers)
                        for visit in visits:
                            writer.writerow([visit.get(h, '') for h in headers])
                    writer.writerow([])
                
                # Capturas
                if raw_data.get('captures'):
                    writer.writerow(['=== CAPTURAS ==='])
                    captures = raw_data['captures']
                    if captures:
                        headers = captures[0].keys()
                        writer.writerow(headers)
                        for capture in captures:
                            writer.writerow([capture.get(h, '') for h in headers])
        
        return str(output_path)
    
    def _get_html_template(self) -> str:
        """Obtener template HTML para reportes"""
        return '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ report.metadata.title }}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #fff;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.2);
            padding-bottom: 20px;
        }
        .header h1 {
            font-size: 2.5em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        .header p {
            font-size: 1.1em;
            opacity: 0.8;
            margin: 10px 0;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .summary-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .summary-card h3 {
            margin: 0 0 10px 0;
            font-size: 1.2em;
            opacity: 0.8;
        }
        .summary-card .value {
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }
        .chart-container {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .chart-container h3 {
            margin-top: 0;
            text-align: center;
            font-size: 1.4em;
        }
        .chart-container img {
            width: 100%;
            height: auto;
            border-radius: 8px;
        }
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            overflow: hidden;
        }
        .data-table th,
        .data-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .data-table th {
            background: rgba(255, 255, 255, 0.1);
            font-weight: bold;
        }
        .section {
            margin-bottom: 40px;
        }
        .section h2 {
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.2);
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ report.metadata.title }}</h1>
            <p>Generado el {{ generated_time }}</p>
            <p>Período: {{ report.metadata.period_hours }} horas | Total de registros: {{ report.metadata.total_records }}</p>
        </div>
        
        <div class="section">
            <h2>📊 Resumen Ejecutivo</h2>
            <div class="summary-grid">
                <div class="summary-card">
                    <h3>Total Visitas</h3>
                    <div class="value">{{ report.summary.total_visits }}</div>
                </div>
                <div class="summary-card">
                    <h3>Total Capturas</h3>
                    <div class="value">{{ report.summary.total_captures }}</div>
                </div>
                <div class="summary-card">
                    <h3>Tasa de Éxito</h3>
                    <div class="value">{{ "%.1f" | format(report.summary.success_rate) }}%</div>
                </div>
                <div class="summary-card">
                    <h3>IPs Únicas</h3>
                    <div class="value">{{ report.summary.unique_ips }}</div>
                </div>
            </div>
        </div>
        
        {% if report.charts %}
        <div class="section">
            <h2>📈 Análisis Visual</h2>
            
            {% if report.charts.temporal_activity %}
            <div class="chart-container">
                <h3>Actividad Temporal</h3>
                <img src="data:image/png;base64,{{ report.charts.temporal_activity }}" alt="Actividad Temporal">
            </div>
            {% endif %}
            
            {% if report.charts.geographic_distribution %}
            <div class="chart-container">
                <h3>Distribución Geográfica</h3>
                <img src="data:image/png;base64,{{ report.charts.geographic_distribution }}" alt="Distribución Geográfica">
            </div>
            {% endif %}
            
            {% if report.charts.template_performance %}
            <div class="chart-container">
                <h3>Rendimiento de Templates</h3>
                <img src="data:image/png;base64,{{ report.charts.template_performance }}" alt="Rendimiento de Templates">
            </div>
            {% endif %}
            
            {% if report.charts.browser_analysis %}
            <div class="chart-container">
                <h3>Análisis de Navegadores</h3>
                <img src="data:image/png;base64,{{ report.charts.browser_analysis }}" alt="Análisis de Navegadores">
            </div>
            {% endif %}
        </div>
        {% endif %}
        
        <div class="section">
            <h2>🔍 Análisis Detallado</h2>
            
            <h3>Distribución Geográfica</h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>País</th>
                        <th>Visitas</th>
                    </tr>
                </thead>
                <tbody>
                    {% for country, count in report.detailed_analysis.geographic_distribution.items() %}
                    <tr>
                        <td>{{ country }}</td>
                        <td>{{ count }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            
            <h3>Rendimiento de Templates</h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Template</th>
                        <th>Capturas</th>
                        <th>Dominios Únicos</th>
                    </tr>
                </thead>
                <tbody>
                    {% for template, stats in report.detailed_analysis.template_performance.items() %}
                    <tr>
                        <td>{{ template }}</td>
                        <td>{{ stats.captures }}</td>
                        <td>{{ stats.unique_domains }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>Reporte generado por AdvancedPhisher | {{ generated_time }}</p>
        </div>
    </div>
</body>
</html>
        '''

# Función de conveniencia para generar reportes
def generate_report(db_path: str, config: ReportConfig = None, output_format: str = "html") -> str:
    """Función de conveniencia para generar reportes"""
    if config is None:
        config = ReportConfig()
    
    generator = ReportGenerator(db_path)
    report_data = generator.generate_comprehensive_report(config)
    
    if output_format == "html":
        return generator.export_html_report(report_data)
    elif output_format == "json":
        return generator.export_json_report(report_data)
    elif output_format == "csv":
        return generator.export_csv_report(report_data)
    else:
        raise ValueError(f"Formato no soportado: {output_format}")