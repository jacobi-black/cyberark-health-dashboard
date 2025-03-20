# Guide Utilisateur - CyberArk Health Dashboard

Ce guide vous aidera à utiliser et interpréter le tableau de bord de santé CyberArk.

## Accès au tableau de bord

### Via l'API REST

L'API REST fournit un accès direct aux données brutes:

- **URL de base**: http://votre-serveur:8000
- **Point d'accès principal**: `/api/dashboard`
- **Documentation API**: `/docs`

### Via Power BI

Le tableau de bord Power BI est la principale interface utilisateur:

1. Ouvrez le fichier `.pbix` fourni
2. Vérifiez que la connexion à l'API est correctement configurée
3. Actualisez les données si nécessaire

## Interprétation des différentes sections

### 1. Vue d'ensemble

![Vue d'ensemble](../powerbi/assets/overview_section.png)

Cette section présente les principaux indicateurs de santé:

- **Statut global du système**: État global de tous les composants
- **Composants connectés**: Pourcentage de composants connectés
- **Comptes gérés**: Pourcentage de comptes gérés par CyberArk
- **Utilisation des ressources**: Niveaux de CPU, mémoire et disque

### 2. État des composants

Cette section détaille l'état de chaque type de composant CyberArk:

- **CPM (Central Policy Manager)**: Gère les politiques de mot de passe
- **PVWA (Password Vault Web Access)**: Interface web d'accès au coffre-fort
- **PSM (Privileged Session Manager)**: Gère les sessions privilégiées
- **AAM (Application Access Manager)**: Gère l'accès des applications aux comptes privilégiés

Les indicateurs incluent:
- Nombre total de composants par type
- Nombre de composants connectés vs déconnectés
- Statut global par type de composant (OK, Warning, Error)

### 3. Gestion des comptes

Visualisation des comptes dans CyberArk:

- **Comptes totaux**: Nombre total de comptes dans le coffre-fort
- **Comptes gérés**: Comptes dont les mots de passe sont gérés par CyberArk
- **Comptes non gérés**: Comptes stockés mais non gérés
- **Comptes en attente**: Comptes en attente d'opérations
- **Comptes en échec**: Comptes avec des opérations en échec

### 4. Événements récents

Journal des événements de sécurité récents:

- **Connexions réussies/échouées**
- **Accès aux comptes**
- **Changements de mot de passe**
- **Violations de politique**
- **Sessions privilégiées**

Les événements sont classés par sévérité (Info, Warning, Critical).

### 5. Santé du système

Métriques de santé du système:

- **Utilisation CPU**: Pourcentage d'utilisation du processeur
- **Utilisation mémoire**: Pourcentage d'utilisation de la mémoire
- **Utilisation disque**: Espace disque utilisé
- **Latence réseau**: Temps de réponse réseau
- **Date dernière sauvegarde**: Date de la dernière sauvegarde réussie

## Filtres et interactions

Le tableau de bord offre plusieurs options de filtrage:

- **Par type de composant**: Filtrer les données pour un type spécifique (CPM, PVWA, etc.)
- **Par plage de dates**: Afficher les données sur une période spécifique
- **Par sévérité**: Filtrer les événements par niveau de sévérité
- **Par statut**: Filtrer les composants par statut (connecté/déconnecté)

## Alertes et notifications

Le tableau de bord met en évidence les éléments nécessitant votre attention:

- **Rouge**: Éléments critiques nécessitant une attention immédiate
- **Orange**: Avertissements nécessitant une surveillance
- **Vert**: Éléments fonctionnant normalement

## Actualisation des données

Les données sont automatiquement collectées à intervalles réguliers (configurable dans le fichier `.env`).

Pour forcer une actualisation:

1. Dans le backend: Appelez `POST /api/collect`
2. Dans Power BI: Cliquez sur "Actualiser" dans l'interface

## Bonnes pratiques

- **Vérifiez régulièrement** le tableau de bord pour identifier les problèmes potentiels
- **Investiguer promptement** les composants déconnectés ou en erreur
- **Surveillez les tendances** d'utilisation des ressources pour anticiper les besoins
- **Prêtez attention** aux événements de sécurité critiques
- **Configurez des alertes** pour être informé des problèmes important

## Dépannage

Si vous rencontrez des problèmes avec le tableau de bord:

1. Vérifiez que l'API est en cours d'exécution (`http://votre-serveur:8000/api/health`)
2. Assurez-vous que les connexions à CyberArk sont configurées correctement
3. Consultez les journaux de l'application pour les erreurs
4. Référez-vous au [Guide de dépannage](Troubleshooting.md) pour des solutions aux problèmes courants