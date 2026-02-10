import click
from flask.cli import with_appcontext
from application import db
from application.data.models.user import User

@click.command('create-admin')
@click.argument('email')
@click.argument('password')
@with_appcontext
def create_admin_command(email, password):
    """
    Skapar en ny admin-användare via terminalen (idempotent).
    Användning: flask create-admin <email> <password>
    
    Idempotent: Exiterar med 0 både vid skapande och om användaren redan finns.
    """
    # Kolla om användaren redan finns
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        click.echo(f"Admin user '{email}' already exists — skipping.")
        return
    
    # Validera lösenord
    if len(password) < 8:
        click.echo(f"Error: Password must be at least 8 characters long", err=True)
        raise click.Exit(1)
    
    # Skapa ny användare
    new_user = User(email=email)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    click.echo(f"Admin user '{email}' created successfully.")

def register_commands(app):
    """Registrera alla CLI-kommandon"""
    app.cli.add_command(create_admin_command)