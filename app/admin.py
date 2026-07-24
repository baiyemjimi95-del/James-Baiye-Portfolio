from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
import uuid
from datetime import datetime
from app import db, csrf
from models import User, Project, BlogPost, Skill, ContactMessage, Service

admin_bp = Blueprint('admin', __name__)

# ============================================================
# HELPERS
# ============================================================
def save_image(file, folder='projects'):
    if not file or not file.filename:
        return None
    
    upload_folder = os.path.join(current_app.root_path, 'static', 'images', folder)
    os.makedirs(upload_folder, exist_ok=True)
    
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    return f"{folder}/{filename}"

def delete_image(filename):
    if not filename:
        return
    filepath = os.path.join(current_app.root_path, 'static', 'images', filename)
    if os.path.exists(filepath):
        os.remove(filepath)

# ============================================================
# AUTHENTICATION
# ============================================================
@admin_bp.route('/login', methods=['GET', 'POST'])
@csrf.exempt  # <--- DISABLE CSRF FOR LOGIN
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            flash('Welcome back!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))

# ============================================================
# DASHBOARD
# ============================================================
@admin_bp.route('/')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    stats = {
        'projects': Project.query.count(),
        'blogs': BlogPost.query.count(),
        'skills': Skill.query.count(),
        'services': Service.query.count(),
        'messages': ContactMessage.query.filter_by(is_read=False).count(),
        'total_messages': ContactMessage.query.count()
    }
    
    recent_messages = ContactMessage.query.order_by(
        ContactMessage.created_at.desc()
    ).limit(5).all()
    
    recent_projects = Project.query.order_by(
        Project.created_at.desc()
    ).limit(5).all()
    
    return render_template('admin/dashboard.html',
        stats=stats,
        recent_messages=recent_messages,
        recent_projects=recent_projects
    )

# ============================================================
# PROFILE MANAGEMENT
# ============================================================
@admin_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile = User.query.filter_by(username='admin').first()
    if not profile:
        flash('Profile not found.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        profile.full_name = request.form['full_name']
        profile.email = request.form['email']
        
        if request.form.get('password') and request.form['password'] != '':
            if request.form['password'] == request.form.get('confirm_password', ''):
                profile.set_password(request.form['password'])
                flash('Password updated successfully!', 'success')
            else:
                flash('Passwords do not match.', 'danger')
                return redirect(url_for('admin.profile'))
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin.profile'))
    
    return render_template('admin/profile.html', profile=profile)

# ============================================================
# PROJECT MANAGEMENT
# ============================================================
@admin_bp.route('/projects')
@login_required
def projects():
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=all_projects)

@admin_bp.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        project = Project(
            title=request.form['title'],
            slug=request.form['title'].lower().replace(' ', '-').replace('/', '-'),
            description=request.form['description'],
            technologies=request.form.get('technologies', ''),
            github_url=request.form.get('github_url', ''),
            live_url=request.form.get('live_url', ''),
            category=request.form.get('category', 'Web'),
            is_featured='is_featured' in request.form,
            is_published='is_published' in request.form
        )
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                project.image = save_image(file, 'projects')
        
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/project_form.html', title='Add Project', project=None)

@admin_bp.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    
    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.technologies = request.form.get('technologies', '')
        project.github_url = request.form.get('github_url', '')
        project.live_url = request.form.get('live_url', '')
        project.category = request.form.get('category', 'Web')
        project.is_featured = 'is_featured' in request.form
        project.is_published = 'is_published' in request.form
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                if project.image:
                    delete_image(project.image)
                project.image = save_image(file, 'projects')
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/project_form.html', title='Edit Project', project=project)

@admin_bp.route('/projects/delete/<int:id>')
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    if project.image:
        delete_image(project.image)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.projects'))

# ============================================================
# BLOG MANAGEMENT
# ============================================================
@admin_bp.route('/blog')
@login_required
def blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/blog.html', posts=posts)

@admin_bp.route('/blog/add', methods=['GET', 'POST'])
@login_required
def add_blog():
    if request.method == 'POST':
        slug = request.form['title'].lower().replace(' ', '-').replace('/', '-')
        existing = BlogPost.query.filter_by(slug=slug).first()
        if existing:
            slug = f"{slug}-{uuid.uuid4().hex[:4]}"
        
        post = BlogPost(
            title=request.form['title'],
            slug=slug,
            excerpt=request.form.get('excerpt', request.form['content'][:200]),
            content=request.form['content'],
            tags=request.form.get('tags', ''),
            is_published='is_published' in request.form
        )
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                post.image = save_image(file, 'blog')
        
        db.session.add(post)
        db.session.commit()
        flash('Blog post added successfully!', 'success')
        return redirect(url_for('admin.blog'))
    
    return render_template('admin/blog_form.html', title='Add Blog Post', post=None)

@admin_bp.route('/blog/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blog(id):
    post = BlogPost.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.excerpt = request.form.get('excerpt', request.form['content'][:200])
        post.content = request.form['content']
        post.tags = request.form.get('tags', '')
        post.is_published = 'is_published' in request.form
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                if post.image:
                    delete_image(post.image)
                post.image = save_image(file, 'blog')
        
        db.session.commit()
        flash('Blog post updated successfully!', 'success')
        return redirect(url_for('admin.blog'))
    
    return render_template('admin/blog_form.html', title='Edit Blog Post', post=post)

@admin_bp.route('/blog/delete/<int:id>')
@login_required
def delete_blog(id):
    post = BlogPost.query.get_or_404(id)
    if post.image:
        delete_image(post.image)
    db.session.delete(post)
    db.session.commit()
    flash('Blog post deleted successfully!', 'success')
    return redirect(url_for('admin.blog'))

# ============================================================
# SKILL MANAGEMENT
# ============================================================
@admin_bp.route('/skills')
@login_required
def skills():
    all_skills = Skill.query.order_by(Skill.display_order).all()
    return render_template('admin/skills.html', skills=all_skills)

@admin_bp.route('/skills/add', methods=['POST'])
@login_required
def add_skill():
    skill = Skill(
        name=request.form['name'],
        percentage=int(request.form['percentage']),
        category=request.form.get('category', 'Technical')
    )
    db.session.add(skill)
    db.session.commit()
    flash('Skill added successfully!', 'success')
    return redirect(url_for('admin.skills'))

@admin_bp.route('/skills/edit/<int:id>', methods=['POST'])
@login_required
def edit_skill(id):
    skill = Skill.query.get_or_404(id)
    skill.name = request.form['name']
    skill.percentage = int(request.form['percentage'])
    db.session.commit()
    flash('Skill updated successfully!', 'success')
    return redirect(url_for('admin.skills'))

@admin_bp.route('/skills/delete/<int:id>')
@login_required
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('admin.skills'))

# ============================================================
# SERVICES MANAGEMENT
# ============================================================
@admin_bp.route('/services')
@login_required
def services():
    all_services = Service.query.order_by(Service.display_order).all()
    return render_template('admin/services.html', services=all_services)

@admin_bp.route('/services/add', methods=['POST'])
@login_required
def add_service():
    service = Service(
        name=request.form['name'],
        description=request.form.get('description', ''),
        icon=request.form.get('icon', 'fa-code')
    )
    db.session.add(service)
    db.session.commit()
    flash('Service added successfully!', 'success')
    return redirect(url_for('admin.services'))

@admin_bp.route('/services/edit/<int:id>', methods=['POST'])
@login_required
def edit_service(id):
    service = Service.query.get_or_404(id)
    service.name = request.form['name']
    service.description = request.form.get('description', '')
    service.icon = request.form.get('icon', 'fa-code')
    db.session.commit()
    flash('Service updated successfully!', 'success')
    return redirect(url_for('admin.services'))

@admin_bp.route('/services/delete/<int:id>')
@login_required
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted successfully!', 'success')
    return redirect(url_for('admin.services'))

# ============================================================
# MESSAGES
# ============================================================
@admin_bp.route('/messages')
@login_required
def messages():
    all_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=all_messages)

@admin_bp.route('/messages/read/<int:id>')
@login_required
def read_message(id):
    message = ContactMessage.query.get_or_404(id)
    message.is_read = True
    db.session.commit()
    flash('Message marked as read.', 'success')
    return redirect(url_for('admin.messages'))

@admin_bp.route('/messages/delete/<int:id>')
@login_required
def delete_message(id):
    message = ContactMessage.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('admin.messages'))

# ============================================================
# SETTINGS
# ============================================================
@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('admin.settings'))
    
    return render_template('admin/settings.html')
