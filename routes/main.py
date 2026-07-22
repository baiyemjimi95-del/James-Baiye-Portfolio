from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Project, Skill, Service, BlogPost, ContactMessage
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured_projects = Project.query.filter_by(is_featured=True).limit(2).all()
    skills = Skill.query.order_by(Skill.display_order).all()
    services = Service.query.all()
    return render_template('pages/home.html',
        projects=featured_projects,
        skills=skills,
        services=services
    )

@main_bp.route('/about')
def about():
    return render_template('pages/about.html')

@main_bp.route('/portfolio')
def portfolio():
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('pages/portfolio.html', projects=all_projects)

@main_bp.route('/services')
def services_page():
    services = Service.query.all()
    return render_template('pages/services.html', services=services)

@main_bp.route('/blog')
def blog():
    posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).all()
    return render_template('pages/blog.html', posts=posts)

@main_bp.route('/contact')
def contact():
    return render_template('pages/contact.html')

@main_bp.route('/contact/submit', methods=['POST'])
def submit_contact():
    msg = ContactMessage(
        name=request.form['name'],
        email=request.form['email'],
        subject=request.form.get('subject', ''),
        message=request.form['message']
    )
    db.session.add(msg)
    db.session.commit()
    flash('Thank you! Your message has been sent.', 'success')
    return redirect(url_for('main.contact'))