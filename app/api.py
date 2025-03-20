from fastapi import FastAPI, BackgroundTasks, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging
from datetime import datetime
import os
from pathlib import Path

from app.models import DashboardData, SessionLocal
from app.health_collector import collector
from app.config import API_CONFIG

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='api.log'
)
logger = logging.getLogger('api')

# Créer l'application FastAPI
app = FastAPI(
    title="CyberArk Health Dashboard API",
    description="API pour récupérer les données de santé de CyberArk",
    version="1.0.0"
)

# Configurer CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration des templates
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Montage des fichiers statiques
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/powerbi", StaticFiles(directory=str(BASE_DIR.parent / "powerbi")), name="powerbi")

# Dépendance pour obtenir une connexion à la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    """
    Événement de démarrage de l'application
    """
    logger.info("Démarrage de l'API")
    # Démarrer le collecteur de données
    collector.start()

@app.on_event("shutdown")
async def shutdown_event():
    """
    Événement d'arrêt de l'application
    """
    logger.info("Arrêt de l'API")
    # Arrêter le collecteur de données
    collector.stop()

@app.get("/", summary="Page d'accueil", tags=["Interface"])
async def home(request: Request):
    """
    Page d'accueil du dashboard
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/health", summary="Vérifier l'état de santé de l'API", tags=["Santé"])
async def health_check():
    """
    Vérifier l'état de santé de l'API
    """
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/api/dashboard", response_model=DashboardData, summary="Récupérer les données du tableau de bord", tags=["Tableau de bord"])
async def get_dashboard_data(
    refresh: bool = Query(False, description="Forcer la récupération de nouvelles données")
):
    """
    Récupérer les données du tableau de bord
    """
    try:
        if refresh:
            # Collecter de nouvelles données
            collector.collect_and_store_health_data()
            
        # Récupérer les dernières données
        dashboard_data = collector.get_latest_health_data()
        
        if not dashboard_data:
            logger.warning("Aucune donnée de tableau de bord disponible")
            raise HTTPException(status_code=404, detail="Aucune donnée disponible")
            
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des données du tableau de bord: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

@app.get("/api/components", summary="Récupérer l'état des composants", tags=["Composants"])
async def get_components_status():
    """
    Récupérer l'état des composants
    """
    try:
        dashboard_data = collector.get_latest_health_data()
        return dashboard_data.get("component_status", {"Items": []})
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'état des composants: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

@app.get("/api/vault", summary="Récupérer l'état du coffre-fort", tags=["Coffre-fort"])
async def get_vault_status():
    """
    Récupérer l'état du coffre-fort
    """
    try:
        dashboard_data = collector.get_latest_health_data()
        return dashboard_data.get("vault_status", {"Safes": {}})
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'état du coffre-fort: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

@app.get("/api/accounts", summary="Récupérer l'état des comptes", tags=["Comptes"])
async def get_accounts_status():
    """
    Récupérer l'état des comptes
    """
    try:
        dashboard_data = collector.get_latest_health_data()
        return dashboard_data.get("accounts_status", {"value": {}})
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'état des comptes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

@app.get("/api/system", summary="Récupérer l'état de santé du système", tags=["Système"])
async def get_system_health():
    """
    Récupérer l'état de santé du système
    """
    try:
        dashboard_data = collector.get_latest_health_data()
        return dashboard_data.get("system_health", {})
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'état de santé du système: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

@app.get("/api/events", summary="Récupérer les événements de sécurité récents", tags=["Événements"])
async def get_security_events(
    limit: int = Query(10, description="Nombre d'événements à récupérer", ge=1, le=100)
):
    """
    Récupérer les événements de sécurité récents
    """
    try:
        dashboard_data = collector.get_latest_health_data()
        events = dashboard_data.get("recent_activities", [])
        return {"events": events[:limit]}
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des événements de sécurité: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

@app.get("/api/logins/failed", summary="Récupérer les tentatives de connexion échouées", tags=["Connexions"])
async def get_failed_logins(
    limit: int = Query(10, description="Nombre de tentatives à récupérer", ge=1, le=100)
):
    """
    Récupérer les tentatives de connexion échouées
    """
    try:
        dashboard_data = collector.get_latest_health_data()
        logins = dashboard_data.get("failed_logins", [])
        return {"logins": logins[:limit]}
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des tentatives de connexion échouées: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

@app.post("/api/collect", summary="Forcer la collecte de données", tags=["Administration"])
async def force_collect_data(background_tasks: BackgroundTasks):
    """
    Forcer la collecte de données
    """
    try:
        # Exécuter la collecte en arrière-plan
        background_tasks.add_task(collector.collect_and_store_health_data)
        return {"status": "collection started", "timestamp": datetime.now().isoformat()}
        
    except Exception as e:
        logger.error(f"Erreur lors de la collecte forcée des données: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

# Fonction pour exécuter l'API
def run_api():
    """
    Exécuter l'API
    """
    import uvicorn
    uvicorn.run(
        "app.api:app",
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        reload=True
    )