"""Fastapp Tools
Tools to manage fastapp outside of server runtime.
Used for things such as initializing the database, creating users, etc.

Author: Collin Meyer
Created: 2024-01-12 21:27
"""
import typer
import rich
from passlib.context import CryptContext

from fastapp.db.db import engine, get_db
from fastapp.db.schema import Base
from fastapp.db.schema import User

cli = typer.Typer()
console = rich.console.Console()

db_app = typer.Typer()
cli.add_typer(db_app, name="db")


@db_app.command()
def init(
    admin_name: str = typer.Option(..., prompt=True),
    admin_email: str = typer.Option(..., prompt=True),
    admin_password: str = typer.Option(..., prompt=True, hide_input=True),
):
    """Initialize the database"""
    Base.metadata.create_all(bind=engine)

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password = pwd_context.hash(admin_password)

    admin = User(
        name=admin_name,
        email=admin_email,
        password=password,
        is_admin=True,
        is_active=True,
    )

    # Generator function, must call next to get instance
    db = next(get_db())
    db.add(admin)
    db.commit()
    typer.echo("Admin user created")


@db_app.command()
def add(name: str, email: str, password: str, is_admin: bool, is_active: bool):
    """Add a user to the database"""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password = pwd_context.hash(password)

    user = User(
        name=name,
        email=email,
        password=password,
        is_admin=is_admin,
        is_active=is_active,
    )

    # Generator function, must call next to get instance
    db = next(get_db())
    db.add(user)
    db.commit()
    typer.echo("User created")


@db_app.command()
def drop():
    """Drop the database"""
    console.print(
        rich.text.Text("Are you sure you want to drop the database? ")
        + rich.text.Text("All data will be lost!!!", style="bold red")
    )

    conf = typer.prompt("Type 'drop_db' to confirm: ", confirmation_prompt=True)
    if conf != "drop_db":
        typer.echo("Entered text != 'drop_db', database not dropped...")
        raise typer.Abort()

    Base.metadata.drop_all(bind=engine)
    typer.echo("Database dropped")


db_show_app = typer.Typer()
db_app.add_typer(db_show_app, name="show")


def users_table(users_list: list[User], title: str = "Users"):
    """Print a table of users using rich package

    Args:
        users_list (list[User]): List of users to display
        title (str, optional): Title of table. Defaults to "Users".
    """
    table = rich.table.Table(title=title)

    table.add_column("Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Email", style="magenta")
    table.add_column("Active", justify="right", style="green")

    for user in users_list:
        table.add_row(user.name, user.email, str(user.is_active))

    console.print(table)


@db_show_app.command()
def admins():
    """Show all admin users"""
    db = next(get_db())
    # pylint: disable=singleton-comparison
    adms = db.query(User).filter(User.is_admin == True).all()
    users_table(adms, "Admins")


@db_show_app.command()
def users():
    """Show all users"""
    db = next(get_db())
    usrs = db.query(User).all()
    users_table(usrs)


def main():
    """Entry point for fastapp-tools"""
    cli()
