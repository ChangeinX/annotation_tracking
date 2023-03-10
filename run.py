import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from flask_migrate import Migrate, upgrade

from app import create_app, db
from app.models import User, Role, Permission, AnnotationTracking

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        Role=Role,
        Permission=Permission,
        AnnotationTracking=AnnotationTracking,
    )


@app.cli.command()
def deploy():
    upgrade()
    Role.insert_roles()


if __name__ == '__main__':
    app.run()
