# James Baiye | Portfolio & Personal Brand

## From Curiosity to Creation

### ?? Live Demo
Coming soon...

### ?? About
A professional portfolio website with full CMS admin panel built with Flask.

### ??? Technologies Used
- **Backend:** Flask (Python)
- **Database:** SQLite with SQLAlchemy
- **Frontend:** HTML5, CSS3, JavaScript
- **Authentication:** Flask-Login
- **Styling:** Custom CSS with Glassmorphism
- **Admin Panel:** Full CRUD operations

### ? Features
- ?? Premium Aurora Glass UI Design
- ?? Dark/Light Mode Toggle
- ?? Fully Responsive Mobile Design
- ?? Dynamic Typing Animation
- ?? Animated Skill Bars
- ?? Interactive Counters
- ?? Full Admin Dashboard
- ?? Blog Management (CRUD)
- ?? Project Management (CRUD)
- ??? Skills & Services Management
- ?? Contact Form with Messages
- ??? Image Upload Support

### ?? Project Structure
\\\
james-portfolio/
+-- app/
¦   +-- __init__.py
¦   +-- admin.py
+-- models/
+-- routes/
+-- static/
+-- templates/
+-- config.py
+-- run.py
+-- requirements.txt
\\\

### ????? Run Locally
\\\ash
# Clone the repository
git clone https://github.com/baiyemjimi95-del/James-Baiye-Portfolio.git
cd james-portfolio

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Initialize database
python -c "from app import create_app, db; app = create_app(); with app.app_context(): db.create_all()"

# Run the application
python run.py
\\\

### ?? Admin Login
- **Username:** admin
- **Password:** admin123

### ????? Author
**James Baiye**
- GitHub: [@baiyemjimi95-del](https://github.com/baiyemjimi95-del)

### ?? License
This project is open source and available under the [MIT License](LICENSE).

