import requests
import logging
import json
import os
import random
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, List, Optional
from requests.exceptions import RequestException

from app.config import CYBERARK_API, DEMO_MODE

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='cyberark_api.log'
)
logger = logging.getLogger('cyberark_api')

class CyberArkAPI:
    def __init__(self):
        """
        Initialiser l'API CyberArk
        """
        self.base_url = CYBERARK_API["url"]
        self.username = CYBERARK_API["username"]
        self.password = CYBERARK_API["password"]
        self.token = None
        self.token_expiry = None
        self.timeout = CYBERARK_API["timeout"]
        self.verify_ssl = CYBERARK_API["verify_ssl"]
        self.demo_mode = DEMO_MODE
        self.demo_data = None
        
        if self.demo_mode:
            self._load_demo_data()
        
        logger.info(f"API CyberArk initialisée avec l'URL: {self.base_url}, Mode démo: {self.demo_mode}")
    
    def _load_demo_data(self):
        """
        Charger les données de démo
        """
        try:
            # Charger depuis le fichier de démo si disponible
            if os.path.exists('demo_data.json'):
                with open('demo_data.json', 'r') as f:
                    self.demo_data = json.load(f)
                    logger.info("Données de démo chargées depuis demo_data.json")
            else:
                # Générer des données de démo
                self.demo_data = self._generate_demo_data()
                
                # Enregistrer les données de démo générées
                with open('demo_data.json', 'w') as f:
                    json.dump(self.demo_data, f, indent=2)
                    logger.info("Données de démo générées et enregistrées dans demo_data.json")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données de démo: {str(e)}")
            # Générer des données de démo en mémoire
            self.demo_data = self._generate_demo_data()
    
    def _generate_demo_data(self) -> Dict[str, Any]:
        """
        Générer des données de démo aléatoires
        """
        current_time = datetime.now()
        
        # Générer des données pour les composants
        component_types = ["CPM", "PSM", "PVWA", "AAM"]
        component_status_data = []
        
        for component_type in component_types:
            total = random.randint(3, 10)
            connected = random.randint(max(1, total - 2), total)
            disconnected = total - connected
            
            component_status_data.append({
                "Component Type": component_type,
                "Total Amount": total,
                "Connected": connected,
                "Disconnected": disconnected,
                "Status": "OK" if disconnected == 0 else "Warning"
            })
        
        # Générer des données pour le coffre-fort
        vault_data = {
            "Total_Safes": random.randint(50, 200),
            "Total_Accounts": random.randint(1000, 5000),
            "Version": f"12.{random.randint(0, 6)}.{random.randint(0, 9)}",
            "License_Status": random.choice(["Valid", "Expiring Soon", "Expired"]),
            "License_Expiration": (current_time + timedelta(days=random.randint(1, 365))).isoformat()
        }
        
        # Générer des données pour les comptes
        total_accounts = vault_data["Total_Accounts"]
        managed_accounts = int(total_accounts * random.uniform(0.75, 0.95))
        non_managed_accounts = int(total_accounts * random.uniform(0.01, 0.10))
        pending_accounts = int(total_accounts * random.uniform(0.01, 0.05))
        failed_accounts = total_accounts - managed_accounts - non_managed_accounts - pending_accounts
        
        accounts_data = {
            "Total_Accounts": total_accounts,
            "Managed_Accounts": managed_accounts,
            "Non_Managed_Accounts": non_managed_accounts,
            "Pending_Accounts": pending_accounts,
            "Failed_Accounts": failed_accounts
        }
        
        # Générer des données pour la santé du système
        health_data = {
            "CPU_Usage": round(random.uniform(10.0, 80.0), 1),
            "Memory_Usage": round(random.uniform(20.0, 90.0), 1),
            "Disk_Usage": round(random.uniform(30.0, 85.0), 1),
            "Network_Latency": round(random.uniform(1.0, 100.0), 1),
            "Last_Backup": (current_time - timedelta(hours=random.randint(1, 24))).isoformat()
        }
        
        # Générer des événements de sécurité récents
        event_types = ["Login", "Logout", "Safe Access", "Account Access", "Policy Change", "Configuration Change"]
        severities = ["Info", "Warning", "Critical"]
        usernames = ["admin", "operator", "user1", "user2", "svc_account"]
        ips = ["192.168.1." + str(i) for i in range(1, 20)]
        safes = ["Root", "WindowsServers", "LinuxServers", "Domain Admins", "Service Accounts"]
        
        recent_activities = []
        
        for _ in range(20):
            event_type = random.choice(event_types)
            username = random.choice(usernames)
            source_ip = random.choice(ips)
            event_time = current_time - timedelta(minutes=random.randint(1, 1440))
            
            event = {
                "EventType": event_type,
                "Username": username,
                "Source_IP": source_ip,
                "Timestamp": event_time.isoformat(),
                "Severity": random.choice(severities)
            }
            
            if event_type in ["Safe Access", "Account Access"]:
                event["Target_Safe"] = random.choice(safes)
                event["Target_Account"] = f"{random.choice(['WIN', 'LIN', 'SVC'])}-{random.randint(100, 999)}"
                event["Description"] = f"{username} accessed {event['Target_Account']} in {event['Target_Safe']}"
            elif event_type in ["Policy Change", "Configuration Change"]:
                event["Description"] = f"{username} modified {random.choice(['password policy', 'rotation settings', 'access rules', 'platform settings'])}"
            else:
                event["Description"] = f"{username} {event_type.lower()}ed from {source_ip}"
            
            recent_activities.append(event)
        
        # Trier les événements par date
        recent_activities.sort(key=lambda x: x["Timestamp"], reverse=True)
        
        # Générer des tentatives de connexion échouées
        reasons = ["Invalid password", "Account locked", "Connection timeout", "MFA required", "Password expired"]
        failed_logins = []
        
        for _ in range(10):
            login_time = current_time - timedelta(minutes=random.randint(1, 1440))
            username = random.choice(usernames)
            
            failed_login = {
                "Username": username,
                "Source_IP": random.choice(ips),
                "Timestamp": login_time.isoformat(),
                "Reason": random.choice(reasons),
                "Severity": "Warning"
            }
            
            failed_logins.append(failed_login)
        
        # Trier les tentatives de connexion échouées par date
        failed_logins.sort(key=lambda x: x["Timestamp"], reverse=True)
        
        # Construire le résultat final
        return {
            "component_status": {"Items": component_status_data},
            "vault_status": {"Safes": vault_data},
            "accounts_status": {"value": accounts_data},
            "system_health": health_data,
            "recent_activities": recent_activities,
            "failed_logins": failed_logins,
            "last_update": current_time.isoformat()
        }
    
    def login(self) -> bool:
        """
        Se connecter à l'API CyberArk et obtenir un jeton d'authentification
        """
        if self.demo_mode:
            self.token = "demo_token"
            self.token_expiry = datetime.now() + timedelta(hours=8)
            return True
            
        logger.info("Tentative de connexion à l'API CyberArk")
        
        try:
            url = f"{self.base_url}/auth/LogOn"
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "username": self.username,
                "password": self.password
            }
            
            response = requests.post(
                url, 
                headers=headers, 
                json=data, 
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            if response.status_code == 200:
                response_data = response.json()
                self.token = response_data.get("Token")
                # Définir l'expiration du jeton (typiquement 8 heures)
                self.token_expiry = datetime.now() + timedelta(hours=8)
                logger.info("Connexion réussie à l'API CyberArk")
                return True
            else:
                logger.error(f"Échec de la connexion à l'API CyberArk: {response.status_code} - {response.text}")
                return False
                
        except RequestException as e:
            logger.error(f"Erreur de connexion à l'API CyberArk: {str(e)}")
            return False
    
    def is_token_valid(self) -> bool:
        """
        Vérifier si le jeton est valide et non expiré
        """
        if self.demo_mode:
            return True
            
        if not self.token or not self.token_expiry:
            return False
            
        # Vérifier si le jeton est toujours valide (avec une marge de 5 minutes)
        return datetime.now() < (self.token_expiry - timedelta(minutes=5))
    
    def ensure_logged_in(self) -> bool:
        """
        S'assurer que l'utilisateur est connecté
        """
        if self.is_token_valid():
            return True
            
        return self.login()
    
    def logout(self) -> bool:
        """
        Se déconnecter de l'API CyberArk
        """
        if self.demo_mode or not self.token:
            self.token = None
            self.token_expiry = None
            return True
            
        logger.info("Tentative de déconnexion de l'API CyberArk")
        
        try:
            url = f"{self.base_url}/auth/LogOff"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
            
            response = requests.post(
                url, 
                headers=headers, 
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            if response.status_code == 200:
                logger.info("Déconnexion réussie de l'API CyberArk")
                self.token = None
                self.token_expiry = None
                return True
            else:
                logger.error(f"Échec de la déconnexion de l'API CyberArk: {response.status_code} - {response.text}")
                return False
                
        except RequestException as e:
            logger.error(f"Erreur de déconnexion de l'API CyberArk: {str(e)}")
            return False
    
    def get_all_health_data(self) -> Tuple[Dict[str, Any], bool]:
        """
        Récupérer toutes les données de santé
        """
        if self.demo_mode:
            logger.info("Utilisation des données de démo")
            # Mettre à jour certaines valeurs pour simuler des changements
            if self.demo_data:
                self._update_demo_data()
            return self.demo_data, True
        
        # Vérifier que l'utilisateur est connecté
        if not self.ensure_logged_in():
            logger.error("Impossible de se connecter à l'API CyberArk")
            return {}, False
        
        # Récupérer les données
        component_status = self.get_component_status()
        vault_status = self.get_vault_status()
        accounts_status = self.get_accounts_status()
        system_health = self.get_system_health()
        recent_activities = self.get_recent_activities()
        failed_logins = self.get_failed_logins()
        
        # Vérifier que toutes les données ont été récupérées
        if not all([component_status, vault_status, accounts_status, system_health]):
            logger.error("Certaines données de santé n'ont pas pu être récupérées")
            return {}, False
        
        # Construire le résultat
        result = {
            "component_status": component_status,
            "vault_status": vault_status,
            "accounts_status": accounts_status,
            "system_health": system_health,
            "recent_activities": recent_activities,
            "failed_logins": failed_logins,
            "last_update": datetime.now().isoformat()
        }
        
        return result, True
    
    def _update_demo_data(self):
        """
        Mettre à jour certaines valeurs des données de démo pour simuler des changements
        """
        if not self.demo_data:
            return
            
        # Mettre à jour l'utilisation du CPU et de la mémoire
        self.demo_data["system_health"]["CPU_Usage"] = round(random.uniform(10.0, 80.0), 1)
        self.demo_data["system_health"]["Memory_Usage"] = round(random.uniform(20.0, 90.0), 1)
        
        # Mettre à jour le nombre de composants connectés/déconnectés
        for item in self.demo_data["component_status"]["Items"]:
            total = item["Total Amount"]
            connected = random.randint(max(1, total - 2), total)
            disconnected = total - connected
            item["Connected"] = connected
            item["Disconnected"] = disconnected
            item["Status"] = "OK" if disconnected == 0 else "Warning"
        
        # Mettre à jour la dernière connexion
        self.demo_data["last_update"] = datetime.now().isoformat()
    
    def get_component_status(self) -> Dict[str, Any]:
        """
        Récupérer l'état des composants
        """
        if self.demo_mode and self.demo_data:
            return self.demo_data.get("component_status", {})
        
        # Implémentation de l'appel API réel
        # À compléter avec l'API réelle
        
        return {}
    
    def get_component_details(self, component_type: str) -> List[Dict[str, Any]]:
        """
        Récupérer les détails des composants d'un type spécifique
        """
        if self.demo_mode and self.demo_data:
            # Générer des détails de composants de démo
            component_details = []
            component_status_items = self.demo_data.get("component_status", {}).get("Items", [])
            
            for item in component_status_items:
                if item.get("Component Type") == component_type:
                    total = item.get("Total Amount", 0)
                    connected = item.get("Connected", 0)
                    
                    for i in range(total):
                        is_connected = i < connected
                        last_connection = datetime.now() - timedelta(minutes=random.randint(0, 1440))
                        
                        detail = {
                            "Component Type": component_type,
                            "Component Version": f"12.{random.randint(0, 6)}.{random.randint(0, 9)}",
                            "IP Address": f"192.168.1.{random.randint(1, 254)}",
                            "Component User": f"svc_{component_type.lower()}_{random.randint(1, 5)}",
                            "Connected": is_connected,
                            "Last Connection": last_connection.isoformat() if is_connected else None,
                            "OS": random.choice(["Windows Server 2019", "Windows Server 2016", "RHEL 8", "Ubuntu 20.04"])
                        }
                        
                        component_details.append(detail)
                    
                    break
            
            return component_details
        
        # Implémentation de l'appel API réel
        # À compléter avec l'API réelle
        
        return []
    
    def get_vault_status(self) -> Dict[str, Any]:
        """
        Récupérer l'état du coffre-fort
        """
        if self.demo_mode and self.demo_data:
            return self.demo_data.get("vault_status", {})
        
        # Implémentation de l'appel API réel
        # À compléter avec l'API réelle
        
        return {}
    
    def get_accounts_status(self) -> Dict[str, Any]:
        """
        Récupérer l'état des comptes
        """
        if self.demo_mode and self.demo_data:
            return self.demo_data.get("accounts_status", {})
        
        # Implémentation de l'appel API réel
        # À compléter avec l'API réelle
        
        return {}
    
    def get_system_health(self) -> Dict[str, Any]:
        """
        Récupérer l'état de santé du système
        """
        if self.demo_mode and self.demo_data:
            return self.demo_data.get("system_health", {})
        
        # Implémentation de l'appel API réel
        # À compléter avec l'API réelle
        
        return {}
    
    def get_recent_activities(self) -> List[Dict[str, Any]]:
        """
        Récupérer les activités récentes
        """
        if self.demo_mode and self.demo_data:
            return self.demo_data.get("recent_activities", [])
        
        # Implémentation de l'appel API réel
        # À compléter avec l'API réelle
        
        return []
    
    def get_failed_logins(self) -> List[Dict[str, Any]]:
        """
        Récupérer les tentatives de connexion échouées
        """
        if self.demo_mode and self.demo_data:
            return self.demo_data.get("failed_logins", [])
        
        # Implémentation de l'appel API réel
        # À compléter avec l'API réelle
        
        return []