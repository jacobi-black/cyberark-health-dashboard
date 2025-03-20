import threading
import time
import logging
import json
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.cyberark_api import CyberArkAPI
from app.models import (
    create_tables,
    SessionLocal,
    ComponentStatus,
    Component,
    VaultStatus,
    AccountsStatus,
    SystemHealth,
    SecurityEvent
)
from app.config import COLLECTOR_CONFIG

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='health_collector.log'
)
logger = logging.getLogger('health_collector')

class HealthCollector:
    def __init__(self, interval=None):
        """
        Initialiser le collecteur de données de santé
        """
        self.interval = interval or COLLECTOR_CONFIG["interval"]
        self.components_to_check = COLLECTOR_CONFIG["components_to_check"]
        self.api = CyberArkAPI()
        self.running = False
        self.thread = None
        
        # Créer les tables dans la base de données si elles n'existent pas
        create_tables()
        
        logger.info(f"Collecteur de données de santé initialisé avec un intervalle de {self.interval} secondes")
    
    def start(self):
        """
        Démarrer la collection périodique de données
        """
        if self.running:
            logger.warning("Le collecteur est déjà en cours d'exécution")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._collect_loop)
        self.thread.daemon = True
        self.thread.start()
        
        logger.info("Collection périodique de données démarrée")
    
    def stop(self):
        """
        Arrêter la collection périodique de données
        """
        self.running = False
        if self.thread:
            self.thread.join(timeout=10)
            
        logger.info("Collection périodique de données arrêtée")
    
    def _collect_loop(self):
        """
        Boucle de collection périodique de données
        """
        while self.running:
            try:
                self.collect_and_store_health_data()
            except Exception as e:
                logger.error(f"Erreur lors de la collection de données: {str(e)}")
            
            # Attendre l'intervalle spécifié
            time.sleep(self.interval)
    
    def collect_and_store_health_data(self):
        """
        Collecter et stocker les données de santé
        """
        logger.info("Début de la collecte des données de santé")
        
        # Récupérer toutes les données de santé
        data, success = self.api.get_all_health_data()
        
        if not success:
            logger.error("Échec de la collecte des données de santé")
            return
            
        # Créer une session de base de données
        db = SessionLocal()
        
        try:
            # Stocker les données d'état des composants
            self._store_component_status(db, data)
            
            # Stocker les données d'état du coffre-fort
            self._store_vault_status(db, data)
            
            # Stocker les données d'état des comptes
            self._store_accounts_status(db, data)
            
            # Stocker les données d'état de santé du système
            self._store_system_health(db, data)
            
            # Stocker les événements de sécurité
            self._store_security_events(db, data)
            
            # Valider les modifications
            db.commit()
            
            logger.info("Données de santé stockées avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors du stockage des données: {str(e)}")
            db.rollback()
        finally:
            # Fermer la session
            db.close()
    
    def _store_component_status(self, db: Session, data: Dict[str, Any]):
        """
        Stocker les données d'état des composants
        """
        component_status_data = data.get("component_status", {}).get("Items", [])
        
        for component_type_data in component_status_data:
            # Créer une entrée d'état de composant
            component_status = ComponentStatus(
                component_type=component_type_data.get("Component Type", "Unknown"),
                total_amount=component_type_data.get("Total Amount", 0),
                connected=component_type_data.get("Connected", 0),
                disconnected=component_type_data.get("Disconnected", 0),
                status="OK" if component_type_data.get("Disconnected", 0) == 0 else "Warning"
            )
            
            db.add(component_status)
            db.flush()
            
            # Récupérer les détails des composants si disponibles
            component_type = component_type_data.get("Component Type", "")
            if component_type in self.components_to_check:
                component_details = self.api.get_component_details(component_type)
                
                for detail in component_details:
                    # Créer une entrée de composant
                    component = Component(
                        component_status_id=component_status.id,
                        component_type=detail.get("Component Type", "Unknown"),
                        component_version=detail.get("Component Version", "Unknown"),
                        ip_address=detail.get("IP Address", "0.0.0.0"),
                        component_user=detail.get("Component User", "Unknown"),
                        connected=detail.get("Connected", False),
                        last_connection=datetime.fromisoformat(detail.get("Last Connection", "").replace('Z', '+00:00')) if detail.get("Last Connection", "") else None,
                        os=detail.get("OS", "Windows")
                    )
                    
                    db.add(component)
    
    def _store_vault_status(self, db: Session, data: Dict[str, Any]):
        """
        Stocker les données d'état du coffre-fort
        """
        vault_data = data.get("vault_status", {}).get("Safes", {})
        
        if vault_data:
            vault_status = VaultStatus(
                total_safes=vault_data.get("Total_Safes", 0),
                total_accounts=vault_data.get("Total_Accounts", 0),
                version=vault_data.get("Version", "Unknown"),
                license_status=vault_data.get("License_Status", "Unknown"),
                license_expiration=datetime.fromisoformat(vault_data.get("License_Expiration", "").replace('Z', '+00:00')) if vault_data.get("License_Expiration", "") else None
            )
            
            db.add(vault_status)
    
    def _store_accounts_status(self, db: Session, data: Dict[str, Any]):
        """
        Stocker les données d'état des comptes
        """
        accounts_data = data.get("accounts_status", {}).get("value", {})
        
        if accounts_data:
            accounts_status = AccountsStatus(
                total_accounts=accounts_data.get("Total_Accounts", 0),
                managed_accounts=accounts_data.get("Managed_Accounts", 0),
                non_managed_accounts=accounts_data.get("Non_Managed_Accounts", 0),
                pending_accounts=accounts_data.get("Pending_Accounts", 0),
                failed_accounts=accounts_data.get("Failed_Accounts", 0)
            )
            
            db.add(accounts_status)
    
    def _store_system_health(self, db: Session, data: Dict[str, Any]):
        """
        Stocker les données d'état de santé du système
        """
        health_data = data.get("system_health", {})
        
        if health_data:
            system_health = SystemHealth(
                cpu_usage=health_data.get("CPU_Usage", 0.0),
                memory_usage=health_data.get("Memory_Usage", 0.0),
                disk_usage=health_data.get("Disk_Usage", 0.0),
                network_latency=health_data.get("Network_Latency", 0.0),
                last_backup=datetime.fromisoformat(health_data.get("Last_Backup", "").replace('Z', '+00:00')) if health_data.get("Last_Backup", "") else None
            )
            
            db.add(system_health)
    
    def _store_security_events(self, db: Session, data: Dict[str, Any]):
        """
        Stocker les événements de sécurité
        """
        security_events = data.get("recent_activities", [])
        
        for event in security_events:
            security_event = SecurityEvent(
                event_type=event.get("EventType", "Unknown"),
                username=event.get("Username", "Unknown"),
                source_ip=event.get("Source_IP", "0.0.0.0"),
                target_safe=event.get("Target_Safe", None),
                target_account=event.get("Target_Account", None),
                severity=event.get("Severity", "Info"),
                description=event.get("Description", ""),
                raw_data=json.dumps(event)
            )
            
            db.add(security_event)
            
        # Stocker également les tentatives de connexion échouées
        failed_logins = data.get("failed_logins", [])
        
        for login in failed_logins:
            security_event = SecurityEvent(
                event_type="Failed Login",
                username=login.get("Username", "Unknown"),
                source_ip=login.get("Source_IP", "0.0.0.0"),
                severity=login.get("Severity", "Warning"),
                description=login.get("Reason", ""),
                raw_data=json.dumps(login)
            )
            
            db.add(security_event)
    
    def get_latest_health_data(self) -> Dict[str, Any]:
        """
        Récupérer les dernières données de santé stockées
        """
        try:
            # Récupérer les données depuis l'API si disponible, ou depuis la base de données sinon
            # En cas d'échec complet, utiliser les données de démo
            
            # Si l'API est disponible, récupérer les données fraîches
            api_data, success = self.api.get_all_health_data()
            if success:
                return api_data
            
            # Sinon, récupérer les dernières données stockées dans la base de données
            db = SessionLocal()
            
            try:
                # Récupérer le dernier état des composants
                component_status_data = []
                component_statuses = db.query(ComponentStatus).order_by(ComponentStatus.timestamp.desc()).limit(10).all()
                
                if component_statuses:
                    for cs in component_statuses:
                        component_status_data.append({
                            "Component Type": cs.component_type,
                            "Total Amount": cs.total_amount,
                            "Connected": cs.connected,
                            "Disconnected": cs.disconnected,
                            "Status": cs.status
                        })
                
                # Récupérer le dernier état du coffre-fort
                vault_status = db.query(VaultStatus).order_by(VaultStatus.timestamp.desc()).first()
                vault_data = {}
                
                if vault_status:
                    vault_data = {
                        "Total_Safes": vault_status.total_safes,
                        "Total_Accounts": vault_status.total_accounts,
                        "Version": vault_status.version,
                        "License_Status": vault_status.license_status,
                        "License_Expiration": vault_status.license_expiration.isoformat() if vault_status.license_expiration else ""
                    }
                
                # Récupérer le dernier état des comptes
                accounts_status = db.query(AccountsStatus).order_by(AccountsStatus.timestamp.desc()).first()
                accounts_data = {}
                
                if accounts_status:
                    accounts_data = {
                        "Total_Accounts": accounts_status.total_accounts,
                        "Managed_Accounts": accounts_status.managed_accounts,
                        "Non_Managed_Accounts": accounts_status.non_managed_accounts,
                        "Pending_Accounts": accounts_status.pending_accounts,
                        "Failed_Accounts": accounts_status.failed_accounts
                    }
                
                # Récupérer le dernier état de santé du système
                system_health = db.query(SystemHealth).order_by(SystemHealth.timestamp.desc()).first()
                health_data = {}
                
                if system_health:
                    health_data = {
                        "CPU_Usage": system_health.cpu_usage,
                        "Memory_Usage": system_health.memory_usage,
                        "Disk_Usage": system_health.disk_usage,
                        "Network_Latency": system_health.network_latency,
                        "Last_Backup": system_health.last_backup.isoformat() if system_health.last_backup else ""
                    }
                
                # Récupérer les derniers événements de sécurité
                security_events = db.query(SecurityEvent).order_by(SecurityEvent.timestamp.desc()).limit(10).all()
                events_data = []
                
                if security_events:
                    for event in security_events:
                        if event.event_type != "Failed Login":
                            events_data.append({
                                "EventType": event.event_type,
                                "Username": event.username,
                                "Source_IP": event.source_ip,
                                "Target_Safe": event.target_safe,
                                "Target_Account": event.target_account,
                                "Severity": event.severity,
                                "Description": event.description,
                                "Timestamp": event.timestamp.isoformat()
                            })
                
                # Récupérer les dernières tentatives de connexion échouées
                failed_logins = db.query(SecurityEvent).filter(SecurityEvent.event_type == "Failed Login").order_by(SecurityEvent.timestamp.desc()).limit(10).all()
                logins_data = []
                
                if failed_logins:
                    for login in failed_logins:
                        logins_data.append({
                            "Username": login.username,
                            "Source_IP": login.source_ip,
                            "Reason": login.description,
                            "Severity": login.severity,
                            "Timestamp": login.timestamp.isoformat()
                        })
                
                # Construire le résultat
                return {
                    "component_status": {"Items": component_status_data},
                    "vault_status": {"Safes": vault_data},
                    "accounts_status": {"value": accounts_data},
                    "system_health": health_data,
                    "recent_activities": events_data,
                    "failed_logins": logins_data,
                    "last_update": datetime.now().isoformat()
                }
                
            finally:
                db.close()
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des dernières données de santé: {str(e)}")
            
            # En cas d'échec complet, retourner des données de démo
            return self.api.demo_data or {
                "component_status": {"Items": []},
                "vault_status": {"Safes": {}},
                "accounts_status": {"value": {}},
                "system_health": {},
                "recent_activities": [],
                "failed_logins": [],
                "last_update": datetime.now().isoformat()
            }

# Créer une instance singleton du collecteur de données
collector = HealthCollector()