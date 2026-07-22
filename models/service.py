from app import db
from datetime import datetime

class Service(db.Model):
    __tablename__ = 'service'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50), default='fa-code')
    
    def __repr__(self):
        return f'<Service {self.name}>'
