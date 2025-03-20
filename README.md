# CyberArk Health Dashboard

Tableau de bord de surveillance pour les environnements CyberArk Privileged Access Management (PAM). Cet outil permet aux administrateurs de surveiller en temps réel la santé et les performances de tous les composants CyberArk.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 🚀 Fonctionnalités

- **Surveillance en temps réel** des composants CyberArk (CPM, PSM, PVWA, AAM)
- **Statistiques des comptes** (gérés, non gérés, en attente, échoués)
- **Métriques système** (CPU, mémoire, disque, réseau)
- **Événements de sécurité** et tentatives de connexion échouées
- **Alertes** pour les problèmes critiques
- **Intégration avec Power BI** pour des visualisations avancées
- **Interface web** simple et intuitive pour un accès rapide aux données

## 📋 Prérequis

- Python 3.8 ou supérieur
- CyberArk PAM v12.0 ou supérieur
- Accès à l'API REST de CyberArk
- Optionnel: Power BI Desktop (pour les visualisations avancées)

## ⚡ Installation rapide

```bash
# Cloner le dépôt
git clone https://github.com/jacobi-black/cyberark-health-dashboard.git
cd cyberark-health-dashboard

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp .env.example .env
# Modifier .env avec vos paramètres

# Initialiser la base de données
python -c "from app.models import init_db; init_db()"

# Démarrer l'API
python main.py
```

## 🔧 Configuration

Configurez l'application en modifiant le fichier `.env` :

```ini
# Mode démo - mettez false pour se connecter à une vraie instance
DEMO_MODE=true

# API CyberArk
CYBERARK_API_URL=https://your-cyberark-instance.com/PasswordVault
CYBERARK_AUTH_TYPE=cyberark
CYBERARK_USERNAME=admin
CYBERARK_PASSWORD=password

# Base de données
DB_CONNECTION_STRING=sqlite:///cyberark_health.db

# Intervalle de collecte en secondes
COLLECTOR_INTERVAL=3600
```

## 🖥️ Interface web

Une fois l'application démarrée, accédez à l'interface web:

- URL : [http://localhost:8000](http://localhost:8000)
- Documentation API : [http://localhost:8000/docs](http://localhost:8000/docs)

## 📊 Visualisations Power BI

Un modèle Power BI est fourni dans le dossier `powerbi/`. Pour l'utiliser:

1. Ouvrez Power BI Desktop
2. Ouvrez le fichier `powerbi/CyberArk_Dashboard.pbix`
3. Configurez la connexion à l'API : `http://localhost:8000/api/dashboard`
4. Actualisez les données

## 🗄️ Base de données

La base de données stocke l'historique de l'état de santé pour:

1. **Analyse de tendances** - Visualisez l'évolution des métriques dans le temps
2. **Continuité de service** - Accédez aux données même pendant les pannes d'API
3. **Optimisation des performances** - Identifiez les goulots d'étranglement et améliorez les performances

## 📚 Documentation

- [Guide d'utilisation](docs/user-guide.md)
- [Guide d'installation](docs/installation.md)
- [Résolution des problèmes](docs/troubleshooting.md)
- [Référence API](docs/api-reference.md)
- [Schéma de données](docs/data-schema.md)

## 🛠️ Développement

Pour contribuer au développement:

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Installer les dépendances de développement
pip install -r requirements-dev.txt

# Exécuter les tests
pytest
```

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues! Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour les directives.

## 📧 Contact

Pour toute question ou assistance, créez une issue sur GitHub ou contactez l'équipe de développement.