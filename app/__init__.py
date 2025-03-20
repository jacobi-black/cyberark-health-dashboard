from app.api import app as api_app
from app.models import create_tables

# Créer une méthode pour initialiser l'application
def initialize_app():
    """
    Initialiser l'application
    """
    # Créer les tables de la base de données
    create_tables()
    
    return api_app