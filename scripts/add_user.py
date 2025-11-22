#!/usr/bin/env python3
"""Add users to the application database.

Usage:
  python scripts/add_user.py             # creates two default users
  python scripts/add_user.py user pass   # creates single user
"""
import sys
import pathlib
from getpass import getpass
from werkzeug.security import generate_password_hash

# Ensure project root is on sys.path so 'from app import app' works when
# executing this script from the repo root or the scripts/ directory.
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import app
from database import db, User


def create_user(username, password):
    with app.app_context():
        db.create_all()
        if User.query.filter_by(username=username).first():
            print(f"User '{username}' already exists, skipping")
            return
        u = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(u)
        db.session.commit()
        print(f"Created user: {username}")


def main():
    if len(sys.argv) == 3:
        uname = sys.argv[1]
        pwd = sys.argv[2]
        create_user(uname, pwd)
        return

    # Default: create the two users requested
    print("No args supplied — creating default users:")
    defaults = [
        ("philippe_keita", "ilovemarate"),
        ("jonathan_allarassem", "ilovemarate"),
    ]
    for u, p in defaults:
        create_user(u, p)


if __name__ == '__main__':
    main()
