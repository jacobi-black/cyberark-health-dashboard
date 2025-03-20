from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from app.config import DB_CONFIG

# Créer une connexion à la base de données
if DB_CONFIG["connection_string"]:
    engine = create_engine(DB_CONFIG["connection_string"])
else:
    # Fallback to SQLite for demo if no connection string is provided
    engine = create_engine("sqlite:///cyberark_health.db")

# Créer une session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer une base déclarative
Base = declarative_base()

# Modèles SQLAlchemy pour la base de données
class ComponentStatus(Base):
    __tablename__ = "component_status"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now)
    component_type = Column(String(100))
    total_amount = Column(Integer)
    connected = Column(Integer)
    disconnected = Column(Integer)
    status = Column(String(50))  # OK, Warning, Error

    components = relationship("Component", back_populates="status")

class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    component_status_id = Column(Integer, ForeignKey("component_status.id"))
    timestamp = Column(DateTime, default=datetime.now)
    component_type = Column(String(100))
    component_version = Column(String(100))
    ip_address = Column(String(100))
    component_user = Column(String(255))
    connected = Column(Boolean)
    last_connection = Column(DateTime, nullable=True)
    os = Column(String(50))

    status = relationship("ComponentStatus", back_populates="components")

class VaultStatus(Base):
    __tablename__ = "vault_status"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now)
    total_safes = Column(Integer)
    total_accounts = Column(Integer)
    version = Column(String(100))
    license_status = Column(String(50))
    license_expiration = Column(DateTime, nullable=True)

class AccountsStatus(Base):
    __tablename__ = "accounts_status"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now)
    total_accounts = Column(Integer)
    managed_accounts = Column(Integer)
    non_managed_accounts = Column(Integer)
    pending_accounts = Column(Integer)
    failed_accounts = Column(Integer)

class SystemHealth(Base):
    __tablename__ = "system_health"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now)
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    disk_usage = Column(Float)
    network_latency = Column(Float)
    last_backup = Column(DateTime, nullable=True)

class SecurityEvent(Base):
    __tablename__ = "security_events"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now)
    event_type = Column(String(100))
    username = Column(String(255))
    source_ip = Column(String(100))
    target_safe = Column(String(255), nullable=True)
    target_account = Column(String(255), nullable=True)
    severity = Column(String(50))
    description = Column(Text)
    raw_data = Column(Text)

# Modèles Pydantic pour l'API
class ComponentStatusBase(BaseModel):
    component_type: str
    total_amount: int
    connected: int
    disconnected: int
    status: str

class ComponentBase(BaseModel):
    component_type: str
    component_version: str
    ip_address: str
    component_user: str
    connected: bool
    last_connection: Optional[datetime] = None
    os: str

class VaultStatusBase(BaseModel):
    total_safes: int
    total_accounts: int
    version: str
    license_status: str
    license_expiration: Optional[datetime] = None

class AccountsStatusBase(BaseModel):
    total_accounts: int
    managed_accounts: int
    non_managed_accounts: int
    pending_accounts: int
    failed_accounts: int

class SystemHealthBase(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_latency: float
    last_backup: Optional[datetime] = None

class SecurityEventBase(BaseModel):
    event_type: str
    username: str
    source_ip: str
    target_safe: Optional[str] = None
    target_account: Optional[str] = None
    severity: str
    description: str
    raw_data: Optional[str] = None

class DashboardData(BaseModel):
    component_status: dict
    vault_status: dict
    accounts_status: dict
    system_health: dict
    recent_activities: List[dict] = []
    failed_logins: List[dict] = []
    last_update: str

# Créer les tables dans la base de données
def create_tables():
    Base.metadata.create_all(bind=engine)