# Guide Power BI - CyberArk Health Dashboard

Ce guide détaille la création, la configuration et l'utilisation du tableau de bord Power BI pour le CyberArk Health Dashboard. Il couvre tous les aspects, de la connexion aux données à la personnalisation avancée.

## Configuration initiale

### Prérequis

- Power BI Desktop (version 2.93.641.0 ou supérieure)
- URL de l'API du CyberArk Health Dashboard
- Droits d'accès à l'API
- Connaissance de base de Power BI

### Installation de Power BI Desktop

1. Téléchargez Power BI Desktop depuis le [site officiel de Microsoft](https://powerbi.microsoft.com/desktop/)
2. Installez l'application en suivant les instructions
3. Lancez Power BI Desktop

## Connexion aux données

### Option 1: Utiliser le fichier PBIX prédéfini

1. Téléchargez le fichier `.pbix` fourni dans le répertoire `/powerbi/` du projet
2. Ouvrez le fichier dans Power BI Desktop
3. Cliquez sur "Transformer les données" dans le ruban Home
4. Mettez à jour les paramètres de connexion à l'API dans la fenêtre "Éditeur Power Query"
5. Cliquez sur "Fermer et appliquer"

### Option 2: Créer une connexion depuis zéro

1. Ouvrez Power BI Desktop
2. Cliquez sur "Obtenir les données" dans le ruban Home
3. Sélectionnez "Web" comme source de données
4. Entrez l'URL de l'API : `http://<serveur>:8000/api/dashboard`
5. Cliquez sur "OK"
6. Si nécessaire, configurez l'authentification et cliquez sur "Se connecter"
7. Dans la fenêtre "Navigateur", sélectionnez "Document" et cliquez sur "Transformer les données"
8. Dans l'éditeur Power Query, convertissez le JSON en tables utilisables :
   - Cliquez sur l'icône d'expansion à côté des colonnes de type Record ou List
   - Sélectionnez les colonnes à extraire
   - Répétez pour chaque niveau d'imbrication
9. Renommez les tables obtenues selon leur contenu
10. Cliquez sur "Fermer et appliquer"

## Organisation du modèle de données

### Tables principales

Le modèle de données recommandé comprend les tables suivantes :

1. **ComponentStatus** - État des composants CyberArk
   - Colonnes clés : ComponentName, Status, LastConnection, Version

2. **VaultStatus** - État global du coffre-fort CyberArk
   - Colonnes clés : TotalSafes, TotalAccounts, LicenseUsage, LicenseExpiry

3. **AccountsStatus** - Statistiques des comptes
   - Colonnes clés : ManagedAccounts, NonManagedAccounts

4. **AccountsByPlatform** - Distribution des comptes par plateforme
   - Colonnes clés : Platform, Count

5. **SystemHealth** - Métriques de santé système
   - Colonnes clés : CPUUsage, MemoryUsage, DiskUsage

6. **Activities** - Activités récentes
   - Colonnes clés : Timestamp, Username, Action, Component, Details

7. **FailedLogins** - Tentatives de connexion échouées
   - Colonnes clés : Timestamp, Username, Reason, SourceIP, AttemptCount

### Création de relations

Établissez les relations suivantes entre les tables :

1. **Activities** liée à **ComponentStatus** via le champ "Component"/"ComponentName"
2. **SystemHealth** en relation unique avec **VaultStatus**
3. **AccountsByPlatform** en relation un-à-plusieurs avec **AccountsStatus**

Pour créer une relation :
1. Allez dans l'onglet "Modèle" de Power BI Desktop
2. Faites glisser un champ d'une table vers le champ correspondant d'une autre table
3. Configurez la cardinalité et la direction du filtrage croisé selon vos besoins

## Création de mesures DAX

Les mesures DAX permettent de calculer des indicateurs clés. Voici quelques mesures essentielles :

### Pourcentage de composants connectés

```dax
PctComponentsConnected = 
DIVIDE(
    COUNTROWS(FILTER('ComponentStatus', 'ComponentStatus'[Status] = "Connected")),
    COUNTROWS('ComponentStatus')
) * 100
```

### Pourcentage de comptes gérés

```dax
PctManagedAccounts = 
DIVIDE(
    'AccountsStatus'[ManagedAccounts],
    'AccountsStatus'[ManagedAccounts] + 'AccountsStatus'[NonManagedAccounts]
) * 100
```

### État global du système

```dax
SystemHealthStatus = 
IF(
    MAX('SystemHealth'[CPUUsage]) > 90 || MAX('SystemHealth'[MemoryUsage]) > 90 || MAX('SystemHealth'[DiskUsage]) > 90,
    "Critical",
    IF(
        MAX('SystemHealth'[CPUUsage]) > 70 || MAX('SystemHealth'[MemoryUsage]) > 70 || MAX('SystemHealth'[DiskUsage]) > 70,
        "Warning",
        "Normal"
    )
)
```

### Nombre total de tentatives de connexion échouées

```dax
TotalFailedLogins = 
SUMX('FailedLogins', 'FailedLogins'[AttemptCount])
```

### Création d'une mesure

Pour créer une nouvelle mesure :
1. Cliquez sur "Nouvelle mesure" dans le ruban Modélisation
2. Entrez la formule DAX dans l'éditeur de formule
3. Nommez la mesure et cliquez sur la coche pour valider

## Création des visualisations

### Tableau de bord principal

Créez les visualisations suivantes pour le tableau de bord principal :

#### 1. Carte de score pour les composants connectés

1. Sélectionnez la visualisation "Carte" dans le panneau Visualisations
2. Faites glisser la mesure "PctComponentsConnected" dans le champ "Valeurs"
3. Formatez la carte :
   - Titre : "Composants connectés"
   - Catégorie : Pourcentage
   - Plage de valeurs : 0-100
   - Couleurs conditionnelles : Rouge (<70%), Jaune (70-90%), Vert (>90%)

#### 2. Graphique en anneau pour l'état des composants

1. Sélectionnez la visualisation "Graphique en anneau" dans le panneau Visualisations
2. Faites glisser "ComponentName" dans le champ "Légende"
3. Faites glisser "Status" dans le champ "Valeurs"
4. Formatez le graphique :
   - Titre : "État des composants"
   - Couleurs conditionnelles selon le statut

#### 3. Graphique à barres pour les comptes par plateforme

1. Sélectionnez la visualisation "Graphique à barres" dans le panneau Visualisations
2. Faites glisser "Platform" dans le champ "Axe"
3. Faites glisser "Count" dans le champ "Valeurs"
4. Formatez le graphique :
   - Titre : "Comptes par plateforme"
   - Triez par ordre décroissant de nombre de comptes

#### 4. Jauges pour l'utilisation des ressources

Créez trois jauges pour l'utilisation CPU, mémoire et disque :

1. Sélectionnez la visualisation "Jauge" dans le panneau Visualisations
2. Faites glisser "CPUUsage" dans le champ "Valeur"
3. Configurez la plage de valeurs : Min = 0, Max = 100
4. Définissez les plages de données :
   - 0-70 : Vert
   - 70-90 : Jaune
   - 90-100 : Rouge
5. Répétez pour MemoryUsage et DiskUsage

#### 5. Tableau pour les activités récentes

1. Sélectionnez la visualisation "Tableau" dans le panneau Visualisations
2. Faites glisser "Timestamp", "Username", "Action" et "Component" dans le champ "Valeurs"
3. Triez par "Timestamp" en ordre décroissant
4. Formatez le tableau :
   - Titre : "Activités récentes"
   - Appliquez un formatage conditionnel selon le type d'action

#### 6. Tableau pour les tentatives de connexion échouées

1. Sélectionnez la visualisation "Tableau" dans le panneau Visualisations
2. Faites glisser "Timestamp", "Username", "Reason" et "SourceIP" dans le champ "Valeurs"
3. Triez par "Timestamp" en ordre décroissant
4. Formatez le tableau :
   - Titre : "Tentatives de connexion échouées"
   - Appliquez un formatage conditionnel sur la colonne "Reason"

### Tableaux de bord additionnels

Créez des pages supplémentaires pour des analyses détaillées :

#### Page "Analyse des composants"

Contenant des visualisations détaillées pour chaque composant CyberArk :
- Chronologie de l'état de connexion
- Détails des versions
- Métriques spécifiques aux composants

#### Page "Gestion des comptes"

Axée sur les statistiques de gestion des comptes :
- Tendances du taux de gestion
- Distribution par type de compte
- Âge des mots de passe

#### Page "Sécurité"

Centrée sur les métriques de sécurité :
- Carte de chaleur des tentatives de connexion échouées
- Analyse des activités suspectes
- Tendances des accès

## Mise en page et conception

### Mise en page recommandée

```
┌────────────────────────────────────────┐
│ [Logo/Titre]        [Date/Heure]       │
├────────────┬────────────┬──────────────┤
│            │            │              │
│  État des  │ % Comptes  │  État des    │
│ composants │   gérés    │  ressources  │
│            │            │              │
├────────────┴────────┬───┴──────────────┤
│                     │                  │
│   Graphique des     │   Activités      │
│   comptes par       │   récentes       │
│   plateforme        │                  │
│                     │                  │
├─────────────────────┴──────────────────┤
│                                        │
│      Tentatives de connexion échouées  │
│                                        │
└────────────────────────────────────────┘
```

### Thème et style

1. **Appliquer un thème cohérent**
   - Cliquez sur "Vue" > "Thèmes"
   - Sélectionnez un thème professionnel ou importez un thème personnalisé

2. **Utiliser une palette de couleurs cohérente**
   - Rouge pour les états critiques
   - Jaune pour les avertissements
   - Vert pour les états normaux
   - Bleu pour les données neutres

3. **Ajouter un logo et des éléments d'identité visuelle**
   - Insérez le logo CyberArk
   - Utilisez des polices cohérentes avec l'identité visuelle

4. **Créer un arrière-plan personnalisé**
   - Importez une image d'arrière-plan discrète
   - Utilisez des zones transparentes pour délimiter les sections

## Interactivité et filtres

### Segments (Slicers)

Ajoutez les segments suivants pour filtrer les données :

1. **Segment de date**
   - Type : Chronologie ou liste déroulante
   - Permet de filtrer sur une période spécifique

2. **Segment de composant**
   - Type : Liste à choix multiples
   - Permet de filtrer par composant CyberArk

3. **Segment de sévérité**
   - Type : Boutons ou cases à cocher
   - Permet de filtrer les événements par niveau de sévérité

### Navigation entre pages

Ajoutez des boutons de navigation pour passer d'une page à l'autre :

1. Insérez des formes pour servir de boutons
2. Configurez l'action de chaque bouton :
   - Cliquez sur la forme
   - Dans le panneau Format, allez dans Action
   - Sélectionnez "Type d'action" = "Page"
   - Choisissez la page de destination

### Exploration des données (Drill-through)

Configurez l'exploration des données pour permettre aux utilisateurs d'approfondir l'analyse :

1. Créez une page de détail pour chaque entité principale (composants, comptes, etc.)
2. Configurez le drill-through :
   - Dans la page de détail, sélectionnez "Exploration" dans le panneau Visualisations
   - Ajoutez les champs sur lesquels l'exploration est possible
3. Les utilisateurs pourront faire un clic droit sur une valeur et sélectionner "Explorer" pour voir les détails

## Rafraîchissement des données

### Configuration du rafraîchissement automatique

Pour les tableaux de bord publiés sur Power BI Service :

1. Publiez votre rapport sur Power BI Service
2. Allez dans les paramètres du jeu de données
3. Sélectionnez "Planifier l'actualisation"
4. Configurez la fréquence de rafraîchissement (par exemple, toutes les heures)
5. Définissez l'heure de début et les jours de rafraîchissement

### Configuration de la passerelle de données

Pour accéder à l'API depuis Power BI Service :

1. Téléchargez et installez la passerelle de données personnelle
2. Configurez la passerelle dans Power BI Service
3. Liez votre jeu de données à la passerelle
4. Configurez les informations d'identification de la source de données

## Partage et distribution

### Publication sur Power BI Service

1. Dans Power BI Desktop, cliquez sur "Publier"
2. Connectez-vous à votre compte Power BI
3. Sélectionnez l'espace de travail de destination
4. Cliquez sur "Publier"

### Création d'un tableau de bord

1. Dans Power BI Service, ouvrez le rapport publié
2. Épinglez les visualisations au tableau de bord :
   - Survolez une visualisation
   - Cliquez sur l'icône d'épingle
   - Sélectionnez un tableau de bord existant ou créez-en un nouveau

### Partage et sécurité

1. **Partage direct**
   - Dans l'espace de travail, sélectionnez le tableau de bord
   - Cliquez sur "Partager"
   - Entrez les adresses e-mail des destinataires
   - Configurez les options de partage

2. **Sécurité au niveau des lignes**
   - Créez des rôles de sécurité dans Power BI Desktop
   - Définissez des expressions DAX pour filtrer les données selon le rôle
   - Publiez le rapport et configurez les membres des rôles

3. **Application Power BI**
   - Créez une application depuis votre espace de travail
   - Sélectionnez les rapports et tableaux de bord à inclure
   - Configurez la navigation et les détails de l'application
   - Publiez l'application et partagez-la avec votre organisation

## Personnalisation avancée

### Création de visuels personnalisés

1. **Importation de visuels**
   - Accédez à la galerie de visuels Power BI
   - Sélectionnez et importez des visuels pertinents pour votre cas d'usage

2. **Développement de visuels personnalisés**
   - Pour les développeurs, utilisez le SDK de visualisation Power BI
   - Créez des visuels spécifiques aux besoins de surveillance CyberArk

### Intégration de R ou Python

1. **Visualisations R**
   - Activez les scripts R dans Power BI Desktop
   - Créez des visualisations avancées avec R
   
   Exemple de script R pour une visualisation avancée :
   ```r
   library(ggplot2)
   
   # Créer un graphique de chaleur pour les tentatives de connexion
   ggplot(dataset, aes(x = Timestamp, y = SourceIP, fill = AttemptCount)) +
     geom_tile() +
     scale_fill_gradient(low = "blue", high = "red") +
     theme_minimal() +
     labs(title = "Carte de chaleur des tentatives de connexion échouées")
   ```

2. **Visualisations Python**
   - Activez les scripts Python dans Power BI Desktop
   - Utilisez des bibliothèques comme matplotlib ou seaborn
   
   Exemple de script Python :
   ```python
   import matplotlib.pyplot as plt
   import seaborn as sns
   
   # Créer une matrice de corrélation
   plt.figure(figsize=(10, 8))
   correlation_matrix = dataset.corr()
   sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
   plt.title("Corrélation entre les métriques système")
   ```

### Alertes et notifications

Configurez des alertes dans Power BI Service :

1. Ouvrez une visualisation de type carte ou jauge
2. Cliquez sur les trois points (...)
3. Sélectionnez "Gérer les alertes"
4. Cliquez sur "Ajouter une règle d'alerte"
5. Configurez les conditions et la fréquence des notifications

## Dépannage

### Problèmes courants et solutions

#### Les données ne se rafraîchissent pas

**Solutions possibles :**
- Vérifiez que l'URL de l'API est correcte
- Testez l'API dans un navigateur ou avec Postman
- Assurez-vous que les identifiants sont valides
- Vérifiez les paramètres de la passerelle de données

#### Erreurs de transformation des données

**Solutions possibles :**
- Vérifiez le format JSON renvoyé par l'API
- Utilisez l'éditeur de requêtes pour résoudre les problèmes de transformation
- Assurez-vous que les types de données sont corrects

#### Problèmes de performance

**Solutions possibles :**
- Réduisez la quantité de données chargées
- Optimisez les formules DAX
- Évitez les relations complexes dans le modèle
- Utilisez des requêtes directes au lieu d'importer les données

### Optimisations

1. **Optimisation des requêtes**
   - Filtrez les données à la source plutôt que dans Power BI
   - Utilisez des paramètres de requête pour limiter les données

2. **Optimisation des formules DAX**
   - Utilisez CALCULATE avec des filtres plutôt que des expressions IF complexes
   - Évitez les calculs imbriqués excessifs
   - Utilisez des variables pour stocker les calculs intermédiaires

3. **Optimisation du modèle de données**
   - Supprimez les colonnes inutilisées
   - Utilisez la compression des colonnes
   - Créez des tables d'agrégation pour les grands ensembles de données

## Conclusion

Ce guide vous a présenté les étapes nécessaires pour créer, configurer et utiliser un tableau de bord Power BI pour le CyberArk Health Dashboard. En suivant ces instructions, vous pourrez créer un outil de surveillance puissant et intuitif pour votre environnement CyberArk.

N'hésitez pas à explorer davantage les capacités de Power BI pour personnaliser et améliorer votre tableau de bord selon vos besoins spécifiques.