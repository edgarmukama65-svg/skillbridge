# setup_db.py - Run this once to create the database

from database import create_tables

if __name__ == "__main__":
    create_tables()
    print("🎉 Database setup complete!")