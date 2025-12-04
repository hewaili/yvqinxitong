from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Create Admin
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        print("Created admin user: admin / admin123")
    
    # Create Normal User
    if not User.query.filter_by(username='user').first():
        user = User(username='user', role='user')
        user.set_password('user123')
        db.session.add(user)
        print("Created normal user: user / user123")
    
    db.session.commit()
    print("Seeding completed.")
