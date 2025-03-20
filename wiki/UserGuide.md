# Guide de l'utilisateur - CyberArk Health Dashboard

Ce guide fournit des instructions détaillées pour utiliser le CyberArk Health Dashboard, naviguer dans ses fonctionnalités et interpréter les informations présentées.

## Accès au tableau de bord

### Accès à l'API REST

L'API REST du CyberArk Health Dashboard est accessible à l'adresse suivante:

```
http://<server-ip>:8000
```

Où `<server-ip>` est l'adresse du serveur où l'application est installée. Si vous accédez localement, utilisez `localhost` ou `127.0.0.1`.

**Points d'accès principaux**:

- `/api/dashboard` - Données complètes du tableau de bord (format JSON)
- `/api/health` - Vérification de l'état de santé de l'API
- `/docs` - Documentation interactive de l'API (Swagger UI)

### Accès au tableau de bord Power BI

Pour accéder au tableau de bord Power BI:

1. Ouvrez Power BI Desktop
2. Ouvrez le fichier `.pbix` fourni avec l'application
3. Actualisez les données pour voir les informations les plus récentes

Si le tableau de bord a été publié sur Power BI Service:

1. Accédez à [app.powerbi.com](https://app.powerbi.com)
2. Connectez-vous avec vos identifiants
3. Accédez à l'espace de travail où le tableau de bord a été publié

## Navigation dans le tableau de bord

### Vue d'ensemble

Le tableau de bord CyberArk Health est organisé en plusieurs sections:

1. **En-tête** - Affiche les métriques clés et l'état général du système
2. **État des composants** - Affiche l'état de connexion de chaque composant CyberArk
3. **Gestion des comptes** - Présente les statistiques sur les comptes gérés et non gérés
4. **Santé du système** - Montre l'utilisation des ressources système
5. **Activités récentes** - Liste les événements récents du système
6. **Tentatives de connexion échouées** - Affiche les tentatives de connexion échouées

### Filtres et segmentation

Vous pouvez filtrer les données affichées dans le tableau de bord en utilisant:

- **Filtre de date** - Pour afficher les données sur une période spécifique
- **Filtre de composant** - Pour se concentrer sur un ou plusieurs composants CyberArk
- **Filtre d'utilisateur** - Pour filtrer les activités par utilisateur

Pour appliquer un filtre:

1. Cliquez sur l'icône de filtre dans le coin supérieur droit d'une visualisation
2. Sélectionnez les valeurs que vous souhaitez inclure ou exclure
3. Cliquez sur "Appliquer"

## Interprétation des données

### État des composants

Chaque composant CyberArk est représenté avec un statut:

- **Connecté** (vert) - Le composant est en ligne et fonctionne normalement
- **Déconnecté** (rouge) - Le composant est hors ligne ou ne répond pas
- **Avertissement** (jaune) - Le composant est en ligne mais présente des problèmes

La visualisation en anneau montre la proportion de composants connectés par rapport au total.

### Gestion des comptes

Le tableau de bord présente les statistiques suivantes sur les comptes:

- **Comptes gérés** - Nombre de comptes sous gestion CyberArk
- **Comptes non gérés** - Nombre de comptes détectés mais non gérés
- **Pourcentage de gestion** - Proportion des comptes sous gestion

Un pourcentage élevé (>80%) indique une bonne couverture de gestion des comptes.

### Santé du système

Les métriques de santé du système incluent:

- **Utilisation CPU** - Pourcentage d'utilisation du CPU des serveurs CyberArk
- **Utilisation mémoire** - Pourcentage d'utilisation de la mémoire
- **Utilisation disque** - Pourcentage d'espace disque utilisé

Les seuils d'alerte sont:
- Vert: 0-70% (normal)
- Jaune: 70-90% (attention)
- Rouge: 90-100% (critique)

### Activités récentes

La table des activités récentes affiche:

- **Horodatage** - Date et heure de l'événement
- **Utilisateur** - Utilisateur qui a effectué l'action
- **Action** - Description de l'activité
- **Composant** - Composant concerné par l'activité

Cette section aide à surveiller l'activité du système et à identifier les actions inhabituelles.

### Tentatives de connexion échouées

Cette section montre:

- **Horodatage** - Date et heure de la tentative
- **Utilisateur** - Nom d'utilisateur utilisé
- **Raison** - Raison de l'échec (mot de passe incorrect, compte verrouillé, etc.)
- **Source IP** - Adresse IP de la tentative

Surveillez cette section pour détecter d'éventuelles tentatives d'accès non autorisé.

## Cas d'utilisation courants

### Surveillance quotidienne

Pour une surveillance quotidienne efficace:

1. Vérifiez l'état de tous les composants dans la section "État des composants"
2. Examinez les métriques d'utilisation des ressources dans "Santé du système"
3. Passez en revue les activités récentes pour identifier toute activité inhabituelle
4. Vérifiez les tentatives de connexion échouées pour détecter d'éventuelles tentatives d'intrusion

### Analyse des tendances

Pour analyser les tendances sur une période plus longue:

1. Utilisez le filtre de date pour définir la période d'analyse
2. Examinez l'évolution de l'utilisation des ressources au fil du temps
3. Observez les changements dans le nombre de comptes gérés vs non gérés
4. Analysez les patterns d'activité pour identifier des comportements récurrents

### Résolution de problèmes

En cas de problème détecté:

1. Identifiez le composant concerné dans la section "État des composants"
2. Vérifiez les métriques de santé du système pour ce composant
3. Consultez les activités récentes liées à ce composant
4. Utilisez ces informations pour diagnostiquer et résoudre le problème

## Personnalisation du tableau de bord

### Ajout de visualisations

Pour ajouter de nouvelles visualisations dans Power BI Desktop:

1. Cliquez sur l'icône du type de visualisation souhaité dans le panneau Visualisations
2. Sélectionnez les champs de données à utiliser dans le panneau Champs
3. Configurez les options de formatage selon vos préférences

### Création de mesures personnalisées

Pour créer des mesures personnalisées:

1. Dans Power BI Desktop, cliquez sur "Modélisation" > "Nouvelle mesure"
2. Entrez la formule DAX pour votre mesure, par exemple:
   ```
   PourcentageComposantsConnectés = 
   DIVIDE(
       COUNTROWS(FILTER('ComponentStatus', 'ComponentStatus'[Status] = "Connected")),
       COUNTROWS('ComponentStatus')
   ) * 100
   ```
3. Cliquez sur "Valider" puis sur "OK"

### Configuration des alertes

Pour configurer des alertes dans Power BI Service:

1. Ouvrez le rapport dans Power BI Service
2. Cliquez sur les trois points (...) sur la visualisation où vous voulez configurer une alerte
3. Sélectionnez "Gérer les alertes"
4. Cliquez sur "Ajouter une règle d'alerte"
5. Configurez les seuils et la fréquence de notification
6. Cliquez sur "Enregistrer"

## Exportation et partage de données

### Exportation de rapports

Pour exporter des données du tableau de bord:

1. Dans Power BI Desktop, cliquez sur "Fichier" > "Exporter"
2. Choisissez le format d'exportation (PDF, PowerPoint, etc.)
3. Configurez les options d'exportation
4. Cliquez sur "Exporter"

### Planification de rapports automatiques

Pour configurer des rapports automatiques dans Power BI Service:

1. Ouvrez le rapport dans Power BI Service
2. Cliquez sur "S'abonner" ou "Abonnements"
3. Configurez la fréquence d'envoi et les destinataires
4. Cliquez sur "Enregistrer et fermer"

### Partage du tableau de bord

Pour partager le tableau de bord avec d'autres utilisateurs:

1. Dans Power BI Service, ouvrez le rapport ou le tableau de bord
2. Cliquez sur "Partager"
3. Entrez les adresses e-mail des destinataires
4. Configurez les options de partage (autoriser le partage, autoriser la construction, etc.)
5. Cliquez sur "Partager"

## Bonnes pratiques

### Fréquence de surveillance recommandée

- **Critique**: Vérification horaire de l'état des composants et des métriques de santé
- **Standard**: Vérification quotidienne de toutes les métriques et activités
- **Routine**: Analyse hebdomadaire des tendances et des statistiques de gestion des comptes

### Interprétation des alertes

- **Composant déconnecté**: Vérifiez immédiatement l'état du serveur et des services
- **Utilisation élevée des ressources**: Examinez les processus en cours et planifiez une optimisation
- **Tentatives de connexion échouées répétées**: Évaluez un possible risque de sécurité

### Maintenance du tableau de bord

Pour maintenir les performances optimales du tableau de bord:

1. Actualisez régulièrement les données (au moins une fois par jour)
2. Vérifiez périodiquement la connexion à l'API CyberArk
3. Optimisez les requêtes de données si le volume augmente significativement
4. Mettez à jour le modèle Power BI lorsque de nouvelles fonctionnalités sont ajoutées

## Résolution des problèmes courants

### Problèmes de connexion aux données

Si les données ne se chargent pas correctement:

1. Vérifiez que l'API est en cours d'exécution (`http://<server-ip>:8000/api/health`)
2. Vérifiez les paramètres de connexion dans Power BI
3. Testez la connectivité réseau entre Power BI et le serveur d'API
4. Consultez les journaux d'API pour identifier les erreurs potentielles

### Visualisations incorrectes

Si les visualisations affichent des données incorrectes:

1. Vérifiez les formules des mesures utilisées
2. Assurez-vous que les filtres appliqués sont appropriés
3. Actualisez complètement les données
4. Recréez la visualisation si nécessaire

### Problèmes de performance

Si le tableau de bord est lent:

1. Réduisez la quantité de données visualisées en utilisant des filtres
2. Simplifiez les visualisations complexes
3. Optimisez les requêtes DAX utilisées dans les mesures
4. Vérifiez les ressources système du serveur hébergeant l'API

## Glossaire

- **CPM (Central Policy Manager)**: Composant CyberArk responsable de la gestion des mots de passe
- **PVWA (Password Vault Web Access)**: Interface web pour accéder au coffre-fort CyberArk
- **PSM (Privileged Session Manager)**: Composant gérant les sessions privilégiées
- **AAM (Application Access Manager)**: Composant gérant l'accès aux applications
- **Compte géré**: Compte dont les informations d'identification sont gérées par CyberArk
- **Coffre-fort (Vault)**: Serveur central de stockage sécurisé des informations d'identification
- **DAX (Data Analysis Expressions)**: Langage de formule utilisé dans Power BI