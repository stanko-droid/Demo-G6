#!/bin/bash
# Quick script to show latest subscribers from both databases

cd /Users/ludwigsevenheim/Demo-G6
source .venv/bin/activate

python << 'EOF'
from application import create_app, db
from application.data.models.subscriber import Subscriber
from tabulate import tabulate

print("\n" + "="*80)
print("📊 LATEST SUBSCRIBERS FROM BOTH DATABASES")
print("="*80 + "\n")

# Show local database
app_dev = create_app("development")
with app_dev.app_context():
    local_subs = db.session.query(Subscriber).order_by(
        Subscriber.subscribed_at.desc()
    ).all()
    
    print(f"📍 LOCAL DATABASE (SQLite) - {len(local_subs)} registreringar:")
    print("-" * 80)
    table_data = []
    for i, sub in enumerate(local_subs, 1):
        table_data.append([i, sub.email, sub.name, sub.subscribed_at.strftime('%Y-%m-%d %H:%M:%S')])
    
    headers = ["#", "Email", "Namn", "Registrerad"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Show Azure database
print("\n")
app_prod = create_app("production")
with app_prod.app_context():
    azure_subs = db.session.query(Subscriber).order_by(
        Subscriber.subscribed_at.desc()
    ).all()
    
    print(f"☁️  AZURE DATABASE (SQL Server) - {len(azure_subs)} registreringar:")
    print("-" * 80)
    table_data = []
    for i, sub in enumerate(azure_subs, 1):
        table_data.append([i, sub.email, sub.name, sub.subscribed_at.strftime('%Y-%m-%d %H:%M:%S')])
    
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

print("\n" + "="*80 + "\n")

EOF
