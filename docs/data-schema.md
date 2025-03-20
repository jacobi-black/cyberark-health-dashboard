# Schéma de données

Ce document décrit le schéma de données utilisé par le tableau de bord de santé CyberArk, y compris les modèles de base de données et les structures de données de l'API.

## Modèles de base de données

Les modèles suivants sont utilisés pour stocker les données dans la base de données:

### ComponentStatus

Stocke l'état des composants CyberArk.

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant unique |
| timestamp | DateTime | Date et heure de la collecte |
| component_type | String | Type de composant (CPM, PSM, PVWA, AAM) |
| component_version | String | Version du composant |
| ip_address | String | Adresse IP du composant |
| component_user | String | Utilisateur du composant |
| connected | Boolean | État de connexion |
| last_connection | DateTime | Dernière connexion |
| os | String | Système d'exploitation |

### VaultStatus

Stocke l'état du coffre-fort CyberArk.

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant unique |
| timestamp | DateTime | Date et heure de la collecte |
| total_safes | Integer | Nombre total de coffres |
| active_safes | Integer | Nombre de coffres actifs |
| inactive_safes | Integer | Nombre de coffres inactifs |
| version | String | Version du coffre-fort |
| license_status | String | État de la licence |
| license_expiry | Date | Date d'expiration de la licence |

### AccountsStatus

Stocke l'état des comptes CyberArk.

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant unique |
| timestamp | DateTime | Date et heure de la collecte |
| total_accounts | Integer | Nombre total de comptes |
| managed_accounts | Integer | Nombre de comptes gérés |
| unmanaged_accounts | Integer | Nombre de comptes non gérés |
| pending_accounts | Integer | Nombre de comptes en attente |
| failed_accounts | Integer | Nombre de comptes échoués |

### SystemHealth

Stocke l'état de santé du système.

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant unique |
| timestamp | DateTime | Date et heure de la collecte |
| cpu_usage | Float | Utilisation du CPU (%) |
| cpu_cores | Integer | Nombre de cœurs CPU |
| memory_total | Integer | Mémoire totale (MB) |
| memory_used | Integer | Mémoire utilisée (MB) |
| memory_usage | Float | Utilisation de la mémoire (%) |
| disk_total | Integer | Espace disque total (MB) |
| disk_used | Integer | Espace disque utilisé (MB) |
| disk_usage | Float | Utilisation du disque (%) |
| network_latency | Float | Latence réseau (ms) |

### SecurityEvent

Stocke les événements de sécurité.

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant unique |
| timestamp | DateTime | Date et heure de l'événement |
| username | String | Nom d'utilisateur |
| event_type | String | Type d'événement |
| description | String | Description de l'événement |
| ip_address | String | Adresse IP |

### FailedLogin

Stocke les tentatives de connexion échouées.

| Champ | Type | Description |
|-------|------|-------------|
| id | Integer | Identifiant unique |
| timestamp | DateTime | Date et heure de la tentative |
| username | String | Nom d'utilisateur |
| ip_address | String | Adresse IP |
| reason | String | Raison de l'échec |

## Structure des données de l'API

L'API renvoie les données au format JSON avec la structure suivante:

### Dashboard Data

```json
{
  "component_status": {
    "Items": [
      {
        "Component Type": "CPM",
        "Total Amount": 3,
        "Connected": 3,
        "Disconnected": 0,
        "Status": "OK",
        "Components": [
          {
            "Component Type": "CPM",
            "Component Version": "12.6.0",
            "IP Address": "10.0.0.10",
            "Component User": "PasswordManager",
            "Connected": true,
            "Last Connection": "2023-04-20T15:30:22Z",
            "OS": "Windows"
          },
          // ...
        ]
      },
      // ...
    ]
  },
  "vault_status": {
    "Safes": {
      "Total": 120,
      "Active": 118,
      "Inactive": 2
    },
    "Version": "12.6.0",
    "License": "Valid",
    "License Expiry": "2024-12-31"
  },
  "accounts_status": {
    "value": {
      "Total": 1250,
      "Managed": 1050,
      "Unmanaged": 200,
      "Pending": 15,
      "Failed": 5
    }
  },
  "system_health": {
    "CPU": {
      "Usage": 45.2,
      "Cores": 8
    },
    "Memory": {
      "Total": 32768,
      "Used": 16384,
      "Usage": 50.0
    },
    "Disk": {
      "Total": 1024000,
      "Used": 512000,
      "Usage": 50.0
    },
    "NetworkLatency": 15.3
  },
  "recent_activities": [
    {
      "Timestamp": "2023-04-21T16:30:45Z",
      "Username": "admin",
      "EventType": "Login",
      "Description": "Successful login",
      "IP": "192.168.1.100"
    },
    // ...
  ],
  "failed_logins": [
    {
      "Timestamp": "2023-04-21T12:15:30Z",
      "Username": "john",
      "IP": "192.168.1.101",
      "Reason": "Invalid password"
    },
    // ...
  ]
}
```

## Relations entre les modèles

Les modèles sont relativement indépendants, mais sont liés par le champ `timestamp` qui permet de corréler les données collectées au même moment.

Par exemple, pour analyser l'état complet du système à un moment donné, on peut joindre les enregistrements des différents modèles ayant le même timestamp.

## Évolution du schéma

Le schéma de données est conçu pour être extensible. De nouveaux champs ou modèles peuvent être ajoutés pour prendre en charge des fonctionnalités supplémentaires.

Lorsque des modifications sont apportées au schéma, les migrations de base de données sont gérées automatiquement par SQLAlchemy.