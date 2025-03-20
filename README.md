# CyberArk Health Dashboard

Un tableau de bord complet pour surveiller la santé des composants CyberArk et le statut des comptes gérés.

## Caractéristiques

- **Surveillance en temps réel** des composants CyberArk (CPM, PVWA, PSM, AAM)
- **Statistiques des comptes** gérés et non gérés
- **Métriques système** (CPU, mémoire, espace disque)
- **Détection des événements de sécurité** et des tentatives de connexion infructueuses
- **Alertes** sur les composants non connectés ou les ressources système élevées
- **Intégration avec PowerBI** pour une visualisation avancée

## Prérequis

- Python 3.8+
- CyberArk PAM v12.0+
- Compte CyberArk avec droits d'audit suffisants
- PowerBI Desktop (pour les tableaux de bord)

## Installation rapide

```bash
# Cloner le dépôt
git clone https://github.com/jacobi-black/cyberark-health-dashboard.git
cd cyberark-health-dashboard

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos paramètres

# Initialiser la base de données
python -c "from app.models import create_tables; create_tables()"

# Démarrer l'API
python main.py
```

## Configuration

Configurez les paramètres dans le fichier `.env` :

```
# Configuration de l'API CyberArk
CYBERARK_API_URL=https://votre-instance-cyberark.com
CYBERARK_AUTH_TYPE=cyberark  # ou ldap, radius
CYBERARK_USERNAME=votreUser
CYBERARK_PASSWORD=votreMotDePasse

# Configuration de la base de données
DB_CONNECTION_STRING=sqlite:///cyberark_health.db

# Configuration de l'API
API_HOST=0.0.0.0
API_PORT=8000
```

## Visualisation avec PowerBI

Le dashboard peut être visualisé directement via l'API REST ou à travers PowerBI :

1. Connectez PowerBI Desktop à l'API REST (http://localhost:8000/api/dashboard)
2. Importez les données en utilisant le connecteur JSON ou Web
3. Créez vos visualisations ou utilisez les modèles disponibles dans `/powerbi/`

## Rôle de la base de données

La base de données joue un rôle crucial dans l'application :

- **Historique des données** : Permet d'analyser l'évolution des métriques sur la durée
- **Continuité de service** : Conserve les données même en cas d'indisponibilité temporaire de l'API CyberArk
- **Analyses rétroactives** : Possibilité d'identifier les tendances et comportements anormaux
- **Support du mode hors ligne** : L'application peut afficher les dernières données collectées même sans connexion
- **Optimisation des performances** : Réduit les appels API répétitifs vers CyberArk

## Documentation

- [Guide d'installation](docs/installation.md)
- [Guide de l'utilisateur](docs/user-guide.md)
- [Documentation de l'API](http://localhost:8000/docs) (disponible après démarrage)
- [Schéma des données](docs/data-schema.md)
- [Dépannage](docs/troubleshooting.md)

## Développement

Pour contribuer au projet :

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows

# Installer les dépendances de développement
pip install -r requirements-dev.txt

# Lancer les tests
pytest
```

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Contribution

Toute contribution est la bienvenue ! Veuillez consulter [CONTRIBUTING.md](CONTRIBUTING.md) pour les directives.

## Contact

Pour toute question ou suggestion, veuillez ouvrir une issue sur ce dépôt.