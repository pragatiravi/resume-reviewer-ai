import os
from flask import Flask, render_template
from flask_login import LoginManager
from models import db, login_manager, User
from routes import main, auth, resume
from config import Config

def create_app(config_class=Config):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(resume, url_prefix='/resume')
    
    # Create uploads directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize database if it doesn't exist
    with app.app_context():
        db.create_all()
        print('Database tables created or confirmed to exist.')
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
        
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # Shell context
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User}
    
    # Database initialization command
    @app.cli.command('init-db')
    def init_db():
        """Create database tables"""
        db.create_all()
        print('Database initialized.')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 