"""Main entry point for the application"""
from app import app, db

if __name__ == '__main__':
    # Ensure tables exist before serving (works with Flask 3+)
    with app.app_context():
        db.create_all()
    app.run()
