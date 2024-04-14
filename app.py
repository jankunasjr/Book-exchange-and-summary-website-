from flask import Flask
from sqlalchemy import true

from website import create_app

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
