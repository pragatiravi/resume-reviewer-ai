from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize SQLAlchemy and LoginManager
db = SQLAlchemy()
login_manager = LoginManager()

# Import models after db is defined to avoid circular imports
from .user import User
from .resume import Resume
from .feedback import Feedback 