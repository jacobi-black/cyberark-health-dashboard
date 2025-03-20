# Guide de création du tableau de bord Power BI pour CyberArk Health Dashboard

Ce guide vous guidera à travers le processus de création d'un tableau de bord Power BI pour visualiser les données de santé de votre environnement CyberArk.

## Prérequis

- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) installé sur votre poste de travail
- API CyberArk Health Dashboard opérationnelle
- Connaissances de base de Power BI

## Configuration initiale

1. Téléchargez et ouvrez Power BI Desktop
2. Cliquez sur **Obtenir les données** > **Web**
3. Dans le champ URL, entrez l'URL de l'API CyberArk Health Dashboard:
   ```
   http://votre-serveur:8000/api/dashboard
   ```
4. Cliquez sur **OK** et sélectionnez **JSON** comme format de source de données
5. Cliquez sur **Charger** pour importer les données

## Création des mesures

Une fois les données chargées, créez les mesures suivantes dans Power BI:

### 1. Pourcentage de composants connectés

```
PctComponentsConnected = 
VAR TotalComponents = SUM('component_status'[Total Amount])
VAR ConnectedComponents = SUM('component_status'[Connected])
RETURN
    IF(TotalComponents > 0, DIVIDE(ConnectedComponents, TotalComponents) * 100, 0)
```

### 2. Pourcentage de comptes gérés

```
PctManagedAccounts = 
VAR TotalAccounts = 'accounts_status'[Total_Accounts]
VAR ManagedAccounts = 'accounts_status'[Managed_Accounts]
RETURN
    IF(TotalAccounts > 0, DIVIDE(ManagedAccounts, TotalAccounts) * 100, 0)
```

### 3. État de santé du système

```
SystemHealthStatus = 
VAR CPUStatus = IF('system_health'[CPU_Usage] > 90, "Critical", IF('system_health'[CPU_Usage] > 75, "Warning", "Normal"))
VAR MemoryStatus = IF('system_health'[Memory_Usage] > 90, "Critical", IF('system_health'[Memory_Usage] > 75, "Warning", "Normal"))
VAR DiskStatus = IF('system_health'[Disk_Usage] > 90, "Critical", IF('system_health'[Disk_Usage] > 75, "Warning", "Normal"))
RETURN
    IF(CPUStatus = "Critical" || MemoryStatus = "Critical" || DiskStatus = "Critical", "Critical",
    IF(CPUStatus = "Warning" || MemoryStatus = "Warning" || DiskStatus = "Warning", "Warning", "Normal"))
```

## Création des visualisations

### 1. Tableau de bord de vue d'ensemble

Créez une nouvelle page nommée "Vue d'ensemble" et ajoutez les visualisations suivantes:

#### a. Cartes pour les métriques clés

- **Carte 1**: Pourcentage de composants connectés (mesure `PctComponentsConnected`)
  - Format: Ajoutez le symbole % et une décimale
  - Définir des couleurs conditionnelles: Rouge (<90%), Jaune (<95%), Vert (>=95%)

- **Carte 2**: Pourcentage de comptes gérés (mesure `PctManagedAccounts`)
  - Format: Ajoutez le symbole % et une décimale
  - Définir des couleurs conditionnelles: Rouge (<70%), Jaune (<90%), Vert (>=90%)

- **Carte 3**: État de santé du système (mesure `SystemHealthStatus`)
  - Format: Texte sans décimale
  - Définir des couleurs conditionnelles: Rouge ("Critical"), Jaune ("Warning"), Vert ("Normal")

#### b. Graphique en anneau pour l'état des composants

- Créez un graphique en anneau montrant la répartition des composants par état
  - Valeurs: COUNT de 'Component Type'
  - Légende: 'Status'
  - Titre: "État des composants"

#### c. Table des composants déconnectés

- Créez une table filtrée pour afficher uniquement les composants déconnectés
  - Colonnes: 'Component Type', 'Component Version', 'IP Address', 'Last Connection'
  - Filtre: 'Connected' = FALSE
  - Titre: "Composants déconnectés"

### 2. Page des détails des composants

Créez une nouvelle page nommée "Composants" avec les visualisations suivantes:

#### a. Graphique à barres pour les types de composants

- Créez un graphique à barres empilées montrant les composants connectés/déconnectés
  - Axe X: 'Component Type'
  - Axe Y: Count de 'Components'
  - Légende: 'Connected' (True/False)
  - Titre: "État de connexion par type de composant"

#### b. Table détaillée des composants

- Créez une table montrant tous les détails des composants
  - Colonnes: 'Component Type', 'Component Version', 'IP Address', 'Connected', 'Last Connection', 'OS'
  - Titre: "Détails des composants"

### 3. Page de gestion des comptes

Créez une nouvelle page nommée "Comptes" avec les visualisations suivantes:

#### a. Graphique à barres pour la répartition des comptes

- Créez un graphique à barres montrant la répartition des comptes
  - Données: 'Managed_Accounts', 'Non_Managed_Accounts', 'Pending_Accounts', 'Failed_Accounts'
  - Titre: "Répartition des comptes"

#### b. Graphique en jauge pour le pourcentage de comptes gérés

- Créez une jauge pour afficher le pourcentage de comptes gérés
  - Valeur: mesure `PctManagedAccounts`
  - Valeur minimale: 0
  - Valeur maximale: 100
  - Cibles: 90 (vert), 70 (jaune), <70 (rouge)
  - Titre: "Pourcentage de comptes gérés"

### 4. Page des événements récents

Créez une nouvelle page nommée "Événements" avec les visualisations suivantes:

#### a. Table des événements récents

- Créez une table pour afficher les événements récents
  - Colonnes: 'Timestamp', 'EventType', 'Username', 'Source_IP', 'Severity', 'Description'
  - Trier par: 'Timestamp' (décroissant)
  - Titre: "Événements récents"

#### b. Graphique en anneau pour les types d'événements

- Créez un graphique en anneau pour afficher la répartition des types d'événements
  - Valeurs: COUNT de 'EventType'
  - Légende: 'EventType'
  - Titre: "Types d'événements"

#### c. Graphique en anneau pour la sévérité des événements

- Créez un graphique en anneau pour afficher la répartition de la sévérité des événements
  - Valeurs: COUNT de 'Severity'
  - Légende: 'Severity'
  - Titre: "Sévérité des événements"

### 5. Page de santé du système

Créez une nouvelle page nommée "Système" avec les visualisations suivantes:

#### a. Jauges pour les métriques système

- **Jauge 1**: Utilisation CPU
  - Valeur: 'CPU_Usage'
  - Minimum: 0
  - Maximum: 100
  - Cibles: 75 (vert), 90 (jaune), >90 (rouge)
  - Titre: "Utilisation CPU (%)"

- **Jauge 2**: Utilisation mémoire
  - Valeur: 'Memory_Usage'
  - Minimum: 0
  - Maximum: 100
  - Cibles: 75 (vert), 90 (jaune), >90 (rouge)
  - Titre: "Utilisation mémoire (%)"

- **Jauge 3**: Utilisation disque
  - Valeur: 'Disk_Usage'
  - Minimum: 0
  - Maximum: 100
  - Cibles: 75 (vert), 90 (jaune), >90 (rouge)
  - Titre: "Utilisation disque (%)"

#### b. Carte pour la latence réseau

- Créez une carte pour afficher la latence réseau
  - Valeur: 'Network_Latency'
  - Format: 1 décimale, suffixe "ms"
  - Titre: "Latence réseau (ms)"

#### c. Carte pour la dernière sauvegarde

- Créez une carte pour afficher la date de la dernière sauvegarde
  - Valeur: 'Last_Backup'
  - Format: Date/heure
  - Titre: "Dernière sauvegarde"

## Configuration des segments et filtres

### 1. Ajouter des segments

Ajoutez les segments suivants à toutes les pages:

- **Segment par type de composant**: Basé sur 'Component Type'
- **Segment par sévérité**: Basé sur 'Severity' (pour les pages avec des événements)
- **Segment par statut de connexion**: Basé sur 'Connected' (True/False)

### 2. Ajouter des filtres croisés

Configurez des filtres croisés pour permettre aux utilisateurs de:

- Filtrer les événements par type de composant
- Filtrer les composants par statut
- Filtrer les comptes par type de gestion

## Configuration de l'actualisation des données

1. Cliquez sur **Fichier** > **Options et paramètres** > **Paramètres de source de données**
2. Sélectionnez la source de données API et cliquez sur **Modifier les autorisations**
3. Configurez l'actualisation pour utiliser les informations d'identification du système
4. Définissez une planification d'actualisation (par exemple, toutes les 30 minutes)

## Personnalisation de l'apparence

### 1. Appliquer un thème

1. Cliquez sur **Affichage** > **Thèmes**
2. Sélectionnez un thème approprié (recommandé: "Corporatif" ou un thème personnalisé aux couleurs de votre entreprise)

### 2. Personnaliser les couleurs

1. Pour les graphiques en anneau et les jauges, utilisez des couleurs cohérentes:
   - Vert: #00B050 (pour les états OK)
   - Jaune: #FFC000 (pour les avertissements)
   - Rouge: #C00000 (pour les états critiques)

### 3. Configuration des titres et des étiquettes

1. Assurez-vous que tous les graphiques ont des titres clairs
2. Ajoutez des descriptions aux visualisations complexes
3. Utilisez une terminologie cohérente dans tout le tableau de bord

## Exemple de disposition

```
+---------------------------------------------------------------+
|                       VUE D'ENSEMBLE                          |
+---------------+---------------+---------------+---------------+
| Composants    | Comptes       | Santé du      | État des      |
| Connectés (%) | Gérés (%)     | Système       | Composants    |
| [Carte]       | [Carte]       | [Carte]       | [Anneau]      |
+---------------+---------------+---------------+---------------+
|                                              |                |
| Composants déconnectés                       | Événements     |
| [Table]                                      | récents        |
|                                              | [Table]        |
+---------------------------------------------------------------+
```

## Publication et partage

1. Cliquez sur **Publier** pour publier le tableau de bord sur Power BI Service
2. Configurez une passerelle de données pour l'actualisation automatique
3. Partagez le tableau de bord avec les utilisateurs concernés
4. Configurez des alertes pour les métriques critiques

## Conseils pour l'analyse

Une fois le tableau de bord configuré, surveiller en particulier:

1. Les composants déconnectés ou en erreur
2. Les augmentations d'utilisation des ressources système
3. Les tentatives de connexion échouées répétées
4. Les échecs d'opérations sur les comptes
5. Les violations de politique

## Dépannage

Si les données ne s'actualisent pas correctement:

1. Vérifiez que l'API est accessible
2. Vérifiez les informations d'identification
3. Testez l'URL de l'API dans un navigateur
4. Vérifiez la passerelle de données (si utilisée)
5. Consultez les journaux de Power BI pour les erreurs d'actualisation