import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration générale
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

# Configuration de l'API CyberArk
CYBERARK_API = {
    "base_url": os.getenv("CYBERARK_API_URL", "https://your-cyberark-instance.com"),
    "auth_type": os.getenv("CYBERARK_AUTH_TYPE", "cyberark"),
    "username": os.getenv("CYBERARK_USERNAME", ""),
    "password": os.getenv("CYBERARK_PASSWORD", ""),
    "timeout": int(os.getenv("CYBERARK_API_TIMEOUT", "30")),
    "verify_ssl": os.getenv("CYBERARK_API_VERIFY_SSL", "true").lower() == "true"
}

# Configuration de la base de données
DB_CONFIG = {
    "driver": os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server"),
    "server": os.getenv("DB_SERVER", "localhost"),
    "database": os.getenv("DB_NAME", "CyberArkHealthDB"),
    "username": os.getenv("DB_USERNAME", "sa"),
    "password": os.getenv("DB_PASSWORD", ""),
    "connection_string": os.getenv("DB_CONNECTION_STRING", "")
}

# Configuration du collecteur de données
COLLECTOR_CONFIG = {
    "interval": int(os.getenv("COLLECTOR_INTERVAL", "3600")),  # Intervalle en secondes (défaut: 1 heure)
    "components_to_check": os.getenv("COMPONENTS_TO_CHECK", "CPM,PSM,PVWA,AAM Credential Provider").split(","),
}

# Configuration de l'API
API_CONFIG = {
    "host": os.getenv("API_HOST", "0.0.0.0"),
    "port": int(os.getenv("API_PORT", "8000")),
}