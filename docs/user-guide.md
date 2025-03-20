# Guide d'utilisation

Ce guide vous aidera à naviguer et utiliser efficacement le tableau de bord de santé CyberArk.

## Interface web

L'interface web du tableau de bord est accessible à l'adresse `http://localhost:8000` (ou l'IP/port que vous avez configuré).

### Page d'accueil

La page d'accueil présente un aperçu complet de la santé de votre environnement CyberArk avec les sections suivantes:

1. **État des composants** - Affiche l'état de tous les composants CyberArk (CPM, PSM, PVWA, AAM)
2. **État du coffre-fort** - Présente les informations sur le coffre-fort, y compris le nombre de coffres et la version
3. **État des comptes** - Montre la répartition des comptes (gérés, non gérés, en attente, échoués)
4. **Santé du système** - Affiche les métriques de performance (CPU, mémoire, disque, réseau)
5. **Activités récentes** - Liste les dernières activités enregistrées dans le système
6. **Tentatives de connexion échouées** - Affiche les récentes tentatives de connexion qui ont échoué

### Actualisation des données

Vous pouvez actualiser manuellement les données en cliquant sur le bouton "Actualiser les données" en haut de la page. Par défaut, les données sont automatiquement actualisées toutes les 30 secondes.

## API REST

L'API REST est accessible à l'adresse `http://localhost:8000/api` et propose les endpoints suivants:

- `/api/health` - Vérifie l'état de santé de l'API
- `/api/dashboard` - Récupère toutes les données du tableau de bord
- `/api/components` - Récupère l'état des composants
- `/api/vault` - Récupère l'état du coffre-fort
- `/api/accounts` - Récupère l'état des comptes
- `/api/system` - Récupère l'état de santé du système
- `/api/events` - Récupère les événements de sécurité récents
- `/api/logins/failed` - Récupère les tentatives de connexion échouées

La documentation complète de l'API est disponible à l'adresse `http://localhost:8000/docs`.

## Visualisations Power BI

Le modèle Power BI permet de créer des visualisations avancées et des rapports personnalisés.

### Utilisation du modèle

1. Ouvrez Power BI Desktop
2. Ouvrez le fichier `powerbi/CyberArk_Dashboard.pbix`
3. Actualisez les données

### Personnalisation

Vous pouvez personnaliser le modèle Power BI en ajoutant de nouvelles visualisations ou en modifiant celles existantes. Le modèle se connecte à l'API REST et utilise les données récupérées pour générer les visualisations.