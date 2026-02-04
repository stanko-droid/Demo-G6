#!/usr/bin/env python
"""
Sync subscribers from Azure SQL to local SQLite database.
Run this script to pull latest registrations from Azure and display them locally.
"""

from application import create_app, db
from application.data.models.subscriber import Subscriber
from tabulate import tabulate


def sync_azure_to_local():
    """Fetch subscribers from Azure and sync to local database."""
    print("\n" + "="*80)
    print("🔄 SYNCING AZURE → LOCAL DATABASE")
    print("="*80 + "\n")
    
    # Connect to Azure (production)
    app_azure = create_app("production")
    azure_subscribers = []
    
    with app_azure.app_context():
        azure_subscribers = db.session.query(Subscriber).order_by(
            Subscriber.subscribed_at.desc()
        ).all()
        print(f"📥 Hämtade {len(azure_subscribers)} registreringar från Azure\n")
    
    # Sync to local (development)
    app_local = create_app("development")
    
    with app_local.app_context():
        synced_count = 0
        for sub in azure_subscribers:
            existing = db.session.query(Subscriber).filter_by(
                email=sub.email
            ).first()
            
            if not existing:
                new_sub = Subscriber(email=sub.email, name=sub.name)
                db.session.add(new_sub)
                synced_count += 1
        
        db.session.commit()
        print(f"✅ Synkade {synced_count} nya registreringar lokalt\n")
        
        # Get all local subscribers
        all_local = db.session.query(Subscriber).order_by(
            Subscriber.subscribed_at.desc()
        ).all()
        
        # Prepare table data
        table_data = []
        for i, sub in enumerate(all_local, 1):
            table_data.append([
                i,
                sub.email,
                sub.name,
                sub.subscribed_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        # Display as table
        headers = ["#", "Email", "Namn", "Registrerad"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print(f"\n📊 TOTALT: {len(all_local)} registreringar lokalt")
        print("="*80 + "\n")


if __name__ == "__main__":
    sync_azure_to_local()

