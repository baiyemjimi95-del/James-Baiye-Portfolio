from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Project, Skill, BlogPost, ContactMessage
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    featured_projects = Project.query.filter_by(is_featured=True, is_published=True).limit(6).all()
    skills = Skill.query.order_by(Skill.display_order).all()
    return render_template('pages/home.html', 
        projects=featured_projects,
        skills=skills
    )

@main_bp.route('/about')
def about():
    return render_template('pages/about.html')

@main_bp.route('/projects')
def projects():
    all_projects = Project.query.filter_by(is_published=True).order_by(Project.created_at.desc()).all()
    return render_template('pages/projects.html', projects=all_projects)

@main_bp.route('/project/<slug>')
def project_detail(slug):
    project = Project.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template('pages/project_detail.html', project=project)

@main_bp.route('/blog')
def blog():
    posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.published_at.desc()).all()
    return render_template('pages/blog.html', posts=posts)

@main_bp.route('/blog/<slug>')
def blog_post(slug):
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template('pages/blog_post.html', post=post)

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
