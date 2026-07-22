from app import db
from datetime import datetime

class PortfolioItem(db.Model):
    __tablename__ = 'portfolio_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(100))
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    thumbnail_url = db.Column(db.String(500))
    github_url = db.Column(db.String(500))
    live_demo_url = db.Column(db.String(500))
    documentation_url = db.Column(db.String(500))
    category = db.Column(db.String(50), nullable=False, default='Software')
    technologies = db.Column(db.String(200))
    features = db.Column(db.String(500))
    architecture = db.Column(db.Text)
    is_featured = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def get_slug(self):
        return self.title.lower().replace(' ', '-').replace('/', '-')
    
    def get_technologies_list(self):
        if not self.technologies:
            return []
        return [t.strip() for t in self.technologies.split(',')]
    
    def get_features_list(self):
        if not self.features:
            return []
        return [f.strip() for f in self.features.split(',')]

class PortfolioScreenshot(db.Model):
    __tablename__ = 'portfolio_screenshots'
    
    id = db.Column(db.Integer, primary_key=True)
    portfolio_item_id = db.Column(db.Integer, db.ForeignKey('portfolio_items.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.String(200))
    display_order = db.Column(db.Integer, default=0)
