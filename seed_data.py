from app import create_app, db
from models import Project, Skill

app = create_app()

with app.app_context():
    # Clear existing data
    Project.query.delete()
    Skill.query.delete()
    
    # Add Projects
    projects = [
        Project(
            title='Chronos HR System',
            description='Enterprise HR management platform with performance tracking, KPI management, and reporting.',
            technologies='Flask, SQL, Python, Bootstrap',
            is_featured=True,
            is_published=True
        ),
        Project(
            title='Financial Intelligence Dashboard',
            description='Power BI dashboard for financial analytics, KPI tracking, and executive reporting.',
            technologies='Power BI, Python, SQL',
            is_featured=True,
            is_published=True
        ),
        Project(
            title='Data Automation Pipeline',
            description='Python script for automated data cleaning, transformation, and analysis.',
            technologies='Python, Pandas, NumPy',
            is_featured=False,
            is_published=True
        )
    ]
    
    for p in projects:
        db.session.add(p)
    
    # Add Skills
    skills = [
        Skill(name='Python', category='Languages', proficiency=95),
        Skill(name='SQL', category='Languages', proficiency=92),
        Skill(name='Flask', category='Frameworks', proficiency=90),
        Skill(name='Power BI', category='Tools', proficiency=85),
        Skill(name='Machine Learning', category='AI', proficiency=80),
        Skill(name='JavaScript', category='Languages', proficiency=75)
    ]
    
    for s in skills:
        db.session.add(s)
    
    db.session.commit()
    print('✅ Sample data added successfully!')
    print(f'📊 Projects: {Project.query.count()}')
    print(f'📊 Skills: {Skill.query.count()}')
