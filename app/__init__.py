from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()
cache = Cache()
cors = CORS()

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    from config import config as config_dict
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static")
    )
    
    app.config.from_object(config_dict[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)
    cors.init_app(app)
    
    # Login configuration
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Please log in to access the admin panel.'
    
    # Import models
    from models import User, Project, Skill, Service, BlogPost, ContactMessage
    
    # Register blueprints
    from routes.main import main_bp
    app.register_blueprint(main_bp)
    
    from auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from admin.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from portfolio.routes import portfolio_bp
    app.register_blueprint(portfolio_bp, url_prefix='/portfolio')
    
    from blog.routes import blog_bp
    app.register_blueprint(blog_bp, url_prefix='/blog')
    
    from services.routes import services_bp
    app.register_blueprint(services_bp, url_prefix='/services')
    
    from contact.routes import contact_bp
    app.register_blueprint(contact_bp, url_prefix='/contact')
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # Context processors
    @app.context_processor
    def utility_processor():
        from datetime import datetime
        return {
            'site_name': 'James Baiye - Software Developer',
            'current_year': datetime.now().year,
            'user': current_user
        }
    
    return app
