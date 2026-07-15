# test_db.py - Test database connection

from database import register_user, login_user, save_analysis, get_user_analyses
from database import create_tables

print("✅ Imports successful!")

# Check connection
print("🔄 Creating tables...")
create_tables()

print("✅ All good!")