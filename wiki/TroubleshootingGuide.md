# Guide de Dépannage - CyberArk Health Dashboard

Ce guide fournit des solutions aux problèmes courants rencontrés lors de l'installation, de la configuration et de l'utilisation du CyberArk Health Dashboard.

## Problèmes d'installation

### L'installation des dépendances échoue

**Problème** : Erreurs lors de l'installation des packages Python avec `pip install -r requirements.txt`.

**Solutions possibles** :

1. **Mettre à jour pip** :
   ```bash
   pip install --upgrade pip
   ```

2. **Vérifier la compatibilité Python** :
   - Assurez-vous d'utiliser Python 3.8 ou supérieur
   ```bash
   python --version
   ```

3. **Installer les packages un par un** :
   ```bash
   pip install fastapi
   pip install uvicorn
   pip install sqlalchemy
   # etc.
   ```

4. **Résoudre les dépendances manquantes du système** :
   
   Sur Ubuntu/Debian :
   ```bash
   sudo apt update
   sudo apt install -y python3-dev build-essential libssl-dev libffi-dev
   ```
   
   Sur RHEL/CentOS :
   ```bash
   sudo yum install -y python3-devel gcc openssl-devel libffi-devel
   ```

5. **Utiliser un environnement virtuel propre** :
   ```bash
   python -m venv fresh_venv
   source fresh_venv/bin/activate  # ou fresh_venv\Scripts\activate sur Windows
   pip install -r requirements.txt
   ```

### Le service ne démarre pas

**Problème** : Le service systemd ou le conteneur Docker ne démarre pas correctement.

**Solutions possibles** :

1. **Vérifier les journaux systemd** :
   ```bash
   sudo journalctl -u cyberark-health.service -n 50
   ```

2. **Vérifier les permissions** :
   ```bash
   sudo chown -R cyberark:cyberark /opt/cyberark-health-dashboard
   sudo chmod -R 755 /opt/cyberark-health-dashboard
   ```

3. **Tester le démarrage manuel** :
   ```bash
   cd /opt/cyberark-health-dashboard
   source venv/bin/activate
   python main.py
   ```

4. **Vérifier le fichier .env** :
   - Assurez-vous que toutes les variables d'environnement requises sont définies
   - Vérifiez les formats des URL et des chemins

5. **Pour Docker** :
   ```bash
   docker logs cyberark-health-container
   ```

## Problèmes de connexion à CyberArk

### Erreur d'authentification

**Problème** : Échec de l'authentification à l'API CyberArk.

**Solutions possibles** :

1. **Vérifier les identifiants** :
   - Assurez-vous que les valeurs `CYBERARK_USERNAME` et `CYBERARK_PASSWORD` sont correctes
   - Vérifiez que le compte n'est pas verrouillé ou expiré

2. **Vérifier l'URL de l'API** :
   - Format correct : `https://votre-cyberark-instance.com/PasswordVault`
   - Assurez-vous que l'URL est accessible depuis le serveur où tourne l'application

3. **Vérifier la méthode d'authentification** :
   - Assurez-vous que `CYBERARK_AUTH_TYPE` correspond à la méthode configurée (cyberark, ldap, radius)

4. **Vérifier les journaux** :
   - Examinez le fichier `cyberark_api.log` pour des erreurs détaillées
   - Définissez un niveau de journalisation plus détaillé

   ```python
   # Dans app/cyberark_api.py
   logging.basicConfig(
       level=logging.DEBUG,  # Changer de INFO à DEBUG
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       filename='cyberark_api.log'
   )
   ```

5. **Tester l'API manuellement** :
   ```bash
   curl -X POST "https://votre-cyberark-instance.com/PasswordVault/API/auth/cyberark/Logon" \
       -H "Content-Type: application/json" \
       -d '{"username":"votreUtilisateur", "password":"votreMotDePasse"}'
   ```

### Erreur de certificat SSL

**Problème** : Erreurs SSL lors de la connexion à l'API CyberArk.

**Solutions possibles** :

1. **Installer les certificats CA** :
   - Assurez-vous que les certificats CA de votre organisation sont installés sur le serveur

2. **Configurer les certificats dans Python** :
   ```python
   # Dans app/cyberark_api.py, ajouter
   import os
   os.environ['REQUESTS_CA_BUNDLE'] = '/chemin/vers/votre/ca-bundle.pem'
   ```

3. **Alternative (non recommandée pour la production)** :
   ```python
   # Dans app/cyberark_api.py
   import requests
   requests.packages.urllib3.disable_warnings()
   session = requests.Session()
   session.verify = False
   ```

4. **Tester avec curl** :
   ```bash
   curl -k https://votre-cyberark-instance.com/PasswordVault/API/auth/Logon
   ```

## Problèmes de base de données

### Erreurs de connexion à la base de données

**Problème** : L'application ne peut pas se connecter à la base de données.

**Solutions possibles** :

1. **Vérifier la chaîne de connexion** :
   - Pour SQLite : `sqlite:///cyberark_health.db`
   - Pour PostgreSQL : `postgresql://utilisateur:motdepasse@hote:port/base`
   - Pour SQL Server : `mssql+pyodbc://utilisateur:motdepasse@serveur/base?driver=ODBC+Driver+17+for+SQL+Server`

2. **Vérifier l'existence de la base de données** :
   - Pour SQLite, vérifiez si le fichier existe
   - Pour d'autres bases de données, vérifiez que la base existe et est accessible

3. **Vérifier les permissions** :
   - Assurez-vous que l'utilisateur a les permissions nécessaires pour lire/écrire dans la base

4. **Initialiser la base de données** :
   ```bash
   python -c "from app.models import create_tables; create_tables()"
   ```

5. **Tester la connexion manuellement** :
   ```python
   from sqlalchemy import create_engine
   engine = create_engine('votre_chaine_de_connexion')
   connection = engine.connect()
   connection.close()
   ```

### Erreurs de migration ou de schéma

**Problème** : Erreurs liées au schéma de la base de données ou aux migrations.

**Solutions possibles** :

1. **Réinitialiser la base de données** (perte de données) :
   - Pour SQLite : supprimer le fichier `cyberark_health.db`
   - Pour PostgreSQL : `DROP DATABASE nom_base; CREATE DATABASE nom_base;`
   - Puis réinitialiser : `python -c "from app.models import create_tables; create_tables()"`

2. **Identifier les tables problématiques** :
   ```python
   from sqlalchemy import inspect
   from sqlalchemy import create_engine
   
   engine = create_engine('votre_chaine_de_connexion')
   inspector = inspect(engine)
   
   # Lister les tables existantes
   print(inspector.get_table_names())
   
   # Lister les colonnes d'une table
   for column in inspector.get_columns('nom_table'):
       print(column)
   ```

3. **Backup et restauration** :
   - Créez un backup avant toute opération risquée
   - Pour SQLite : `cp cyberark_health.db cyberark_health.db.backup`

## Problèmes de collecte de données

### La collecte de données échoue

**Problème** : Le processus de collecte de données depuis CyberArk échoue.

**Solutions possibles** :

1. **Vérifier les permissions de l'utilisateur CyberArk** :
   - L'utilisateur doit avoir les permissions pour accéder aux données requises
   - Vérifiez les restrictions réseau ou pare-feu

2. **Activer le mode démo pour les tests** :
   - Dans le fichier `.env`, définissez `DEMO_MODE=true`
   - Cela utilisera des données d'exemple au lieu de se connecter à CyberArk

3. **Vérifier le fichier de journal** :
   - Examinez `cyberark_api.log` pour des erreurs détaillées

4. **Tester la collecte individuellement** :
   ```bash
   curl -X POST http://localhost:8000/api/collect
   ```

5. **Vérifier les composants configurés** :
   - Assurez-vous que les valeurs dans `COMPONENTS_TO_CHECK` existent dans votre environnement CyberArk

### La collecte programmée ne s'exécute pas

**Problème** : La collecte automatique à intervalles réguliers ne s'exécute pas.

**Solutions possibles** :

1. **Vérifier l'intervalle configuré** :
   - Assurez-vous que `COLLECTOR_INTERVAL` est défini correctement (en secondes)

2. **Vérifier que le planificateur est actif** :
   - Examinez les journaux pour voir si le planificateur démarre correctement

3. **Redémarrer l'application** :
   ```bash
   sudo systemctl restart cyberark-health
   ```

4. **Vérifier que le processus reste actif** :
   ```bash
   ps aux | grep python
   ```

5. **Alternative : configurer un cron job** :
   ```bash
   crontab -e
   ```
   Ajouter :
   ```
   0 * * * * curl -X POST http://localhost:8000/api/collect > /dev/null 2>&1
   ```

## Problèmes d'API REST

### L'API n'est pas accessible

**Problème** : Impossible d'accéder à l'API REST.

**Solutions possibles** :

1. **Vérifier que l'application est en cours d'exécution** :
   ```bash
   ps aux | grep uvicorn
   ```

2. **Vérifier la configuration de l'API** :
   - Assurez-vous que `API_HOST` et `API_PORT` sont correctement définis
   - Pour l'accès depuis d'autres machines, utilisez `API_HOST=0.0.0.0`

3. **Tester localement** :
   ```bash
   curl http://localhost:8000/api/health
   ```

4. **Vérifier les pare-feu** :
   ```bash
   sudo ufw status
   ```
   ou
   ```bash
   sudo iptables -L
   ```

5. **Vérifier les journaux d'erreur** :
   ```bash
   sudo journalctl -u cyberark-health -n 100
   ```

### Erreurs 500 de l'API

**Problème** : L'API répond avec des erreurs 500 (Internal Server Error).

**Solutions possibles** :

1. **Consulter les journaux d'application** :
   ```bash
   tail -n 100 cyberark_api.log
   ```

2. **Activer le mode de débogage** :
   - Dans le fichier de configuration ou les variables d'environnement:
   ```
   DEBUG=true
   ```

3. **Vérifier les erreurs de base de données** :
   - Assurez-vous que la base de données est accessible et contient les données nécessaires

4. **Redémarrer l'application** :
   ```bash
   sudo systemctl restart cyberark-health
   ```

5. **Tester des endpoints spécifiques** :
   ```bash
   curl http://localhost:8000/api/health
   curl http://localhost:8000/api/components
   ```

## Problèmes Power BI

### Erreur de connexion à l'API depuis Power BI

**Problème** : Power BI ne peut pas se connecter à l'API du CyberArk Health Dashboard.

**Solutions possibles** :

1. **Vérifier l'accessibilité réseau** :
   - Assurez-vous que le serveur d'API est accessible depuis la machine exécutant Power BI
   - Testez avec un navigateur ou curl depuis cette machine

2. **Configurer les paramètres d'authentification** :
   - Si nécessaire, configurez les informations d'identification dans Power BI

3. **Vérifier le format de l'URL** :
   - URL correcte : `http://serveur:8000/api/dashboard`
   - Testez d'abord dans un navigateur

4. **Examiner les erreurs Power BI** :
   - Cliquez sur "Voir les détails" dans les messages d'erreur de Power BI

5. **Tester avec Postman** :
   - Utilisez Postman pour tester l'API et assurez-vous qu'elle renvoie un JSON valide

### Les données ne s'actualisent pas dans Power BI

**Problème** : Les données dans Power BI ne se mettent pas à jour.

**Solutions possibles** :

1. **Actualiser manuellement** :
   - Cliquez sur "Actualiser" dans Power BI

2. **Vérifier les paramètres d'actualisation** :
   - Dans Power BI Desktop : Accueil > Actualiser
   - Dans Power BI Service : Planifier l'actualisation

3. **Vérifier les informations d'identification** :
   - Dans Power BI Desktop : Accueil > Transformer les données > Paramètres de la source de données

4. **Forcer une collecte de données** :
   ```bash
   curl -X POST http://localhost:8000/api/collect
   ```

5. **Vérifier le format des dates** :
   - Assurez-vous que le format des dates est compatible entre l'API et Power BI

## Problèmes de performance

### L'API est lente à répondre

**Problème** : Les requêtes API prennent trop de temps à répondre.

**Solutions possibles** :

1. **Vérifier la charge du serveur** :
   ```bash
   top
   ```

2. **Optimiser la base de données** :
   - Ajoutez des index sur les colonnes fréquemment utilisées
   ```sql
   CREATE INDEX idx_component_status_created_at ON component_status(created_at);
   CREATE INDEX idx_activities_timestamp ON activities(timestamp);
   ```

3. **Limiter les données retournées** :
   - Utilisez des paramètres comme `limit` et `from_date`/`to_date`

4. **Vérifier la mémoire disponible** :
   ```bash
   free -m
   ```

5. **Mettre en cache les résultats** :
   - Implémenter une mise en cache des requêtes fréquentes
   ```python
   from fastapi_cache import FastAPICache
   from fastapi_cache.backends.redis import RedisBackend
   from fastapi_cache.decorator import cache
   
   @app.on_event("startup")
   async def startup():
       redis = aioredis.from_url("redis://localhost")
       FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
   
   @app.get("/api/dashboard")
   @cache(expire=60)  # Cache pendant 60 secondes
   async def get_dashboard():
       # ...
   ```

### Consommation de mémoire excessive

**Problème** : L'application consomme trop de mémoire.

**Solutions possibles** :

1. **Surveiller l'utilisation de la mémoire** :
   ```bash
   ps aux | grep python
   ```

2. **Limiter les données en mémoire** :
   - Utilisez le streaming pour les grandes collections
   - Paginez les résultats

3. **Nettoyer les anciennes données** :
   - Implémentez une politique de rétention des données
   ```sql
   DELETE FROM activities WHERE timestamp < DATE_SUB(NOW(), INTERVAL 90 DAY);
   ```

4. **Optimiser les requêtes SQLAlchemy** :
   ```python
   # Au lieu de charger tous les objets
   results = db.query(Activity).all()
   
   # Utilisez la pagination
   results = db.query(Activity).limit(100).offset(page * 100).all()
   ```

5. **Redémarrer périodiquement le service** :
   - Configurez un redémarrage périodique pour éviter les fuites de mémoire

## Problèmes divers

### Problèmes de journalisation

**Problème** : Les journaux ne sont pas générés correctement ou sont trop volumineux.

**Solutions possibles** :

1. **Configurer la rotation des journaux** :
   ```python
   import logging
   from logging.handlers import RotatingFileHandler
   
   handler = RotatingFileHandler('cyberark_api.log', maxBytes=10485760, backupCount=5)
   logging.basicConfig(level=logging.INFO, handlers=[handler])
   ```

2. **Ajuster le niveau de journalisation** :
   ```python
   # Plus détaillé pour le débogage
   logging.basicConfig(level=logging.DEBUG)
   
   # Moins détaillé pour la production
   logging.basicConfig(level=logging.WARNING)
   ```

3. **Vérifier les permissions des fichiers de journal** :
   ```bash
   sudo chown cyberark:cyberark cyberark_api.log
   sudo chmod 644 cyberark_api.log
   ```

### Intégration avec d'autres outils

**Problème** : Difficultés à intégrer avec d'autres outils ou systèmes.

**Solutions possibles** :

1. **Utiliser l'API REST** :
   - Tous les systèmes peuvent intégrer via l'API REST
   - Consultez la documentation de l'API pour les points d'accès disponibles

2. **Exporter des données** :
   - Ajoutez un endpoint d'exportation au format CSV ou JSON
   ```python
   @app.get("/api/export/csv")
   def export_csv():
       # Logique d'exportation CSV
       return FileResponse("export.csv")
   ```

3. **Utiliser des webhooks** :
   - Implémentez des notifications par webhook pour les événements importants

## Contact et support

Si les solutions ci-dessus ne résolvent pas votre problème, contactez l'équipe de support via les canaux suivants :

- **Issue GitHub** : Ouvrez une issue sur le dépôt GitHub du projet
- **Email** : support@cyberark-health-dashboard.com (fictif)
- **Forum** : https://community.cyberark-health-dashboard.com/support (fictif)

Lors de la demande de support, incluez les informations suivantes :
- Version du CyberArk Health Dashboard
- Journaux pertinents
- Description détaillée du problème
- Étapes pour reproduire le problème
- Environnement d'exécution (OS, version Python, etc.)