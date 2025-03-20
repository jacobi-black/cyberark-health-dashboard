# Résolution des problèmes

Ce guide vous aidera à résoudre les problèmes courants que vous pourriez rencontrer lors de l'utilisation du tableau de bord de santé CyberArk.

## Problèmes de connexion à l'API CyberArk

### Erreur d'authentification

**Symptôme**: Le message d'erreur "Échec de l'authentification" apparaît dans les logs.

**Solutions possibles**:
1. Vérifiez que le nom d'utilisateur et le mot de passe sont corrects dans le fichier `.env`
2. Assurez-vous que l'utilisateur a les autorisations nécessaires dans CyberArk
3. Vérifiez que le type d'authentification (`CYBERARK_AUTH_TYPE`) correspond à la configuration de votre environnement
4. Confirmez que l'URL de l'API est correcte et inclut `/PasswordVault`

### Erreur de connexion

**Symptôme**: Le message d'erreur "Impossible de se connecter à l'API" apparaît dans les logs.

**Solutions possibles**:
1. Vérifiez que l'URL de l'API est correcte dans le fichier `.env`
2. Assurez-vous que le serveur CyberArk est accessible depuis la machine où le tableau de bord est exécuté
3. Vérifiez les paramètres de pare-feu qui pourraient bloquer les connexions
4. Si vous utilisez HTTPS, vérifiez que `CYBERARK_VERIFY_SSL` est correctement configuré

## Problèmes de base de données

### Erreur de connexion à la base de données

**Symptôme**: Le message d'erreur "Échec de la connexion à la base de données" apparaît lors du démarrage.

**Solutions possibles**:
1. Vérifiez que la chaîne de connexion à la base de données est correcte dans le fichier `.env`
2. Assurez-vous que la base de données existe et est accessible
3. Pour SQLite, vérifiez les permissions du dossier où le fichier de base de données est stocké
4. Pour PostgreSQL/MySQL, vérifiez que le service de base de données est en cours d'exécution

### Erreurs de migration

**Symptôme**: Des erreurs apparaissent lors de l'initialisation de la base de données.

**Solutions possibles**:
1. Supprimez le fichier de base de données SQLite (si vous utilisez SQLite) et réinitialisez-la
2. Vérifiez que vous avez les privilèges nécessaires pour créer des tables dans la base de données

## Problèmes d'interface web

### Interface web inaccessible

**Symptôme**: Impossible d'accéder à l'interface web.

**Solutions possibles**:
1. Vérifiez que l'API est en cours d'exécution
2. Confirmez que les paramètres `API_HOST` et `API_PORT` sont correctement configurés dans le fichier `.env`
3. Si vous utilisez `0.0.0.0` comme hôte, essayez d'accéder à l'interface via `localhost` ou l'adresse IP de la machine
4. Vérifiez les pare-feu qui pourraient bloquer l'accès au port configuré

### Données non actualisées

**Symptôme**: Les données sur l'interface web ne sont pas actualisées.

**Solutions possibles**:
1. Cliquez sur le bouton "Actualiser les données" en haut de la page
2. Vérifiez que le collecteur de données fonctionne correctement en consultant les logs
3. Assurez-vous que la connexion à l'API CyberArk est fonctionnelle
4. Vérifiez que l'intervalle de collecte (`COLLECTOR_INTERVAL`) n'est pas trop long

## Problèmes de collecte de données

### Aucune donnée collectée

**Symptôme**: Le tableau de bord n'affiche aucune donnée.

**Solutions possibles**:
1. Si vous n'êtes pas en mode démo, vérifiez la connexion à l'API CyberArk
2. Consultez les logs pour détecter d'éventuelles erreurs lors de la collecte de données
3. Forcez une collecte de données via l'API: `curl -X POST http://localhost:8000/api/collect`
4. Vérifiez que les composants spécifiés dans `COMPONENTS_TO_CHECK` sont corrects

## Consultation des logs

Les logs de l'application peuvent fournir des informations précieuses pour diagnostiquer les problèmes:

- **API**: `api.log`
- **CyberArk API**: `cyberark_api.log`
- **Collecteur de données**: Inclus dans les logs standards

## Obtenir de l'aide supplémentaire

Si vous ne parvenez pas à résoudre votre problème, vous pouvez:

1. Créer une issue sur GitHub avec une description détaillée du problème
2. Inclure les logs pertinents (après avoir supprimé les informations sensibles)
3. Préciser les étapes pour reproduire le problème