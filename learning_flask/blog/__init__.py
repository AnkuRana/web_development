from flask import Flask
from extensions import db, migrate
from config import DevConfig



def create_app():
    app =  Flask(__name__)
    app.config.from_object(DevConfig)
    db.init_app(app)
    migrate.init_app(app)
    
    
    return app