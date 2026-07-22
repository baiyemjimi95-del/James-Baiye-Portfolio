from app import db
from datetime import datetime

class Skill(db.Model):
    __tablename__ = 'skill'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    percentage = db.Column(db.Integer, default=80)
    category = db.Column(db.String(50), default='Technical')
    display_order = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Skill {self.name}>'
