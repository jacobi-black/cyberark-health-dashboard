# API Reference - CyberArk Health Dashboard

Ce document détaille les points d'accès de l'API REST fournie par CyberArk Health Dashboard.

## Informations générales

- **URL de base**: `http://votre-serveur:8000`
- **Format des réponses**: JSON
- **Authentification**: Aucune (pour usage interne uniquement)
- **Documentation OpenAPI**: `/docs` ou `/redoc`

## Points d'accès de l'API

### Vérification de l'état de santé

```
GET /api/health
```

Vérifie si l'API est opérationnelle.

**Réponse**:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2023-04-20T15:45:00Z"
}
```

### Tableau de bord complet

```
GET /api/dashboard
```

Récupère toutes les données du tableau de bord en une seule requête.

**Réponse**:
```json
{
  "component_status": { ... },
  "vault_status": { ... },
  "accounts_status": { ... },
  "system_health": { ... },
  "recent_activities": [ ... ],
  "failed_logins": [ ... ],
  "last_update": "2023-04-20T15:45:00Z"
}
```

### État des composants

```
GET /api/components
```

Récupère l'état de tous les composants CyberArk.

**Paramètres optionnels**:
- `?component_type=CPM` - Filtre par type de composant
- `?connected=true` - Filtre par état de connexion

**Réponse**:
```json
{
  "Items": [
    {
      "Component Type": "CPM",
      "Total Amount": 3,
      "Connected": 3,
      "Disconnected": 0,
      "Status": "OK",
      "Components": [ ... ]
    },
    ...
  ]
}
```

### État du coffre-fort

```
GET /api/vault
```

Récupère les informations sur l'état du coffre-fort CyberArk.

**Réponse**:
```json
{
  "Safes": {
    "Total_Safes": 45,
    "Total_Accounts": 1250,
    "Version": "12.6.0",
    "License_Status": "Valid",
    "License_Expiration": "2025-12-31T00:00:00Z"
  }
}
```

### État des comptes

```
GET /api/accounts
```

Récupère les statistiques sur les comptes gérés dans CyberArk.

**Réponse**:
```json
{
  "value": {
    "Total_Accounts": 1250,
    "Managed_Accounts": 980,
    "Non_Managed_Accounts": 270,
    "Pending_Accounts": 5,
    "Failed_Accounts": 3
  }
}
```

### Santé du système

```
GET /api/system
```

Récupère les métriques de santé du système.

**Réponse**:
```json
{
  "CPU_Usage": 35.5,
  "Memory_Usage": 42.3,
  "Disk_Usage": 68.7,
  "Network_Latency": 5.2,
  "Last_Backup": "2023-04-20T08:30:00Z"
}
```

### Événements récents

```
GET /api/events
```

Récupère les événements de sécurité récents.

**Paramètres optionnels**:
- `?limit=10` - Nombre d'événements à récupérer (défaut: 10)
- `?severity=Warning` - Filtre par sévérité (Info, Warning, Critical)
- `?event_type=LoginFailed` - Filtre par type d'événement

**Réponse**:
```json
[
  {
    "Timestamp": "2023-04-20T15:40:22Z",
    "EventType": "LoginSuccess",
    "Username": "admin",
    "Source_IP": "192.168.1.100",
    "Target_Safe": null,
    "Target_Account": null,
    "Severity": "Info",
    "Description": "Successful login"
  },
  ...
]
```

### Tentatives de connexion échouées

```
GET /api/logins/failed
```

Récupère les tentatives de connexion échouées.

**Paramètres optionnels**:
- `?limit=10` - Nombre de tentatives à récupérer (défaut: 10)
- `?username=admin` - Filtre par nom d'utilisateur

**Réponse**:
```json
[
  {
    "Timestamp": "2023-04-20T15:20:12Z",
    "Username": "jane.smith",
    "Source_IP": "192.168.1.120",
    "Severity": "Warning",
    "Reason": "Invalid credentials"
  },
  ...
]
```

### Forcer la collecte de données

```
POST /api/collect
```

Force une collecte immédiate des données de santé depuis CyberArk.

**Réponse**:
```json
{
  "status": "success",
  "message": "Data collection started",
  "job_id": "12345678-1234-5678-1234-567812345678"
}
```

### Historique de collecte

```
GET /api/collect/history
```

Récupère l'historique des collectes de données.

**Paramètres optionnels**:
- `?limit=10` - Nombre d'entrées à récupérer (défaut: 10)

**Réponse**:
```json
[
  {
    "job_id": "12345678-1234-5678-1234-567812345678",
    "start_time": "2023-04-20T15:45:00Z",
    "end_time": "2023-04-20T15:45:30Z",
    "status": "success",
    "components_collected": 11,
    "events_collected": 10
  },
  ...
]
```

## Codes de statut HTTP

- **200 OK**: La requête a réussi
- **400 Bad Request**: Paramètres invalides
- **404 Not Found**: Ressource non trouvée
- **500 Internal Server Error**: Erreur interne du serveur

## Limites

- Taux limite: 60 requêtes par minute
- Taille maximale des réponses: 10 Mo

## Exemples d'utilisation

### cURL

```bash
# Récupérer toutes les données du tableau de bord
curl -X GET http://votre-serveur:8000/api/dashboard

# Récupérer uniquement les événements critiques
curl -X GET "http://votre-serveur:8000/api/events?severity=Critical"

# Forcer une collecte de données
curl -X POST http://votre-serveur:8000/api/collect
```

### Python

```python
import requests

# Récupérer toutes les données du tableau de bord
response = requests.get('http://votre-serveur:8000/api/dashboard')
data = response.json()

# Accéder aux composants
components = data['component_status']['Items']
for component in components:
    print(f"{component['Component Type']}: {component['Status']}")
```

### PowerShell

```powershell
# Récupérer toutes les données du tableau de bord
$response = Invoke-RestMethod -Uri "http://votre-serveur:8000/api/dashboard" -Method Get

# Accéder aux composants
$components = $response.component_status.Items
foreach ($component in $components) {
    Write-Host "$($component.'Component Type'): $($component.Status)"
}
```