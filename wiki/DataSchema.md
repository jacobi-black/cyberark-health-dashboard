# Schéma de Données - CyberArk Health Dashboard

Ce document décrit en détail les structures de données utilisées dans le CyberArk Health Dashboard, incluant les modèles de base de données, les formats d'API et les relations entre les entités.

## Vue d'ensemble du schéma

Le CyberArk Health Dashboard utilise une architecture de données structurée autour de plusieurs entités principales qui reflètent les différents aspects d'un environnement CyberArk PAM. Ces entités sont stockées dans une base de données relationnelle et exposées via l'API REST.

### Entités principales

1. **Components** - Composants CyberArk (CPM, PVWA, PSM, etc.)
2. **ComponentStatus** - État de connexion des composants au fil du temps
3. **Accounts** - Informations sur les comptes gérés et non gérés
4. **SystemMetrics** - Métriques de santé système (CPU, mémoire, disque)
5. **Activities** - Événements et activités du système
6. **FailedLogins** - Tentatives de connexion échouées

### Structure de la base de données

![Schéma de base de données](../assets/db_schema.png)

## Schéma détaillé des tables

### Table Components

Stocke les informations sur les composants CyberArk disponibles.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| name | VARCHAR(100) | NOT NULL | Nom du composant |
| type | VARCHAR(50) | NOT NULL | Type de composant (CPM, PVWA, PSM, etc.) |
| hostname | VARCHAR(255) | | Nom d'hôte ou IP du serveur |
| version | VARCHAR(50) | | Version du composant |
| details | TEXT | | Détails supplémentaires au format JSON |
| created_at | TIMESTAMP | NOT NULL | Date de création de l'enregistrement |
| updated_at | TIMESTAMP | NOT NULL | Date de dernière mise à jour |

### Table ComponentStatus

Stocke l'historique des états de connexion pour chaque composant.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| component_id | INTEGER | FOREIGN KEY | Référence à Components.id |
| status | VARCHAR(50) | NOT NULL | État (Connected, Disconnected, Warning) |
| last_connection | TIMESTAMP | | Horodatage de la dernière connexion |
| details | TEXT | | Détails ou message d'erreur au format JSON |
| created_at | TIMESTAMP | NOT NULL | Date de création de l'enregistrement |

### Table Accounts

Stocke les informations sur les comptes CyberArk.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| name | VARCHAR(255) | NOT NULL | Nom du compte |
| platform | VARCHAR(100) | | Plateforme associée |
| safe | VARCHAR(100) | | Coffre-fort contenant le compte |
| is_managed | BOOLEAN | NOT NULL | Si le compte est géré par CyberArk |
| last_password_change | TIMESTAMP | | Date du dernier changement de mot de passe |
| last_verification | TIMESTAMP | | Date de la dernière vérification |
| details | TEXT | | Détails supplémentaires au format JSON |
| created_at | TIMESTAMP | NOT NULL | Date de création de l'enregistrement |
| updated_at | TIMESTAMP | NOT NULL | Date de dernière mise à jour |

### Table VaultStatus

Stocke l'état global du coffre-fort CyberArk.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| total_safes | INTEGER | | Nombre total de coffres-forts |
| total_accounts | INTEGER | | Nombre total de comptes |
| license_usage | INTEGER | | Pourcentage d'utilisation de la licence |
| license_expiry | DATE | | Date d'expiration de la licence |
| snapshot_time | TIMESTAMP | NOT NULL | Horodatage de la prise d'instantané |
| details | TEXT | | Détails supplémentaires au format JSON |

### Table SystemMetrics

Stocke les métriques de performance système.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| component_id | INTEGER | FOREIGN KEY | Référence à Components.id (NULL pour métriques globales) |
| cpu_usage | FLOAT | | Pourcentage d'utilisation CPU |
| memory_usage | FLOAT | | Pourcentage d'utilisation mémoire |
| disk_usage | FLOAT | | Pourcentage d'utilisation disque |
| collection_time | TIMESTAMP | NOT NULL | Horodatage de la collecte |
| details | TEXT | | Détails supplémentaires au format JSON |

### Table Activities

Stocke les événements et activités du système.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| timestamp | TIMESTAMP | NOT NULL | Horodatage de l'activité |
| username | VARCHAR(255) | | Utilisateur ayant effectué l'action |
| action | VARCHAR(255) | NOT NULL | Description de l'action |
| component_id | INTEGER | FOREIGN KEY | Référence à Components.id |
| severity | VARCHAR(50) | | Niveau de sévérité (Info, Warning, Error, Critical) |
| details | TEXT | | Détails supplémentaires au format JSON |

### Table FailedLogins

Stocke les tentatives de connexion échouées.

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Identifiant unique |
| timestamp | TIMESTAMP | NOT NULL | Horodatage de la tentative |
| username | VARCHAR(255) | | Nom d'utilisateur utilisé |
| source_ip | VARCHAR(50) | | Adresse IP source |
| reason | VARCHAR(255) | | Raison de l'échec |
| attempt_count | INTEGER | | Nombre de tentatives |
| details | TEXT | | Détails supplémentaires au format JSON |

## Modèles de Données Python (SQLAlchemy)

Voici les modèles SQLAlchemy qui correspondent aux tables définies ci-dessus:

```python
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Component(Base):
    __tablename__ = 'components'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    hostname = Column(String(255))
    version = Column(String(50))
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    statuses = relationship("ComponentStatus", back_populates="component")
    metrics = relationship("SystemMetric", back_populates="component")
    activities = relationship("Activity", back_populates="component")

class ComponentStatus(Base):
    __tablename__ = 'component_status'
    
    id = Column(Integer, primary_key=True)
    component_id = Column(Integer, ForeignKey('components.id'))
    status = Column(String(50), nullable=False)
    last_connection = Column(DateTime)
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    
    component = relationship("Component", back_populates="statuses")

class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    platform = Column(String(100))
    safe = Column(String(100))
    is_managed = Column(Boolean, nullable=False)
    last_password_change = Column(DateTime)
    last_verification = Column(DateTime)
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

class VaultStatus(Base):
    __tablename__ = 'vault_status'
    
    id = Column(Integer, primary_key=True)
    total_safes = Column(Integer)
    total_accounts = Column(Integer)
    license_usage = Column(Integer)
    license_expiry = Column(Date)
    snapshot_time = Column(DateTime, nullable=False)
    details = Column(Text)

class SystemMetric(Base):
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True)
    component_id = Column(Integer, ForeignKey('components.id'))
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    disk_usage = Column(Float)
    collection_time = Column(DateTime, nullable=False)
    details = Column(Text)
    
    component = relationship("Component", back_populates="metrics")

class Activity(Base):
    __tablename__ = 'activities'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    username = Column(String(255))
    action = Column(String(255), nullable=False)
    component_id = Column(Integer, ForeignKey('components.id'))
    severity = Column(String(50))
    details = Column(Text)
    
    component = relationship("Component", back_populates="activities")

class FailedLogin(Base):
    __tablename__ = 'failed_logins'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    username = Column(String(255))
    source_ip = Column(String(50))
    reason = Column(String(255))
    attempt_count = Column(Integer)
    details = Column(Text)
```

## Formats JSON pour l'API

### Format ComponentStatus

```json
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
}
```

### Format VaultStatus

```json
{
  "total_safes": 45,
  "total_accounts": 2500,
  "license_usage": 85,
  "license_expiry": "2024-06-30"
}
```

### Format AccountsStatus

```json
{
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
}
```

### Format SystemHealth

```json
{
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
}
```

### Format Activity

```json
{
  "timestamp": "2023-08-15T09:58:23Z",
  "username": "admin",
  "action": "Password verified",
  "component": "CPM",
  "details": "Account: WindowsServerAdmin"
}
```

### Format FailedLogin

```json
{
  "timestamp": "2023-08-15T08:22:14Z",
  "username": "mike.jones",
  "reason": "Incorrect password",
  "source_ip": "192.168.1.45",
  "attempt_count": 2
}
```

## Schéma Pydantic pour Validation d'API

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date

class ComponentStatusDetail(BaseModel):
    hostname: Optional[str] = None
    services_status: Optional[str] = None
    scanning_enabled: Optional[bool] = None
    active_sessions: Optional[int] = None
    error: Optional[str] = None

class ComponentStatusModel(BaseModel):
    component_name: str
    status: str
    last_connection: datetime
    version: Optional[str] = None
    details: Optional[ComponentStatusDetail] = None

class PlatformCount(BaseModel):
    platform: str
    count: int

class AccountsStatusModel(BaseModel):
    managed_accounts: int
    non_managed_accounts: int
    accounts_by_platform: List[PlatformCount]

class SystemAlert(BaseModel):
    severity: str
    description: str
    timestamp: datetime

class SystemHealthModel(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    system_alerts: List[SystemAlert] = []

class ActivityModel(BaseModel):
    timestamp: datetime
    username: Optional[str] = None
    action: str
    component: str
    details: Optional[str] = None

class FailedLoginModel(BaseModel):
    timestamp: datetime
    username: str
    reason: str
    source_ip: str
    attempt_count: int = 1

class VaultStatusModel(BaseModel):
    total_safes: int
    total_accounts: int
    license_usage: int
    license_expiry: date

class DashboardModel(BaseModel):
    component_status: List[ComponentStatusModel]
    vault_status: VaultStatusModel
    accounts_status: AccountsStatusModel
    system_health: SystemHealthModel
    recent_activities: List[ActivityModel]
    failed_logins: List[FailedLoginModel]
```

## Intégration avec Power BI

### Tables Power BI

Power BI peut se connecter à l'API REST et créer les tables suivantes:

1. **ComponentStatus**
   - ComponentName (texte)
   - Status (texte)
   - LastConnection (datetime)
   - Version (texte)

2. **VaultStatus**
   - TotalSafes (entier)
   - TotalAccounts (entier)
   - LicenseUsage (entier)
   - LicenseExpiry (date)

3. **AccountsStatus**
   - ManagedAccounts (entier)
   - NonManagedAccounts (entier)

4. **AccountsByPlatform**
   - Platform (texte)
   - Count (entier)

5. **SystemHealth**
   - CPUUsage (décimal)
   - MemoryUsage (décimal)
   - DiskUsage (décimal)

6. **SystemAlerts**
   - Severity (texte)
   - Description (texte)
   - Timestamp (datetime)

7. **Activities**
   - Timestamp (datetime)
   - Username (texte)
   - Action (texte)
   - Component (texte)
   - Details (texte)

8. **FailedLogins**
   - Timestamp (datetime)
   - Username (texte)
   - Reason (texte)
   - SourceIP (texte)
   - AttemptCount (entier)

### Relations Power BI

Les relations suivantes peuvent être établies dans le modèle Power BI:

1. **Activities** à **ComponentStatus** (via ComponentName)
2. **SystemAlerts** à **SystemHealth** (relation un-à-plusieurs)
3. **AccountsByPlatform** à **AccountsStatus** (relation un-à-plusieurs)

### Mesures DAX

Exemples de mesures DAX à créer dans Power BI:

```dax
PctComponentsConnected = 
DIVIDE(
    COUNTROWS(FILTER('ComponentStatus', 'ComponentStatus'[Status] = "Connected")),
    COUNTROWS('ComponentStatus')
) * 100

PctManagedAccounts = 
DIVIDE(
    'AccountsStatus'[ManagedAccounts],
    'AccountsStatus'[ManagedAccounts] + 'AccountsStatus'[NonManagedAccounts]
) * 100

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

TotalFailedLogins = 
SUMX('FailedLogins', 'FailedLogins'[AttemptCount])
```

## Évolutions futures du schéma

Les évolutions suivantes du schéma de données sont envisagées pour les futures versions:

1. **Suivi des applications** - Ajout de tables pour suivre les applications utilisant l'API d'Application Access Manager
2. **Métriques détaillées** - Collecte de métriques de performance plus détaillées par composant
3. **Audit avancé** - Extension du modèle d'activité pour un suivi d'audit plus détaillé
4. **Analyse prédictive** - Structures pour stocker les prédictions basées sur l'analyse des tendances historiques
5. **Conformité** - Tables spécifiques pour le suivi des indicateurs de conformité réglementaire