import subprocess
import sys
import signal

COMPOSE_FILE = "docker-compose.dev.yml"

def compose_up():
    return subprocess.run(
        ["docker", "compose", "-f", COMPOSE_FILE, "up", "-d"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

def compose_down(*args, **kwargs):
    return subprocess.run(
        ["docker", "compose", "-f", COMPOSE_FILE, "down"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

def flask_run():
    return subprocess.run(
        ["flask", "run", "-h", "0.0.0.0", "-p", "5000"],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

def create_tables():
    from manage import app
    from effective_mobile_task import db

    with app.app_context():
        db.create_all()

def create_admin_user():
    from manage import app
    from effective_mobile_task import db
    from effective_mobile_task.models import User, ADMIN_ROLE
    from werkzeug.security import generate_password_hash

    admin_email = "a@mail.com"
    admin_password = "12345678"

    with app.app_context():
        password_hash = generate_password_hash(admin_password)
        admin = User(
            name="Admin",
            last_name="Admin",
            email=admin_email,
            password=password_hash,
            is_active=True,
            role=ADMIN_ROLE,   # предполагается наличие поля role_id в модели User
        )
        db.session.add(admin)
        db.session.commit()


def main():
    signal.signal(signal.SIGTERM, compose_down)
    signal.signal(signal.SIGINT, compose_down)
    signal.signal(signal.SIGHUP, compose_down)

    up_process = compose_up()

    if up_process.returncode == 0:
        create_tables()
        create_admin_user()
        flask_run()

    compose_down()