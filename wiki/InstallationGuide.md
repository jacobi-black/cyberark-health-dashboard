# Guide d'Installation - CyberArk Health Dashboard

Ce guide fournit des instructions détaillées pour installer et configurer le CyberArk Health Dashboard dans différents environnements.

## Installation standard

### Prérequis

- Python 3.8 ou supérieur
- Accès à un environnement CyberArk PAM v12.0+ (optionnel en mode démo)
- Power BI Desktop (pour les visualisations)
- Droits d'administration sur le serveur d'installation

### Étapes d'installation

#### 1. Préparation de l'environnement

**Sous Linux (Ubuntu/Debian)**

```bash
# Mettre à jour les packages
sudo apt update && sudo apt upgrade -y

# Installer Python et pip si nécessaire
sudo apt install -y python3 python3-pip python3-venv

# Créer un répertoire pour l'application
mkdir -p /opt/cyberark-health-dashboard
cd /opt/cyberark-health-dashboard
```

**Sous Windows**

```powershell
# Créer un répertoire pour l'application
New-Item -ItemType Directory -Path "C:\CyberArkHealth" -Force
cd C:\CyberArkHealth
```

#### 2. Récupération du code source

**Option 1: Cloner depuis GitHub**

```bash
git clone https://github.com/jacobi-black/cyberark-health-dashboard.git .
```

**Option 2: Télécharger et extraire l'archive**

```bash
# Linux
wget https://github.com/jacobi-black/cyberark-health-dashboard/archive/main.zip
unzip main.zip
mv cyberark-health-dashboard-main/* .
rm -rf main.zip cyberark-health-dashboard-main/

# Windows PowerShell
Invoke-WebRequest -Uri "https://github.com/jacobi-black/cyberark-health-dashboard/archive/main.zip" -OutFile "main.zip"
Expand-Archive -Path main.zip -DestinationPath .
Move-Item -Path ".\cyberark-health-dashboard-main\*" -Destination .
Remove-Item -Path main.zip, cyberark-health-dashboard-main -Recurse -Force
```

#### 3. Création d'un environnement virtuel

**Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### 4. Installation des dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Pour les développeurs, installez également les outils de développement:

```bash
pip install -r requirements-dev.txt
```

#### 5. Configuration

Copiez le fichier d'exemple de configuration et modifiez-le selon vos besoins:

```bash
cp .env.example .env
```

Ouvrez le fichier `.env` dans votre éditeur préféré et configurez les paramètres suivants:

```ini
# Mode démo (utilise les données exemples au lieu de se connecter à CyberArk)
DEMO_MODE=true  # Définir à false pour l'environnement de production

# Configuration de l'API CyberArk
CYBERARK_API_URL=https://votre-cyberark-instance.com/PasswordVault
CYBERARK_AUTH_TYPE=cyberark  # ou ldap, radius, etc.
CYBERARK_USERNAME=nom_utilisateur
CYBERARK_PASSWORD=mot_de_passe

# Configuration de la base de données
DB_CONNECTION_STRING=sqlite:///cyberark_health.db  # SQLite par défaut
# Pour SQL Server, utilisez: mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server

# Configuration du collecteur de données
COLLECTOR_INTERVAL=3600  # Intervalle en secondes (1 heure par défaut)
COMPONENTS_TO_CHECK=CPM,PSM,PVWA,AAM Credential Provider

# Configuration de l'API
API_HOST=0.0.0.0
API_PORT=8000
```

#### 6. Initialisation de la base de données

```bash
python -c "from app.models import create_tables; create_tables()"
```

## Déploiement en production

### Déploiement avec systemd (Linux)

Créez un fichier service systemd:

```bash
sudo nano /etc/systemd/system/cyberark-health.service
```

Ajoutez le contenu suivant:

```ini
[Unit]
Description=CyberArk Health Dashboard
After=network.target

[Service]
User=cyberark
WorkingDirectory=/opt/cyberark-health-dashboard
ExecStart=/opt/cyberark-health-dashboard/venv/bin/python /opt/cyberark-health-dashboard/main.py
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=cyberark-health

[Install]
WantedBy=multi-user.target
```

Activez et démarrez le service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable cyberark-health
sudo systemctl start cyberark-health
```

### Déploiement avec Docker

#### 1. Créer un Dockerfile

Créez un fichier `Dockerfile` à la racine du projet:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copier les fichiers requis
COPY requirements.txt .
COPY app/ ./app/
COPY main.py .
COPY .env.example .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["python", "main.py"]
```

#### 2. Créer un fichier docker-compose.yml

```yaml
version: '3'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./:/app
    environment:
      - DEMO_MODE=true
      # Autres variables d'environnement
```

#### 3. Construire et démarrer le conteneur

```bash
docker-compose up -d
```

## Configuration avec une base de données externe

### SQL Server

1. Installez le driver ODBC pour SQL Server:

```bash
# Ubuntu/Debian
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
sudo apt update
sudo ACCEPT_EULA=Y apt install -y msodbcsql17 unixodbc-dev
```

2. Installez le package pyodbc:

```bash
pip install pyodbc
```

3. Configurez la chaîne de connexion dans le fichier `.env`:

```
DB_CONNECTION_STRING=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
```

### PostgreSQL

1. Installez le package psycopg2:

```bash
pip install psycopg2-binary
```

2. Configurez la chaîne de connexion dans le fichier `.env`:

```
DB_CONNECTION_STRING=postgresql://username:password@server/database
```

## Sécurisation de l'installation

### Recommandations de sécurité

1. **Protection des identifiants**:
   - Utilisez une gestion sécurisée des secrets (HashiCorp Vault, AWS Secrets Manager, etc.)
   - Créez un compte d'utilisateur dédié avec les privilèges minimaux nécessaires

2. **Accès réseau**:
   - Limitez l'accès à l'API en utilisant un pare-feu
   - Configurez un proxy inverse avec HTTPS (nginx, Apache)

3. **Surveillance**:
   - Mettez en place une surveillance des journaux
   - Configurez des alertes en cas d'erreurs ou d'accès non autorisés

### Configuration HTTPS avec Nginx

1. Installez Nginx:

```bash
sudo apt install nginx
```

2. Créez un fichier de configuration:

```bash
sudo nano /etc/nginx/sites-available/cyberark-health
```

3. Ajoutez la configuration:

```nginx
server {
    listen 443 ssl;
    server_name dashboard.votredomaine.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

4. Activez le site:

```bash
sudo ln -s /etc/nginx/sites-available/cyberark-health /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Vérification de l'installation

Après l'installation, vérifiez que tout fonctionne correctement:

1. **Vérifier que l'API est opérationnelle**:
   ```bash
   curl http://localhost:8000/api/health
   ```

2. **Vérifier les journaux**:
   ```bash
   # Si déployé avec systemd
   sudo journalctl -u cyberark-health
   ```

3. **Tester la collecte de données** (si DEMO_MODE=false):
   ```bash
   curl -X POST http://localhost:8000/api/collect
   ```

## Dépannage

### Problèmes courants

1. **L'API ne démarre pas**:
   - Vérifiez que tous les packages sont installés: `pip install -r requirements.txt`
   - Vérifiez les permissions du dossier et des fichiers
   - Consultez les journaux pour plus d'informations

2. **Erreurs de connexion à CyberArk**:
   - Vérifiez les identifiants dans le fichier `.env`
   - Vérifiez l'URL de l'API et l'accessibilité réseau
   - Testez la connexion manuellement avec un outil comme Postman

3. **Erreurs de base de données**:
   - Vérifiez la chaîne de connexion
   - Assurez-vous que l'utilisateur a les permissions nécessaires
   - Vérifiez que la base de données existe et est accessible

### Journalisation

Les journaux sont disponibles dans le fichier `cyberark_api.log` à la racine du projet. Pour augmenter le niveau de détail, modifiez la configuration de logging dans `app/cyberark_api.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Changer INFO en DEBUG pour plus de détails
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='cyberark_api.log'
)
```

## Mise à jour

Pour mettre à jour l'application:

1. Arrêtez le service:
   ```bash
   sudo systemctl stop cyberark-health  # Si déployé avec systemd
   ```

2. Sauvegardez les fichiers de configuration et la base de données:
   ```bash
   cp .env .env.backup
   cp cyberark_health.db cyberark_health.db.backup  # Si SQLite est utilisé
   ```

3. Téléchargez la dernière version:
   ```bash
   git pull origin main  # Si cloné depuis GitHub
   ```

4. Mettez à jour les dépendances:
   ```bash
   pip install -r requirements.txt
   ```

5. Appliquez les migrations de base de données si nécessaire:
   ```python
   python -c "from app.models import create_tables; create_tables()"
   ```

6. Redémarrez le service:
   ```bash
   sudo systemctl start cyberark-health  # Si déployé avec systemd
   ```