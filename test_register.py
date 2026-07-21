# test_register.py - Test registration directly

from database import register_user, get_all_users

print("=" * 50)
print("TESTING REGISTRATION")
print("=" * 50)

# Check users before registration
print("\n📋 Users BEFORE registration:")
users = get_all_users()
if users:
    for user in users:
        print(f"  👤 {user[1]} ({user[2]}) - Role: {user[3]}")
else:
    print("  No users found")

# Register a test user
print("\n🔄 Registering test user...")
name = "Test User"
email = "testuser@email.com"
password = "123456"

user_id, message = register_user(name, email, password)

if user_id:
    print(f"✅ Registration successful! User ID: {user_id}")
else:
    print(f"❌ Registration failed: {message}")

# Check users after registration
print("\n📋 Users AFTER registration:")
users = get_all_users()
if users:
    for user in users:
        print(f"  👤 {user[1]} ({user[2]}) - Role: {user[3]}")
else:
    print("  No users found")