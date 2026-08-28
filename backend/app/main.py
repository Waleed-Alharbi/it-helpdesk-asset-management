from collections import Counter
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .database import Base, engine, get_db, SessionLocal
from .models import Asset, Ticket, User
from .schemas import AssetCreate, AssetOut, AssetUpdate, TicketCreate, TicketOut, TicketUpdate, UserCreate, UserOut, UserUpdate
from .seed import seed_database

app = FastAPI(title="IT Helpdesk & Asset Management API", version="1.0.0", description="Portfolio MVP API for helpdesk tickets, assets, and users.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def start_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

def get_or_404(db, model, item_id, label):
    item = db.get(model, item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"{label} {item_id} was not found")
    return item

def save(db, item):
    try:
        db.add(item); db.commit(); db.refresh(item)
        return item
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="A record with that unique value already exists")

@app.get("/api/health")
def health(): return {"status": "ok"}

@app.get("/api/tickets", response_model=list[TicketOut])
def list_tickets(status: str | None = None, priority: str | None = None, department: str | None = None, search: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Ticket)
    if status: query = query.filter(Ticket.status == status)
    if priority: query = query.filter(Ticket.priority == priority)
    if department: query = query.filter(Ticket.department == department)
    if search:
        term = f"%{search}%"
        query = query.filter(Ticket.title.ilike(term) | Ticket.requester.ilike(term))
    return query.order_by(Ticket.created_at.desc()).all()

@app.get("/api/tickets/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)): return get_or_404(db, Ticket, ticket_id, "Ticket")
@app.post("/api/tickets", response_model=TicketOut, status_code=201)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    from datetime import datetime
    return save(db, Ticket(**payload.model_dump(), created_at=datetime.now()))
@app.put("/api/tickets/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)):
    item = get_or_404(db, Ticket, ticket_id, "Ticket")
    for key, value in payload.model_dump(exclude_unset=True).items(): setattr(item, key, value)
    return save(db, item)
@app.delete("/api/tickets/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db.delete(get_or_404(db, Ticket, ticket_id, "Ticket")); db.commit()

@app.get("/api/assets", response_model=list[AssetOut])
def list_assets(status: str | None = None, device_type: str | None = None, search: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Asset)
    if status: query = query.filter(Asset.status == status)
    if device_type: query = query.filter(Asset.device_type == device_type)
    if search:
        term = f"%{search}%"
        query = query.filter(Asset.device_name.ilike(term) | Asset.serial_number.ilike(term) | Asset.assigned_user.ilike(term))
    return query.order_by(Asset.id.desc()).all()
@app.get("/api/assets/{asset_id}", response_model=AssetOut)
def get_asset(asset_id: int, db: Session = Depends(get_db)): return get_or_404(db, Asset, asset_id, "Asset")
@app.post("/api/assets", response_model=AssetOut, status_code=201)
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)): return save(db, Asset(**payload.model_dump()))
@app.put("/api/assets/{asset_id}", response_model=AssetOut)
def update_asset(asset_id: int, payload: AssetUpdate, db: Session = Depends(get_db)):
    item = get_or_404(db, Asset, asset_id, "Asset")
    for key, value in payload.model_dump(exclude_unset=True).items(): setattr(item, key, value)
    return save(db, item)
@app.delete("/api/assets/{asset_id}", status_code=204)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    db.delete(get_or_404(db, Asset, asset_id, "Asset")); db.commit()

@app.get("/api/users", response_model=list[UserOut])
def list_users(search: str | None = None, db: Session = Depends(get_db)):
    query = db.query(User)
    if search:
        term = f"%{search}%"; query = query.filter(User.name.ilike(term) | User.email.ilike(term) | User.department.ilike(term))
    return query.order_by(User.name).all()
@app.get("/api/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)): return get_or_404(db, User, user_id, "User")
@app.post("/api/users", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)): return save(db, User(**payload.model_dump()))
@app.put("/api/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    item = get_or_404(db, User, user_id, "User")
    for key, value in payload.model_dump(exclude_unset=True).items(): setattr(item, key, value)
    return save(db, item)
@app.delete("/api/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db.delete(get_or_404(db, User, user_id, "User")); db.commit()

def breakdown(items, field):
    return [{"name": name, "value": value} for name, value in Counter(getattr(item, field) for item in items).items()]

@app.get("/api/dashboard/stats")
def dashboard_stats(db: Session = Depends(get_db)):
    tickets, assets, users = db.query(Ticket).all(), db.query(Asset).all(), db.query(User).all()
    return {"stats": {"total_tickets": len(tickets), "open_tickets": sum(t.status == "Open" for t in tickets), "in_progress": sum(t.status == "In Progress" for t in tickets), "resolved": sum(t.status in ["Resolved", "Closed"] for t in tickets), "critical": sum(t.priority == "Critical" for t in tickets), "total_assets": len(assets), "active_users": sum(u.status == "Active" for u in users)}, "tickets_by_status": breakdown(tickets, "status"), "tickets_by_priority": breakdown(tickets, "priority"), "tickets_by_department": breakdown(tickets, "department"), "recent_tickets": sorted(tickets, key=lambda t: t.created_at, reverse=True)[:6]}

@app.get("/api/reports/summary")
def reports_summary(db: Session = Depends(get_db)):
    tickets, assets = db.query(Ticket).all(), db.query(Asset).all()
    resolved = sum(t.status in ["Resolved", "Closed"] for t in tickets)
    months = [{"name": "Mar", "value": 7}, {"name": "Apr", "value": 11}, {"name": "May", "value": 9}, {"name": "Jun", "value": 14}, {"name": "Jul", "value": 12}, {"name": "Aug", "value": len(tickets)}]
    return {"resolution_rate": round((resolved / len(tickets)) * 100) if tickets else 0, "open_vs_resolved": [{"name": "Open", "value": sum(t.status in ["Open", "In Progress"] for t in tickets)}, {"name": "Resolved", "value": resolved}], "tickets_by_department": breakdown(tickets, "department"), "tickets_by_priority": breakdown(tickets, "priority"), "asset_status": breakdown(assets, "status"), "monthly_trend": months}

