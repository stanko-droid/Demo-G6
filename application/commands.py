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
    Skapar en ny admin-användare via terminalen.
    Användning: flask create-admin <email> <password>
    """
    # Kolla om användaren redan finns
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        click.echo(f"Fel: Användaren {email} finns redan!")
        return

    # Skapa ny användare
    new_user = User(email=email)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    click.echo(f"Succé! Skapade admin: {email}")