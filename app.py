from flask import Flask
from sqlalchemy import create_engine, exc
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask_migrate import Migrate
from website import create_app, db


app = create_app()
migrate = Migrate(app, db)


def create_postgres_database(app):
    # Use configurations directly from the app.config
    uri = app.config['SQLALCHEMY_DATABASE_URI']
    try:
        # Try to connect to the targeted database to check if it exists
        engine = create_engine(uri)
        engine.connect()
    except exc.OperationalError:
        # Parse the database URI to extract username, password, and database name
        # Alternatively, keep using the specific variables if they are still defined in config.py
        # This section might need adjustment based on how you decide to manage configurations
        user = app.config.get('DATABASE_USERNAME')
        password = app.config.get('DATABASE_PASSWORD')
        host = 'localhost'  # or another host if specified in your configuration
        dbname = uri.split('/')[-1]  # Assumes database name is the last part of the URI

        # If it fails because the database does not exist, create it
        try:
            # Connect to the default postgres database
            conn = psycopg2.connect(dbname='postgres', user=user, host=host, password=password)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            cur.execute(f'CREATE DATABASE {dbname}')
            cur.close()
            conn.close()
            print(f"Database {dbname} created.")
        except Exception as e:
            print(f"Failed to create database {dbname}. Error: {e}")


@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    create_postgres_database(app)  # Pass the app instance to access its configuration
    with app.app_context():  # Ensure db operations are run within the application context
        db.create_all()
    print("Initialized the database.")


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
