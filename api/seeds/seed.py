# backend/seeds/seed.py

from app import create_app, db
from app.models import User
from app.schemas import UserCreate

app = create_app()
app.app_context().push()

def seed():
    if not User.query.filter_by(email='admin@example.com').first():
        admin_data = {
            'first_name': 'Admin',
            'last_name': 'User',
            'email': 'admin@example.com',
            'password': 'adminpassword',
            'access_level': 'admin',
            'status': 'active'
        }
        try:
            admin = UserCreate(**admin_data)
            user = User(
                first_name=admin.first_name,
                last_name=admin.last_name,
                email=admin.email,
                access_level=admin.access_level,
                status=admin.status
            )
            user.set_password(admin.password)
            db.session.add(user)
            db.session.commit()
            print("Admin user created.")
        except Exception as e:
            print(f"Erro ao criar usuário admin: {e}")
    else:
        print("Admin user already exists.")

if __name__ == '__main__':
    seed()
