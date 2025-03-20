# Guide du Développeur - CyberArk Health Dashboard

Ce guide est destiné aux développeurs qui souhaitent contribuer au projet CyberArk Health Dashboard ou étendre ses fonctionnalités. Il détaille l'architecture du code, les bonnes pratiques et les procédures de développement.

## Architecture du projet

### Structure des répertoires

```
cyberark-health-dashboard/
├── app/                        # Code source principal
│   ├── __init__.py             # Initialisation du package
│   ├── models.py               # Modèles de données SQLAlchemy
│   ├── cyberark_api.py         # Client API CyberArk
│   ├── health_collector.py     # Collecteur de données de santé
│   ├── api.py                  # Définitions de l'API REST
│   ├── schemas.py              # Schémas Pydantic pour validation
│   └── utils.py                # Utilitaires divers
├── main.py                     # Point d'entrée de l'application
├── config.py                   # Configuration globale
├── tests/                      # Tests unitaires et d'intégration
│   ├── __init__.py
│   ├── test_cyberark_api.py
│   ├── test_health_collector.py
│   └── test_api.py
├── alembic/                    # Migrations de base de données
│   ├── versions/
│   └── env.py
├── powerbi/                    # Ressources Power BI
│   ├── README.md               # Documentation Power BI
│   └── assets/                 # Fichiers exemple et images
│       └── sample_data.json    # Données exemples pour Power BI
├── requirements.txt            # Dépendances Python
├── requirements-dev.txt        # Dépendances pour le développement
├── .env.example                # Exemple de fichier de configuration
├── README.md                   # Documentation principale
└── CONTRIBUTING.md             # Guide de contribution
```

### Architecture logicielle

Le projet suit une architecture en couches:

1. **Couche d'accès aux données CyberArk** (`cyberark_api.py`)
   - Interface avec l'API REST CyberArk PAM
   - Abstraction des appels d'API et de l'authentification

2. **Couche de collecte des données** (`health_collector.py`)
   - Collecte périodique des données de santé
   - Traitement et stockage des données collectées

3. **Couche de modèle de données** (`models.py`)
   - Définition des modèles de données SQLAlchemy
   - Gestion de la persistance

4. **Couche API REST** (`api.py`)
   - Exposition des données via une API REST FastAPI
   - Validation des entrées/sorties avec Pydantic

5. **Couche de présentation** (Power BI)
   - Visualisation et analyse des données
   - Tableaux de bord et rapports interactifs

### Flux de données

```
                   ┌────────────────┐
                   │ CyberArk PAM   │
                   │ REST API       │
                   └────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────┐
│ Health Dashboard Backend                        │
│                                                 │
│  ┌─────────────┐      ┌────────────────┐       │
│  │ CyberArk    │──┬──▶│ Health         │       │
│  │ API Client  │  │   │ Collector      │       │
│  └─────────────┘  │   └────────────────┘       │
│                   │          │                  │
│                   │          ▼                  │
│                   │   ┌─────────────┐           │
│                   └──▶│ Database    │           │
│                       └─────────────┘           │
│                              │                  │
│                              ▼                  │
│                       ┌─────────────┐           │
│                       │ REST API    │           │
│                       └─────────────┘           │
└────────────────────────────────────────────────┘
                          │
                          ▼
                   ┌────────────────┐
                   │ Power BI       │
                   │ Dashboard      │
                   └────────────────┘
```

## Environnement de développement

### Prérequis

- Python 3.8 ou supérieur
- Git
- SQLite (pour le développement) ou autre base de données
- Power BI Desktop (pour le développement du tableau de bord)

### Installation de l'environnement de développement

1. **Cloner le dépôt**:

```bash
git clone https://github.com/jacobi-black/cyberark-health-dashboard.git
cd cyberark-health-dashboard
```

2. **Créer un environnement virtuel**:

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
```

3. **Installer les dépendances de développement**:

```bash
pip install -r requirements-dev.txt
```

4. **Configurer les hooks pre-commit**:

```bash
pre-commit install
```

5. **Configurer le fichier .env**:

```bash
cp .env.example .env
# Modifier le fichier .env selon vos besoins
```

6. **Initialiser la base de données**:

```bash
python -c "from app.models import create_tables; create_tables()"
```

### Tâches de développement courantes

#### Exécuter l'application en mode développement

```bash
uvicorn main:app --reload
```

#### Exécuter les tests

```bash
pytest
```

Avec couverture de code:

```bash
pytest --cov=app
```

#### Vérifier la qualité du code

```bash
# Linting
flake8 app tests

# Formattage
black app tests

# Import sorting
isort app tests

# Type checking
mypy app
```

#### Générer une migration de base de données

```bash
# Après modifications des modèles dans models.py
alembic revision --autogenerate -m "Description de la migration"

# Appliquer les migrations
alembic upgrade head
```

## Meilleures pratiques de développement

### Style de code

Le projet suit les conventions de style PEP 8 avec quelques ajustements:

- Longueur de ligne maximale: 100 caractères
- Utilisez des docstrings au format Google pour la documentation
- Utilisez des annotations de type pour améliorer la maintenabilité

Exemple:

```python
def get_component_status(component_name: str) -> Dict[str, Any]:
    """Récupère l'état d'un composant CyberArk.
    
    Args:
        component_name: Nom du composant à vérifier.
        
    Returns:
        Dictionnaire contenant les informations d'état du composant.
        
    Raises:
        ComponentNotFoundError: Si le composant n'existe pas.
    """
    # Implémentation
```

### Tests

- Écrivez des tests unitaires pour toutes les fonctions publiques
- Utilisez des mocks pour simuler les dépendances externes
- Maintenez une couverture de code d'au moins 80%

Exemple de test:

```python
@pytest.fixture
def mock_cyberark_api():
    with patch("app.health_collector.CyberArkAPI") as mock_api:
        mock_api.get_component_status.return_value = {
            "status": "Connected",
            "last_connection": "2023-08-15T10:30:00Z"
        }
        yield mock_api

def test_collect_component_status(mock_cyberark_api):
    collector = HealthCollector(mock_cyberark_api)
    status = collector.collect_component_status("CPM")
    
    assert status["status"] == "Connected"
    assert "last_connection" in status
    mock_cyberark_api.get_component_status.assert_called_once_with("CPM")
```

### Gestion des erreurs

- Utilisez des exceptions personnalisées pour des erreurs spécifiques
- Journalisez les erreurs avec suffisamment de contexte
- Renvoyez des réponses d'API appropriées avec des codes HTTP corrects

Exemple:

```python
class CyberArkAPIError(Exception):
    """Exception de base pour les erreurs d'API CyberArk."""
    pass

class AuthenticationError(CyberArkAPIError):
    """Erreur d'authentification à l'API CyberArk."""
    pass

# Utilisation
try:
    api.authenticate(username, password)
except AuthenticationError as e:
    logger.error(f"Erreur d'authentification: {e}")
    raise HTTPException(status_code=401, detail="Authentification échouée")
```

### Sécurité

- Ne stockez jamais de secrets dans le code source
- Utilisez des variables d'environnement ou un gestionnaire de secrets
- Validez toutes les entrées utilisateur
- Utilisez HTTPS pour toutes les communications en production

## Extension du projet

### Ajout d'un nouveau composant CyberArk

Pour ajouter la surveillance d'un nouveau type de composant CyberArk:

1. Mettre à jour `cyberark_api.py` pour collecter les données du nouveau composant:

```python
def get_new_component_status(self) -> Dict[str, Any]:
    """Récupère l'état du nouveau composant CyberArk."""
    endpoint = f"{self.base_url}/ComponentAPI/Status"
    response = self.session.get(endpoint)
    
    if response.status_code != 200:
        raise CyberArkAPIError(f"Échec de récupération de l'état: {response.text}")
        
    return response.json()
```

2. Mettre à jour `health_collector.py` pour collecter régulièrement ces données:

```python
def collect_new_component_status(self):
    """Collecte l'état du nouveau composant."""
    try:
        status = self.api.get_new_component_status()
        
        # Traiter et stocker les données
        component = self.db.query(Component).filter_by(name="NouveauComposant").first()
        if not component:
            component = Component(name="NouveauComposant", type="NouveauType")
            self.db.add(component)
            self.db.commit()
            
        component_status = ComponentStatus(
            component_id=component.id,
            status=status["status"],
            last_connection=datetime.fromisoformat(status["lastConnection"]),
            details=json.dumps(status)
        )
        self.db.add(component_status)
        self.db.commit()
        
    except Exception as e:
        logger.error(f"Erreur lors de la collecte du nouveau composant: {e}")
```

3. Mettre à jour `api.py` pour exposer ces données:

```python
@router.get("/components/nouveau", response_model=schemas.NewComponentSchema)
def get_new_component():
    """Récupère les données du nouveau composant."""
    component = db.query(Component).filter_by(name="NouveauComposant").first()
    if not component:
        raise HTTPException(status_code=404, detail="Composant non trouvé")
        
    latest_status = db.query(ComponentStatus)\
        .filter_by(component_id=component.id)\
        .order_by(ComponentStatus.created_at.desc())\
        .first()
        
    return {
        "component_name": component.name,
        "status": latest_status.status if latest_status else "Unknown",
        "last_connection": latest_status.last_connection if latest_status else None,
        "details": json.loads(latest_status.details) if latest_status and latest_status.details else {}
    }
```

4. Créer le schéma Pydantic correspondant dans `schemas.py`:

```python
class NewComponentSchema(BaseModel):
    component_name: str
    status: str
    last_connection: Optional[datetime]
    details: Dict[str, Any] = {}
    
    class Config:
        schema_extra = {
            "example": {
                "component_name": "NouveauComposant",
                "status": "Connected",
                "last_connection": "2023-08-15T10:30:00Z",
                "details": {
                    "version": "12.1.0",
                    "specific_attribute": "value"
                }
            }
        }
```

### Ajout de nouvelles visualisations Power BI

Pour ajouter de nouvelles visualisations au tableau de bord Power BI:

1. Ouvrir le fichier `.pbix` dans Power BI Desktop
2. Ajouter une nouvelle mesure DAX:

```dax
NouvelleMetrique = 
CALCULATE(
    COUNT('Activities'[id]),
    'Activities'[action] = "NouvelleAction"
)
```

3. Créer une nouvelle visualisation:
   - Sélectionner le type de visualisation approprié
   - Ajouter la nouvelle mesure
   - Configurer les axes, légendes et formatage

4. Mettre à jour la documentation:
   - Ajouter la nouvelle visualisation à la documentation
   - Expliquer comment l'interpréter

### Intégration avec d'autres systèmes

Pour intégrer avec d'autres systèmes ou sources de données:

1. Créer un nouveau module dans `app/` pour l'intégration:

```python
# app/integration_service.py
class IntegrationService:
    """Service d'intégration avec un système externe."""
    
    def __init__(self, config):
        self.api_url = config.get("API_URL")
        self.api_key = config.get("API_KEY")
        
    def fetch_data(self):
        """Récupère les données du système externe."""
        # Implémentation
```

2. Mettre à jour `health_collector.py` pour utiliser ce service:

```python
def collect_integration_data(self):
    """Collecte des données depuis le système intégré."""
    try:
        integration = IntegrationService(self.config)
        data = integration.fetch_data()
        
        # Traiter et stocker les données
        # ...
        
    except Exception as e:
        logger.error(f"Erreur lors de l'intégration: {e}")
```

3. Exposer les données via l'API:

```python
@router.get("/integration", response_model=schemas.IntegrationSchema)
def get_integration_data():
    """Récupère les données d'intégration."""
    # Implémentation
```

## Déploiement

### Préparation pour la production

Avant de déployer en production:

1. **Sécuriser l'application**:
   - Configurer HTTPS
   - Ajouter une authentification à l'API
   - Restreindre les accès réseau

2. **Optimiser les performances**:
   - Configurer des index de base de données
   - Ajouter une mise en cache des résultats fréquents
   - Configurer la compression des réponses

3. **Mettre en place la surveillance**:
   - Configurer la journalisation
   - Mettre en place des alertes
   - Surveiller l'utilisation des ressources

### Pipeline CI/CD

Un exemple de pipeline CI/CD avec GitHub Actions:

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt
      - name: Lint with flake8
        run: flake8 app tests
      - name: Check formatting with black
        run: black --check app tests
      - name: Run tests
        run: pytest --cov=app

  build:
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and push Docker image
        uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: your-registry/cyberark-health-dashboard:latest
```

## Ressources additionnelles

### Documentation de référence

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentation CyberArk API](https://docs.cyberark.com/Product-Doc/OnlineHelp/PAS/Latest/en/Content/SDK/rest-api-overview.htm)
- [Documentation Power BI](https://docs.microsoft.com/en-us/power-bi/)

### Tutoriels recommandés

- [Guide FastAPI pour SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Tutoriel Power BI pour développeurs](https://docs.microsoft.com/en-us/power-bi/developer/embedded/embedded-analytics-power-bi/)

### Outils de développement

- **VS Code** - Éditeur de code recommandé avec extensions pour Python
- **Postman** - Pour tester l'API REST
- **DBeaver** - Pour explorer et manipuler la base de données
- **Git Flow** - Workflow Git recommandé pour le développement collaboratif