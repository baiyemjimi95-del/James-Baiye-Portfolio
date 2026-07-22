# James Baiye - Professional Portfolio

## 🚀 Live Demo
[View Portfolio](https://yourusername.github.io/james-portfolio)

## 📋 About
A professional portfolio website showcasing my work as a Software Developer, Data Analyst, and AI Developer.

## 🛠️ Technologies Used
- **Backend:** Flask (Python)
- **Database:** SQLite with SQLAlchemy
- **Frontend:** HTML5, CSS3, JavaScript
- **Authentication:** Flask-Login
- **Styling:** Custom CSS with Glassmorphism
- **Deployment:** GitHub Pages / Render

## ✨ Features
- 🎨 Premium Aurora Glass UI Design
- 🌙 Dark/Light Mode Toggle
- 📱 Fully Responsive Mobile Design
- ⌨️ Dynamic Typing Animation
- 🎯 Animated Skill Bars
- 📊 Interactive Counters
- 🏆 Admin Dashboard
- 📝 Blog Management
- 📧 Contact Form
- 💼 Portfolio Management

## 📁 Project Structure
\\\
james portfolio/
├── app/                 # Application factory
├── admin/              # Admin routes
├── models/             # Database models
├── routes/             # Main routes
├── static/             # Static files (CSS, JS, images)
├── templates/          # HTML templates
│   ├── layouts/        # Base layout
│   ├── pages/          # Page templates
│   ├── admin/          # Admin templates
│   └── errors/         # Error pages
├── instance/           # SQLite database
├── config.py           # Configuration
├── requirements.txt    # Python dependencies
├── run.py             # Application entry point
└── .env               # Environment variables
\\\

## 🚀 Local Development

### Prerequisites
- Python 3.8+
- pip

### Installation
\\\ash
# Clone the repository
git clone https://github.com/yourusername/james-portfolio.git
cd james-portfolio

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run the application
python run.py
\\\

### Admin Login
- **Username:** admin
- **Password:** admin123

## 📦 Deployment

### Deploy to Render
1. Push code to GitHub
2. Connect repository to Render
3. Set environment variables
4. Deploy!

### Deploy to GitHub Pages (Static)
For static deployment:
\\\ash
# Build static files
flask build

# Deploy to gh-pages branch
git push origin main:gh-pages
\\\

## 👨‍💻 Author
**James Baiye**
- GitHub: [@jamesbaiye](https://github.com/jamesbaiye)
- LinkedIn: [James Baiye](https://linkedin.com/in/jamesbaiye)
- Email: james@example.com

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
