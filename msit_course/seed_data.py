import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from datetime import date
from decimal import Decimal
from assets.models import Asset, MaintenanceLog, User

# Create a user if none exist
if not User.objects.exists():
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='ADMIN')
    print("Created superuser: admin / admin123")
else:
    user = User.objects.first()
    print(f"Using existing user: {user.username}")

# Create a second user
user2, created = User.objects.get_or_create(username='jsmith', defaults={
    'email': 'jsmith@corp.com', 'role': 'EMPLOYEE'
})
if created:
    user2.set_password('employee123')
    user2.save()
    print("Created user: jsmith / employee123")

user3, created = User.objects.get_or_create(username='mwilson', defaults={
    'email': 'mwilson@corp.com', 'role': 'MANAGER'
})
if created:
    user3.set_password('manager123')
    user3.save()
    print("Created user: mwilson / manager123")

# Sample assets data
assets_data = [
    ("Dell Latitude 5540", "LAPTOP", "1299.99", user),
    ("HP EliteBook 840", "LAPTOP", "1450.00", user2),
    ("Lenovo ThinkPad X1", "LAPTOP", "1599.99", user3),
    ("MacBook Pro 14", "LAPTOP", "2499.00", user),
    ("Dell Inspiron 15", "LAPTOP", "899.50", user2),
    ("LG UltraWide 34WN80C", "MONITOR", "549.99", user),
    ("Samsung Odyssey G7", "MONITOR", "699.99", user2),
    ("Dell P2722H", "MONITOR", "329.99", user3),
    ("ASUS ProArt PA278CV", "MONITOR", "449.00", None),
    ("BenQ PD2700U", "MONITOR", "499.99", user),
    ("iPhone 15 Pro", "PHONE", "1199.00", user3),
    ("Samsung Galaxy S24", "PHONE", "999.99", user2),
    ("Google Pixel 8", "PHONE", "699.00", None),
    ("Herman Miller Aeron", "FURNITURE", "1395.00", user),
    ("Steelcase Leap V2", "FURNITURE", "1049.00", user3),
    ("Standing Desk Pro", "FURNITURE", "799.99", user2),
    ("Logitech Ergo K860", "FURNITURE", "129.99", None),
]

created_assets = []
for name, atype, cost, assigned in assets_data:
    asset, was_created = Asset.objects.get_or_create(
        name=name,
        defaults={
            'asset_type': atype,
            'cost': Decimal(cost),
            'assigned_to': assigned,
        }
    )
    created_assets.append(asset)
    if was_created:
        print(f"  Created asset: {name}")
    else:
        print(f"  Asset already exists: {name}")

# Sample maintenance logs
maintenance_data = [
    (created_assets[0], date(2025, 6, 15), "Replaced battery and keyboard", "249.99"),
    (created_assets[0], date(2025, 11, 20), "SSD upgrade to 1TB", "129.99"),
    (created_assets[1], date(2025, 8, 10), "Screen replacement due to crack", "350.00"),
    (created_assets[5], date(2025, 9, 5), "Power supply unit replaced", "89.99"),
    (created_assets[10], date(2025, 12, 1), "Screen protector and case replacement", "59.99"),
    (created_assets[13], date(2026, 1, 15), "Replaced arm pads and lumbar support", "175.00"),
    (created_assets[3], date(2026, 2, 10), "Logic board repair after liquid damage", "599.00"),
]

for asset, sdate, desc, cost in maintenance_data:
    log, was_created = MaintenanceLog.objects.get_or_create(
        asset=asset,
        service_date=sdate,
        defaults={
            'description': desc,
            'cost': Decimal(cost),
        }
    )
    if was_created:
        print(f"  Created maintenance log: {asset.name} on {sdate}")
    else:
        print(f"  Maintenance log already exists: {asset.name} on {sdate}")

print(f"\nDone! Total assets: {Asset.objects.count()}, Total maintenance logs: {MaintenanceLog.objects.count()}")
