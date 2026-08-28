from sqlalchemy import Column, DateTime, Integer, String, Text
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    department = Column(String(80), nullable=False)
    role = Column(String(50), nullable=False, default="Employee")
    status = Column(String(30), nullable=False, default="Active")

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    requester = Column(String(100), nullable=False)
    department = Column(String(80), nullable=False)
    category = Column(String(80), nullable=False)
    priority = Column(String(30), nullable=False, default="Medium")
    status = Column(String(30), nullable=False, default="Open")
    assigned_technician = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False)
    sla = Column(String(40), nullable=False, default="Within SLA")

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    device_type = Column(String(80), nullable=False)
    device_name = Column(String(150), nullable=False)
    serial_number = Column(String(100), unique=True, nullable=False)
    assigned_user = Column(String(100), nullable=True)
    department = Column(String(80), nullable=False)
    status = Column(String(30), nullable=False, default="Active")
    purchase_date = Column(String(20), nullable=False)
