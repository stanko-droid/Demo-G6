#!/usr/bin/env python3
"""
View all subscribers from the local database.

Usage:
    python view_subscribers.py
"""

from application import create_app
from application.data.models.subscriber import Subscriber
from tabulate import tabulate

def main():
    app = create_app()
    with app.app_context():
        subscribers = Subscriber.query.all()
        
        if not subscribers:
            print("No subscribers yet.")
            return
        
        data = []
        for i, sub in enumerate(subscribers, 1):
            data.append([
                i,
                sub.email,
                sub.name,
                sub.subscribed_at.strftime("%Y-%m-%d %H:%M:%S") if sub.subscribed_at else "N/A"
            ])
        
        print("\n📊 REGISTERED SUBSCRIBERS:")
        print(tabulate(data, headers=["#", "Email", "Name", "Subscribed At"], tablefmt="grid"))
        print(f"\nTotal: {len(subscribers)} subscribers\n")

if __name__ == "__main__":
    main()
