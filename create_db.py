from app import create_app, db
import os

# Ensure instance folder exists
os.makedirs('instance', exist_ok=True)

app = create_app()

with app.app_context():
    db.create_all()
    print('✅ Database created successfully!')
    print(f'📁 Location: {app.config["SQLALCHEMY_DATABASE_URI"]}')
