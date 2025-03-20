# Documentation de l'API - CyberArk Health Dashboard

Cette documentation détaille les points d'accès (endpoints) de l'API REST fournie par le CyberArk Health Dashboard, leurs paramètres, les structures de données et les exemples d'utilisation.

## Informations générales

- **URL de base** : `http://<server-ip>:8000`
- **Format de réponse** : JSON
- **Authentification** : Non requise pour l'accès local, configuration possible pour l'authentification en production
- **Documentation interactive** : Disponible à `/docs` (Swagger UI)

## Points d'accès (Endpoints)

### Vérification de santé de l'API

Permet de vérifier si l'API est opérationnelle.

- **URL** : `/api/health`
- **Méthode** : `GET`
- **Paramètres** : Aucun

**Exemple de réponse** :

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2023-08-15T10:22:33Z"
}
```

### Récupération des données du tableau de bord

Fournit toutes les données nécessaires pour le tableau de bord.

- **URL** : `/api/dashboard`
- **Méthode** : `GET`
- **Paramètres de requête** :
  - `from_date` (optionnel) : Date de début au format YYYY-MM-DD
  - `to_date` (optionnel) : Date de fin au format YYYY-MM-DD

**Exemple de réponse** :

```json
{
  "component_status": [
    {
      "component_name": "CPM",
      "status": "Connected",
      "last_connection": "2023-08-15T09:32:18Z",
      "version": "12.1.0"
    },
    {
      "component_name": "PVWA",
      "status": "Connected",
      "last_connection": "2023-08-15T09:35:42Z",
      "version": "12.1.0"
    },
    {
      "component_name": "PSM",
      "status": "Connected",
      "last_connection": "2023-08-15T09:30:55Z",
      "version": "12.1.0"
    },
    {
      "component_name": "AAM Credential Provider",
      "status": "Disconnected",
      "last_connection": "2023-08-14T22:15:37Z",
      "version": "12.0.0"
    }
  ],
  "vault_status": {
    "total_safes": 45,
    "total_accounts": 2500,
    "license_usage": 85,
    "license_expiry": "2024-06-30"
  },
  "accounts_status": {
    "managed_accounts": 1250,
    "non_managed_accounts": 1250,
    "accounts_by_platform": [
      {
        "platform": "Windows Server Local",
        "count": 800
      },
      {
        "platform": "Unix SSH Keys",
        "count": 450
      },
      {
        "platform": "Oracle Database",
        "count": 350
      },
      {
        "platform": "AWS",
        "count": 250
      },
      {
        "platform": "Other",
        "count": 650
      }
    ]
  },
  "system_health": {
    "cpu_usage": 65,
    "memory_usage": 72,
    "disk_usage": 48,
    "system_alerts": [
      {
        "severity": "Warning",
        "description": "Memory usage above 70%",
        "timestamp": "2023-08-15T08:45:12Z"
      }
    ]
  },
  "recent_activities": [
    {
      "timestamp": "2023-08-15T09:58:23Z",
      "username": "admin",
      "action": "Password verified",
      "component": "CPM",
      "details": "Account: WindowsServerAdmin"
    },
    {
      "timestamp": "2023-08-15T09:42:17Z",
      "username": "john.doe",
      "action": "Session initiated",
      "component": "PSM",
      "details": "Target: DB-PROD-01"
    },
    {
      "timestamp": "2023-08-15T09:30:05Z",
      "username": "jane.smith",
      "action": "Password changed",
      "component": "CPM",
      "details": "Account: OracleDBAdmin"
    }
  ],
  "failed_logins": [
    {
      "timestamp": "2023-08-15T08:22:14Z",
      "username": "mike.jones",
      "reason": "Incorrect password",
      "source_ip": "192.168.1.45",
      "attempt_count": 2
    },
    {
      "timestamp": "2023-08-15T07:15:22Z",
      "username": "unknown",
      "reason": "User not found",
      "source_ip": "203.0.113.42",
      "attempt_count": 5
    }
  ]
}
```

### Déclenchement manuel de la collecte de données

Force une collecte immédiate des données depuis CyberArk.

- **URL** : `/api/collect`
- **Méthode** : `POST`
- **Paramètres** : Aucun

**Exemple de réponse** :

```json
{
  "status": "success",
  "message": "Data collection started",
  "job_id": "coll-2023-08-15-10-45-23"
}
```

### Récupération de l'état des composants

Fournit uniquement les informations sur l'état des composants CyberArk.

- **URL** : `/api/components`
- **Méthode** : `GET`
- **Paramètres** : Aucun

**Exemple de réponse** :

```json
{
  "components": [
    {
      "component_name": "CPM",
      "status": "Connected",
      "last_connection": "2023-08-15T09:32:18Z",
      "version": "12.1.0",
      "details": {
        "hostname": "cpm-server-01",
        "services_status": "Running",
        "scanning_enabled": true
      }
    },
    {
      "component_name": "PVWA",
      "status": "Connected",
      "last_connection": "2023-08-15T09:35:42Z",
      "version": "12.1.0",
      "details": {
        "hostname": "pvwa-server-01",
        "services_status": "Running",
        "active_sessions": 12
      }
    },
    {
      "component_name": "PSM",
      "status": "Connected",
      "last_connection": "2023-08-15T09:30:55Z",
      "version": "12.1.0",
      "details": {
        "hostname": "psm-server-01",
        "services_status": "Running",
        "active_sessions": 3
      }
    },
    {
      "component_name": "AAM Credential Provider",
      "status": "Disconnected",
      "last_connection": "2023-08-14T22:15:37Z",
      "version": "12.0.0",
      "details": {
        "hostname": "aam-server-01",
        "services_status": "Stopped",
        "error": "Connection timeout"
      }
    }
  ]
}
```

### Récupération des statistiques d'utilisation

Fournit des statistiques détaillées sur l'utilisation du système CyberArk.

- **URL** : `/api/stats`
- **Méthode** : `GET`
- **Paramètres de requête** :
  - `period` (optionnel) : Période d'analyse ("day", "week", "month", "year")
  - `from_date` (optionnel) : Date de début au format YYYY-MM-DD
  - `to_date` (optionnel) : Date de fin au format YYYY-MM-DD

**Exemple de réponse** :

```json
{
  "stats_period": "week",
  "from_date": "2023-08-08",
  "to_date": "2023-08-15",
  "usage_stats": {
    "total_sessions": 247,
    "sessions_by_component": {
      "PVWA": 122,
      "PSM": 125
    },
    "sessions_by_user": [
      {
        "username": "john.doe",
        "session_count": 45
      },
      {
        "username": "jane.smith",
        "session_count": 38
      },
      {
        "username": "admin",
        "session_count": 25
      }
    ],
    "password_activities": {
      "verifications": 320,
      "changes": 156,
      "reconciliations": 12
    }
  },
  "resource_usage": {
    "cpu_average": 58,
    "cpu_peak": 87,
    "memory_average": 65,
    "memory_peak": 92,
    "disk_usage_trend": [
      {
        "date": "2023-08-08",
        "usage_percent": 42
      },
      {
        "date": "2023-08-15",
        "usage_percent": 48
      }
    ]
  }
}
```

### Récupération des événements et alertes

Fournit la liste des événements et alertes récents.

- **URL** : `/api/events`
- **Méthode** : `GET`
- **Paramètres de requête** :
  - `limit` (optionnel) : Nombre maximum d'événements à retourner (défaut: 50)
  - `severity` (optionnel) : Filtrer par sévérité ("Info", "Warning", "Error", "Critical")
  - `component` (optionnel) : Filtrer par composant
  - `from_date` (optionnel) : Date de début au format YYYY-MM-DD
  - `to_date` (optionnel) : Date de fin au format YYYY-MM-DD

**Exemple de réponse** :

```json
{
  "events": [
    {
      "id": "evt-123456",
      "timestamp": "2023-08-15T09:58:23Z",
      "severity": "Info",
      "component": "CPM",
      "message": "Password verification completed successfully",
      "details": {
        "username": "admin",
        "account": "WindowsServerAdmin",
        "safe": "WindowsServers"
      }
    },
    {
      "id": "evt-123455",
      "timestamp": "2023-08-15T09:42:17Z",
      "severity": "Info",
      "component": "PSM",
      "message": "Session initiated",
      "details": {
        "username": "john.doe",
        "account": "OracleDBAdmin",
        "target": "DB-PROD-01",
        "session_id": "PSM-SESSION-12345"
      }
    },
    {
      "id": "evt-123454",
      "timestamp": "2023-08-15T08:45:12Z",
      "severity": "Warning",
      "component": "System",
      "message": "Memory usage above threshold",
      "details": {
        "current_usage": "72%",
        "threshold": "70%",
        "hostname": "vault-server-01"
      }
    }
  ],
  "total_count": 325,
  "page_info": {
    "returned_count": 3,
    "has_more": true
  }
}
```

## Structures de données

### ComponentStatus

| Champ | Type | Description |
|-------|------|-------------|
| component_name | string | Nom du composant CyberArk |
| status | string | État de connexion ("Connected", "Disconnected", "Warning") |
| last_connection | string (ISO 8601) | Horodatage de la dernière connexion réussie |
| version | string | Version du composant |
| details | object | Informations supplémentaires spécifiques au composant |

### VaultStatus

| Champ | Type | Description |
|-------|------|-------------|
| total_safes | integer | Nombre total de coffres-forts |
| total_accounts | integer | Nombre total de comptes |
| license_usage | integer | Pourcentage d'utilisation de la licence |
| license_expiry | string (YYYY-MM-DD) | Date d'expiration de la licence |

### AccountsStatus

| Champ | Type | Description |
|-------|------|-------------|
| managed_accounts | integer | Nombre de comptes gérés |
| non_managed_accounts | integer | Nombre de comptes non gérés |
| accounts_by_platform | array | Distribution des comptes par plateforme |

### SystemHealth

| Champ | Type | Description |
|-------|------|-------------|
| cpu_usage | integer | Pourcentage d'utilisation CPU |
| memory_usage | integer | Pourcentage d'utilisation mémoire |
| disk_usage | integer | Pourcentage d'utilisation disque |
| system_alerts | array | Alertes système actives |

### Activity

| Champ | Type | Description |
|-------|------|-------------|
| timestamp | string (ISO 8601) | Horodatage de l'activité |
| username | string | Utilisateur ayant effectué l'action |
| action | string | Description de l'action |
| component | string | Composant concerné |
| details | string | Détails supplémentaires |

### FailedLogin

| Champ | Type | Description |
|-------|------|-------------|
| timestamp | string (ISO 8601) | Horodatage de la tentative |
| username | string | Nom d'utilisateur utilisé |
| reason | string | Raison de l'échec |
| source_ip | string | Adresse IP source |
| attempt_count | integer | Nombre de tentatives |

## Exemples d'utilisation

### Curl

Vérifier l'état de l'API:

```bash
curl -X GET http://localhost:8000/api/health
```

Récupérer les données du tableau de bord pour une période spécifique:

```bash
curl -X GET "http://localhost:8000/api/dashboard?from_date=2023-08-01&to_date=2023-08-15"
```

Déclencher une collecte de données:

```bash
curl -X POST http://localhost:8000/api/collect
```

### Python

```python
import requests
import json
from datetime import datetime, timedelta

# Configuration
api_base_url = "http://localhost:8000"

# Vérifier l'état de l'API
health_response = requests.get(f"{api_base_url}/api/health")
print(f"API Health: {health_response.json()['status']}")

# Calculer la période sur 7 jours
today = datetime.now()
week_ago = today - timedelta(days=7)
from_date = week_ago.strftime("%Y-%m-%d")
to_date = today.strftime("%Y-%m-%d")

# Récupérer les données du tableau de bord
dashboard_response = requests.get(
    f"{api_base_url}/api/dashboard",
    params={"from_date": from_date, "to_date": to_date}
)

# Analyser les résultats
dashboard_data = dashboard_response.json()
print(f"Components connected: {sum(1 for c in dashboard_data['component_status'] if c['status'] == 'Connected')}")
print(f"Total accounts: {dashboard_data['vault_status']['total_accounts']}")
print(f"Managed accounts: {dashboard_data['accounts_status']['managed_accounts']}")
print(f"License usage: {dashboard_data['vault_status']['license_usage']}%")

# Déclencher une collecte de données
collect_response = requests.post(f"{api_base_url}/api/collect")
print(f"Data collection: {collect_response.json()['message']}")
```

### Power BI Web API

Pour la connexion dans Power BI, utilisez:

**URL de l'API Web**:
```
http://localhost:8000/api/dashboard
```

**Paramètres de requête** (optionnels):
- `from_date` (facultatif): Date de début pour filtrer les données
- `to_date` (facultatif): Date de fin pour filtrer les données

## Codes d'erreur

| Code | Message | Description |
|------|---------|-------------|
| 200 | OK | Requête réussie |
| 400 | Bad Request | Paramètres de requête invalides |
| 401 | Unauthorized | Authentification requise |
| 403 | Forbidden | Accès refusé |
| 404 | Not Found | Ressource non trouvée |
| 500 | Internal Server Error | Erreur interne du serveur |
| 503 | Service Unavailable | Service temporairement indisponible |

## Limites et considérations

- **Taux de requêtes**: Limité à 100 requêtes par minute
- **Taille des réponses**: Limitée à 10 MB par requête
- **Délai d'expiration**: 30 secondes par requête
- **Pagination**: Requise pour les grandes collections de données (événements, journaux)
- **Authentification**: Obligatoire pour les déploiements en production