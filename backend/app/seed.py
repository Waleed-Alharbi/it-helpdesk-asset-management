from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models import User, Ticket, Asset

USERS = [
    ("Aisha Rahman", "aisha.rahman@northstar.io", "Finance", "Manager"), ("Omar Hassan", "omar.hassan@northstar.io", "Engineering", "Employee"),
    ("Lina Khalid", "lina.khalid@northstar.io", "Human Resources", "Employee"), ("David Miller", "david.miller@northstar.io", "Sales", "Employee"),
    ("Noor Al-Sayed", "noor.alsayed@northstar.io", "Operations", "Manager"), ("Maya Patel", "maya.patel@northstar.io", "Marketing", "Employee"),
    ("James Chen", "james.chen@northstar.io", "Engineering", "Employee"), ("Hana Ali", "hana.ali@northstar.io", "Finance", "Employee"),
    ("Robert Kim", "robert.kim@northstar.io", "Operations", "Employee"), ("Sara Wilson", "sara.wilson@northstar.io", "Sales", "Employee"),
    ("Waleed Alharbi", "waleed.alharbi@northstar.io", "IT", "IT Administrator"), ("Priya Nair", "priya.nair@northstar.io", "IT", "Technician"),
    ("Daniel Brooks", "daniel.brooks@northstar.io", "IT", "Technician"), ("Yasmin Farouk", "yasmin.farouk@northstar.io", "IT", "Technician"),
    ("Marcus Lee", "marcus.lee@northstar.io", "IT", "Technician")]

TICKETS = [
    ("Unable to connect to corporate Wi-Fi", "Laptop repeatedly disconnects from the staff wireless network.", "Omar Hassan", "Engineering", "Network", "High", "In Progress", "Priya Nair", "Within SLA"),
    ("Microsoft Outlook authentication issue", "Outlook requests credentials each time it opens.", "Aisha Rahman", "Finance", "Software", "High", "Open", "Daniel Brooks", "Due in 2h"),
    ("Laptop performance degradation", "Device is slow during normal accounting work.", "Hana Ali", "Finance", "Hardware", "Medium", "Open", "Yasmin Farouk", "Within SLA"),
    ("VPN connection failure", "Cannot establish VPN connection while travelling.", "David Miller", "Sales", "Network", "Critical", "In Progress", "Priya Nair", "Due in 45m"),
    ("Printer not responding", "Third floor finance printer shows offline.", "Aisha Rahman", "Finance", "Hardware", "Medium", "Resolved", "Marcus Lee", "Met SLA"),
    ("User account access request", "New starter needs access to the CRM workspace.", "Noor Al-Sayed", "Operations", "Access", "Low", "Resolved", "Daniel Brooks", "Met SLA"),
    ("Teams meeting audio failure", "No audio available in scheduled external meetings.", "Maya Patel", "Marketing", "Software", "Medium", "Open", "Yasmin Farouk", "Within SLA"),
    ("Shared drive permission update", "Grant read access to the Q3 planning folder.", "Lina Khalid", "Human Resources", "Access", "Low", "Resolved", "Daniel Brooks", "Met SLA"),
    ("Monitor flickering intermittently", "External monitor flickers after wake from sleep.", "James Chen", "Engineering", "Hardware", "Medium", "In Progress", "Marcus Lee", "Within SLA"),
    ("Suspicious phishing email reported", "User reported an email imitating the payroll team.", "Sara Wilson", "Sales", "Security", "High", "Resolved", "Waleed Alharbi", "Met SLA"),
    ("Mobile device enrollment", "New company mobile needs device management enrollment.", "Robert Kim", "Operations", "Mobile", "Low", "Open", "Yasmin Farouk", "Within SLA"),
    ("Password reset request", "Unable to reset password through self-service portal.", "Lina Khalid", "Human Resources", "Access", "Low", "Resolved", "Daniel Brooks", "Met SLA"),
    ("Network switch port unavailable", "Desk port stopped working after office move.", "Omar Hassan", "Engineering", "Network", "High", "In Progress", "Priya Nair", "Within SLA"),
    ("Adobe license activation", "Creative Cloud activation fails on replacement laptop.", "Maya Patel", "Marketing", "Software", "Medium", "Resolved", "Marcus Lee", "Met SLA"),
    ("Laptop battery replacement", "Battery health warning below company threshold.", "David Miller", "Sales", "Hardware", "Low", "Closed", "Yasmin Farouk", "Met SLA"),
    ("MFA prompt not received", "Authenticator push notification is not arriving.", "Hana Ali", "Finance", "Security", "High", "Open", "Waleed Alharbi", "Due in 4h"),
    ("New employee workstation setup", "Prepare a standard laptop and account for the new hire.", "Noor Al-Sayed", "Operations", "Onboarding", "Medium", "Resolved", "Marcus Lee", "Met SLA"),
    ("Conference room display unavailable", "Meeting room screen has no signal from dock.", "Sara Wilson", "Sales", "Hardware", "Medium", "Open", "Priya Nair", "Within SLA"),
    ("ERP access role correction", "Access is restricted after finance team transfer.", "Aisha Rahman", "Finance", "Access", "High", "In Progress", "Daniel Brooks", "Within SLA"),
    ("Endpoint protection alert", "Managed endpoint flagged a potentially unwanted application.", "James Chen", "Engineering", "Security", "Critical", "Open", "Waleed Alharbi", "Due in 1h")]

ASSETS = [
    ("Laptop", "Dell Latitude 5440", "DL-5440-1001", "Omar Hassan", "Engineering", "Active", "2024-01-15"), ("Laptop", "HP ProBook 450", "HP-450-2002", "Aisha Rahman", "Finance", "Active", "2023-10-02"),
    ("Laptop", "Lenovo ThinkPad T14", "LT-T14-3003", "James Chen", "Engineering", "Active", "2024-03-21"), ("Desktop", "Dell OptiPlex 7010", "DO-7010-4004", "Hana Ali", "Finance", "Active", "2022-08-12"),
    ("Network", "Cisco Catalyst 9200 Switch", "CS-9200-5005", None, "IT", "Active", "2023-06-18"), ("Network", "Cisco Meraki MR46 Access Point", "CM-MR46-6006", None, "IT", "Active", "2024-02-06"),
    ("Laptop", "Dell Latitude 5440", "DL-5440-1007", "David Miller", "Sales", "Active", "2024-01-15"), ("Laptop", "HP ProBook 450", "HP-450-2008", "Lina Khalid", "Human Resources", "Active", "2023-10-02"),
    ("Laptop", "Lenovo ThinkPad T14", "LT-T14-3009", "Maya Patel", "Marketing", "Maintenance", "2022-11-30"), ("Desktop", "Dell OptiPlex 7010", "DO-7010-4010", "Robert Kim", "Operations", "Active", "2022-08-12"),
    ("Mobile", "iPhone 15", "IP-15-7011", "Sara Wilson", "Sales", "Active", "2024-04-10"), ("Peripheral", "Dell P2422H Monitor", "DM-2422-8012", "Noor Al-Sayed", "Operations", "Active", "2023-09-14"),
    ("Laptop", "Dell Latitude 5420", "DL-5420-1013", None, "IT", "In Stock", "2021-07-09"), ("Network", "Fortinet FortiGate 60F", "FG-60F-9014", None, "IT", "Active", "2023-01-24"),
    ("Printer", "HP LaserJet Pro M404", "HP-M404-1015", "Finance Team", "Finance", "Retired", "2020-05-06")]

def update_demo_admin(db: Session):
    legacy_admin = db.query(User).filter(User.email == "alex.morgan@northstar.io").first()
    if legacy_admin:
        legacy_name = legacy_admin.name
        legacy_admin.name = "Waleed Alharbi"
        legacy_admin.email = "waleed.alharbi@northstar.io"
        legacy_admin.department = "IT"
        legacy_admin.role = "IT Administrator"
        db.query(Ticket).filter(Ticket.assigned_technician == legacy_name).update({"assigned_technician": "Waleed Alharbi"})
    db.commit()

def seed_database(db: Session):
    if db.query(User).first():
        update_demo_admin(db)
        return
    db.add_all([User(name=n, email=e, department=d, role=r, status="Active") for n, e, d, r in USERS])
    now = datetime.now()
    db.add_all([Ticket(title=t[0], description=t[1], requester=t[2], department=t[3], category=t[4], priority=t[5], status=t[6], assigned_technician=t[7], sla=t[8], created_at=now - timedelta(days=index * 2, hours=index)) for index, t in enumerate(TICKETS)])
    db.add_all([Asset(device_type=a[0], device_name=a[1], serial_number=a[2], assigned_user=a[3], department=a[4], status=a[5], purchase_date=a[6]) for a in ASSETS])
    db.commit()




