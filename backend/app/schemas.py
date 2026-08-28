from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class UserBase(BaseModel):
    name: str
    email: str
    department: str
    role: str = "Employee"
    status: str = "Active"
class UserCreate(UserBase): pass
class UserUpdate(BaseModel):
    name: Optional[str] = None; email: Optional[str] = None; department: Optional[str] = None
    role: Optional[str] = None; status: Optional[str] = None
class UserOut(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TicketBase(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=3)
    requester: str
    department: str
    category: str
    priority: str = "Medium"
    status: str = "Open"
    assigned_technician: Optional[str] = None
    sla: str = "Within SLA"
class TicketCreate(TicketBase): pass
class TicketUpdate(BaseModel):
    title: Optional[str] = None; description: Optional[str] = None; requester: Optional[str] = None
    department: Optional[str] = None; category: Optional[str] = None; priority: Optional[str] = None
    status: Optional[str] = None; assigned_technician: Optional[str] = None; sla: Optional[str] = None
class TicketOut(TicketBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AssetBase(BaseModel):
    device_type: str
    device_name: str
    serial_number: str
    assigned_user: Optional[str] = None
    department: str
    status: str = "Active"
    purchase_date: str
class AssetCreate(AssetBase): pass
class AssetUpdate(BaseModel):
    device_type: Optional[str] = None; device_name: Optional[str] = None; serial_number: Optional[str] = None
    assigned_user: Optional[str] = None; department: Optional[str] = None; status: Optional[str] = None; purchase_date: Optional[str] = None
class AssetOut(AssetBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
