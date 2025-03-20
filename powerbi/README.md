# PowerBI pour CyberArk Health Dashboard

Ce répertoire contient le fichier modèle PowerBI pour visualiser les données du tableau de bord de santé CyberArk.

## Utilisation du modèle PowerBI

1. Téléchargez [Power BI Desktop](https://powerbi.microsoft.com/desktop/) si vous ne l'avez pas déjà
2. Ouvrez le fichier `CyberArk_Health_Dashboard.pbix` inclus dans ce répertoire
3. Lors de l'ouverture du fichier, vous serez invité à configurer la connexion à l'API
4. Entrez l'URL de l'API: `http://localhost:8000/api/dashboard`
5. Cliquez sur "Actualiser" pour charger les dernières données

## Création de votre propre tableau de bord

Si vous préférez créer votre propre tableau de bord, suivez ces étapes:

1. Ouvrez Power BI Desktop
2. Cliquez sur "Obtenir les données" > "Web"
3. Entrez l'URL de l'API: `http://localhost:8000/api/dashboard`
4. Cliquez sur "OK" et attendez que les données soient chargées
5. Explorez les données et créez vos propres visualisations

## Visualisations recommandées

Voici quelques visualisations recommandées pour votre tableau de bord:

1. **État des composants**:
   - Utilisez un visuel de type "Scorecard" pour afficher le pourcentage de composants connectés
   - Utilisez un graphique en anneau pour montrer les composants par statut

2. **Comptes**:
   - Utilisez un graphique à barres pour comparer les comptes gérés vs non gérés
   - Utilisez des indicateurs pour montrer les comptes en attente ou en échec

3. **Performance du système**:
   - Utilisez des jauges pour afficher l'utilisation CPU, mémoire et disque
   - Utilisez un graphique en courbes pour suivre l'évolution de la performance dans le temps

4. **Événements de sécurité**:
   - Utilisez un tableau pour afficher les activités récentes
   - Utilisez un filtre de date pour explorer les événements par période

## Actualisation des données

Pour configurer l'actualisation automatique des données:

1. Dans PowerBI Desktop, allez dans l'onglet "Accueil"
2. Cliquez sur "Actualiser"
3. Pour configurer une actualisation programmée, vous devrez publier le rapport sur PowerBI Service