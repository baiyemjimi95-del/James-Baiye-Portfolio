from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from models import Project, Skill, Service, BlogPost, ContactMessage, User
from app import db, csrf

admin_bp = Blueprint('admin', __name__)

# ============================================================
# DASHBOARD
# ============================================================

@admin_bp.route('/')
@login_required
def dashboard():
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    
    projects = Project.query.count()
    skills = Skill.query.count()
    services = Service.query.count()
    blogs = BlogPost.query.count()
    messages = ContactMessage.query.filter_by(is_read=False).count()
    
    return render_template('admin/dashboard.html',
        projects=projects,
        skills=skills,
        services=services,
        blogs=blogs,
        messages=messages
    )

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
            description=request.form['description'],
            technologies=request.form['technologies'],
            github_url=request.form.get('github_url', ''),
            live_url=request.form.get('live_url', ''),
            is_featured='is_featured' in request.form
        )
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
        project.technologies = request.form['technologies']
        project.github_url = request.form.get('github_url', '')
        project.live_url = request.form.get('live_url', '')
        project.is_featured = 'is_featured' in request.form
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/project_form.html', title='Edit Project', project=project)

@admin_bp.route('/projects/delete/<int:id>')
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.projects'))

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
        blog = BlogPost(
            title=request.form['title'],
            slug=slug,
            content=request.form['content'],
            excerpt=request.form.get('excerpt', request.form['content'][:200]),
            published='published' in request.form
        )
        db.session.add(blog)
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
        post.content = request.form['content']
        post.excerpt = request.form.get('excerpt', request.form['content'][:200])
        post.published = 'published' in request.form
        db.session.commit()
        flash('Blog post updated successfully!', 'success')
        return redirect(url_for('admin.blog'))
    
    return render_template('admin/blog_form.html', title='Edit Blog Post', post=post)

@admin_bp.route('/blog/delete/<int:id>')
@login_required
def delete_blog(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Blog post deleted successfully!', 'success')
    return redirect(url_for('admin.blog'))

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
# AUTHENTICATION
# ============================================================

@admin_bp.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
