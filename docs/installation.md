# Guide d'installation

Ce guide détaille les étapes nécessaires pour installer et configurer le tableau de bord de santé CyberArk.

## Prérequis

- Python 3.8 ou supérieur
- CyberArk PAM v12.0 ou supérieur avec accès API
- Accès administrateur à l'environnement CyberArk
- Power BI Desktop (optionnel, pour les visualisations avancées)

## Installation de base

### 1. Cloner le dépôt

```bash
git clone https://github.com/jacobi-black/cyberark-health-dashboard.git
cd cyberark-health-dashboard
```

### 2. Créer un environnement virtuel (recommandé)

```bash
# Sur Linux/Mac
python -m venv venv
source venv/bin/activate

# Sur Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer l'environnement

Copiez le fichier d'exemple et modifiez-le avec vos paramètres:

```bash
cp .env.example .env
# Modifiez .env avec vos paramètres
```

Voici les principaux paramètres à configurer:

```ini
# Mode démo (utilise les données exemples au lieu de se connecter à CyberArk)
# Mettez DEMO_MODE=false pour vous connecter à une vraie instance CyberArk
DEMO_MODE=true

# Configuration de l'API CyberArk
CYBERARK_API_URL=https://your-cyberark-instance.com/PasswordVault
CYBERARK_AUTH_TYPE=cyberark
CYBERARK_USERNAME=admin
CYBERARK_PASSWORD=password

# Configuration de la base de données
DB_CONNECTION_STRING=sqlite:///cyberark_health.db
```

### 5. Initialiser la base de données

```bash
python -c "from app.models import init_db; init_db()"
```

### 6. Démarrer l'application

```bash
python main.py
```

L'application sera accessible à l'adresse `http://localhost:8000` (ou l'IP/port que vous avez configuré).

## Déploiement en production

Pour un déploiement en production, il est recommandé de:

1. Utiliser une base de données PostgreSQL ou MySQL au lieu de SQLite
2. Configurer un serveur web (comme Nginx) comme proxy inverse
3. Utiliser un gestionnaire de processus (comme Supervisor ou systemd)
4. Activer HTTPS pour sécuriser les communications

### Exemple de configuration avec Nginx et systemd

#### Configuration Nginx

```nginx
server {
    listen 80;
    server_name your-server-name.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Configuration systemd

Créez un fichier `/etc/systemd/system/cyberark-dashboard.service`:

```ini
[Unit]
Description=CyberArk Health Dashboard
After=network.target

[Service]
User=cyberark
WorkingDirectory=/path/to/cyberark-health-dashboard
ExecStart=/path/to/cyberark-health-dashboard/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Activez et démarrez le service:

```bash
systemctl enable cyberark-dashboard
systemctl start cyberark-dashboard
```

## Mise à jour

Pour mettre à jour l'application:

```bash
cd /path/to/cyberark-health-dashboard
git pull
pip install -r requirements.txt
systemctl restart cyberark-dashboard  # Si vous utilisez systemd
```