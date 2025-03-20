import uvicorn
import logging
from dotenv import load_dotenv

from app import initialize_app
from app.config import API_CONFIG

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='main.log'
)
logger = logging.getLogger('main')

def main():
    """
    Point d'entrée principal de l'application
    """
    try:
        logger.info("Démarrage de l'application")
        
        # Initialiser l'application
        app = initialize_app()
        
        # Exécuter l'API
        host = API_CONFIG["host"]
        port = API_CONFIG["port"]
        
        logger.info(f"Démarrage du serveur API sur {host}:{port}")
        
        uvicorn.run(
            app,
            host=host,
            port=port
        )
        
    except Exception as e:
        logger.error(f"Erreur lors du démarrage de l'application: {str(e)}")
        raise

if __name__ == "__main__":
    main()