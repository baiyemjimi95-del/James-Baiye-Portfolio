from app import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True)
    subtitle = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text)
    image = db.Column(db.String(500))
    technologies = db.Column(db.String(500))
    github_url = db.Column(db.String(500))
    live_url = db.Column(db.String(500))
    category = db.Column(db.String(50), default='Web')
    is_featured = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def get_slug(self):
        if not self.slug:
            self.slug = self.title.lower().replace(' ', '-').replace('/', '-')
        return self.slug
    
    def get_technologies_list(self):
        if not self.technologies:
            return []
        return [t.strip() for t in self.technologies.split(',')]
    
    def __repr__(self):
        return f'<Project {self.title}>'
