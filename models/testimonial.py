from app import db
from datetime import datetime

class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100))
    company = db.Column(db.String(100))
    quote = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, default=5)
    photo_url = db.Column(db.String(500))
    is_featured = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
