from app import db
from datetime import datetime

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    excerpt = db.Column(db.String(500))
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(500))
    tags = db.Column(db.String(500))
    author = db.Column(db.String(100), default='James Baiye')
    view_count = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def get_tags_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',')]
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'
