# CyberArk Health Dashboard

Un tableau de bord moderne pour surveiller la santé de votre environnement CyberArk Privileged Access Manager (PAM).

![CyberArk Health Dashboard](powerbi/assets/dashboard_preview.png)

## 🌟 Fonctionnalités

- **Surveillance des composants** - Suivi en temps réel de l'état de tous les composants CyberArk (CPM, PVWA, PSM, etc.)
- **Statistiques des comptes** - Vue d'ensemble des comptes gérés et non gérés
- **Métriques système** - Surveillance des ressources système (CPU, mémoire, disque)
- **Événements de sécurité** - Journal des événements de sécurité récents
- **Alertes** - Notification des problèmes critiques
- **Tableau de bord Power BI** - Visualisations riches et interactives
- **Mode démonstration** - Fonctionne avec des données de test sans connexion à CyberArk

## 📋 Prérequis

- Python 3.8+
- Power BI Desktop (pour les visualisations)
- CyberArk PAM v12.0+ (pour l'intégration avec un environnement réel)

## 🚀 Installation rapide

1. Cloner ce dépôt:
```bash
git clone https://github.com/your-username/cyberark-health-dashboard.git
cd cyberark-health-dashboard
```

2. Installer les dépendances:
```bash
pip install -r requirements.txt
```

3. Configurer l'environnement:
```bash
# Copier le fichier d'exemple et l'éditer selon vos besoins
cp .env.example .env
```

4. Initialiser la base de données:
```bash
python -c "from app.models import create_tables; create_tables()"
```

5. Démarrer l'API:
```bash
python main.py
```

6. Accéder au tableau de bord:
   - API: http://localhost:8000
   - Documentation API: http://localhost:8000/docs
   - Power BI: Suivre les instructions dans [powerbi/README.md](powerbi/README.md)

## 🔧 Configuration

Le fichier `.env` permet de configurer:

- **Mode démonstration** - Utilise des données d'exemple sans se connecter à CyberArk
- **Connexion à l'API CyberArk** - URL, méthode d'authentification, identifiants
- **Base de données** - Configurer SQLite (par défaut) ou SQL Server
- **Intervalle de collecte** - Fréquence de mise à jour des données
- **Port API** - Port d'écoute du serveur HTTP

## 📊 Visualisations Power BI

![Dashboard Layout](powerbi/assets/layout_example.png)

Le dashboard Power BI inclut:

- Cartes de score pour les métriques clés
- Graphiques en anneau pour l'état des composants
- Graphiques à barres pour la gestion des comptes
- Tableaux pour les événements récents
- Filtres par composant, date et severity

Consultez [powerbi/README.md](powerbi/README.md) pour les instructions détaillées de configuration de Power BI.

## 📚 Documentation

- [Guide utilisateur](wiki/UserGuide.md)
- [Guide d'installation](wiki/InstallationGuide.md)
- [Guide de dépannage](wiki/Troubleshooting.md)
- [API REST](wiki/APIReference.md)
- [Schéma de données](wiki/DataSchema.md)

## 🛠️ Développement

```bash
# Installation des dépendances de développement
pip install -r requirements-dev.txt

# Exécution des tests
pytest

# Vérification du style de code
flake8
```

## 📝 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues! Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour les directives.

## 📧 Contact

Pour toute question ou suggestion, veuillez contacter [votre-email@example.com](mailto:votre-email@example.com).