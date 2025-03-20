# Référence de l'API

L'API REST du tableau de bord de santé CyberArk permet d'accéder programmatiquement aux données de santé et de performance de votre environnement CyberArk.

## Base URL

Toutes les URL référencées dans cette documentation ont pour base:

```
http://localhost:8000
```

Remplacez `localhost:8000` par l'hôte et le port où votre API est déployée.

## Authentification

L'API ne nécessite pas d'authentification pour le moment. Dans un environnement de production, il est recommandé de mettre en place une authentification.

## Format des réponses

Toutes les réponses sont au format JSON. Les codes de statut HTTP standards sont utilisés:

- `200 OK` - La requête a réussi
- `404 Not Found` - La ressource demandée n'existe pas
- `500 Internal Server Error` - Une erreur s'est produite côté serveur

## Endpoints

### Vérifier l'état de santé de l'API

```
GET /api/health
```

**Réponse**:

```json
{
  "status": "ok",
  "timestamp": "2023-04-21T14:30:45.123456"
}
```

### Récupérer les données du tableau de bord

```
GET /api/dashboard
```

**Paramètres de requête**:

- `refresh` (booléen, facultatif): Force la récupération de nouvelles données

**Réponse**:

La réponse contient toutes les données du tableau de bord, y compris l'état des composants, l'état du coffre-fort, l'état des comptes, et plus encore.

### Récupérer l'état des composants

```
GET /api/components
```

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
}
```

### Récupérer l'état du coffre-fort

```
GET /api/vault
```

**Réponse**:

```json
{
  "Safes": {
    "Total": 120,
    "Active": 118,
    "Inactive": 2
  },
  "Version": "12.6.0",
  "License": "Valid",
  "License Expiry": "2024-12-31"
}
```

### Récupérer l'état des comptes

```
GET /api/accounts
```

**Réponse**:

```json
{
  "value": {
    "Total": 1250,
    "Managed": 1050,
    "Unmanaged": 200,
    "Pending": 15,
    "Failed": 5
  }
}
```

### Récupérer l'état de santé du système

```
GET /api/system
```

**Réponse**:

```json
{
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
}
```

### Récupérer les événements de sécurité récents

```
GET /api/events
```

**Paramètres de requête**:

- `limit` (entier, facultatif): Nombre d'événements à récupérer (par défaut: 10, max: 100)

**Réponse**:

```json
{
  "events": [
    {
      "Timestamp": "2023-04-21T16:30:45Z",
      "Username": "admin",
      "EventType": "Login",
      "Description": "Successful login",
      "IP": "192.168.1.100"
    },
    // ...
  ]
}
```

### Récupérer les tentatives de connexion échouées

```
GET /api/logins/failed
```

**Paramètres de requête**:

- `limit` (entier, facultatif): Nombre de tentatives à récupérer (par défaut: 10, max: 100)

**Réponse**:

```json
{
  "logins": [
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

### Forcer la collecte de données

```
POST /api/collect
```

**Réponse**:

```json
{
  "status": "collection started",
  "timestamp": "2023-04-21T16:35:00.123456"
}
```

## Documentation Swagger

Une documentation interactive de l'API est disponible à l'adresse:

```
http://localhost:8000/docs
```

Cette interface vous permet de tester les endpoints directement depuis votre navigateur.