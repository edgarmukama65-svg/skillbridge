# test_save.py - Test saving an analysis

from database import save_analysis, get_user_analyses, get_all_users
import uuid

# First, list all users
print("📋 Finding users in database...")
users = get_all_users()

if not users:
    print("❌ No users found! Please register a user first.")
    print("   Go to the app and register, or insert a user in phpMyAdmin.")
    exit()

# Show users and let user choose
print("\n📋 Available users:")
for i, user in enumerate(users):
    print(f"  {i+1}. {user[1]} ({user[2]}) - ID: {user[0]}")

# Use the first user
user_id = users[0][0]
print(f"\n✅ Using user: {users[0][1]} ({users[0][2]}) with ID: {user_id}")

# Test data
result = {
    "job_title": "Test Job",
    "ats_score": 85,
    "skills_have": ["Python", "SQL", "Java"],
    "skills_need": ["Docker", "AWS", "Kubernetes"],
    "skills_missing": ["Docker", "AWS"],
    "learning_roadmap": ["Learn Docker", "Get AWS Certified"],
    "resume_tips": ["Add Docker to resume", "Quantify achievements"]
}

resume_text = "This is a test resume"
job_description = "This is a test job description"

print(f"\n🔄 Testing save_analysis for user: {user_id}")
analysis_id = save_analysis(user_id, result, resume_text, job_description)

if analysis_id:
    print(f"✅ Analysis saved with ID: {analysis_id}")
    
    # Verify it was saved
    analyses = get_user_analyses(user_id)
    
    if analyses is None:
        print("⚠️ No analyses returned (None)")
    elif len(analyses) == 0:
        print("⚠️ No analyses found for this user")
    else:
        print(f"📊 Total analyses for user: {len(analyses)}")
        
        print("\n📋 Recent analyses:")
        print("-" * 60)
        for a in analyses[:5]:
            try:
                # Get column values - using correct indexes
                # Based on your table structure:
                # 0: Id, 1: UserId, 2: ResumeText, 3: JobTitle, 4: CompanyName,
                # 5: JobDescription, 6: AtsScore, 7: SkillsHave, 8: SkillsNeed,
                # 9: Status, 10: ProcessingTimeMs, 11: CreatedAt
                
                created_at = a[11] if len(a) > 11 else "No Date"
                ats_score = a[6] if len(a) > 6 else 0
                job_title = a[3] if len(a) > 3 else "No Job"
                analysis_id_val = a[0] if len(a) > 0 else "No ID"
                
                # Format the date nicely
                if created_at != "No Date" and created_at:
                    try:
                        # Try to format the date
                        date_short = created_at[:16].replace("T", " ") if len(created_at) > 16 else created_at
                    except:
                        date_short = created_at
                else:
                    date_short = "No Date"
                
                print(f"🆔 ID: {analysis_id_val}")
                print(f"   📅 Date: {date_short}")
                print(f"   📊 Score: {ats_score}%")
                print(f"   💼 Job: {job_title}")
                print("-" * 60)
                
            except Exception as e:
                print(f"❌ Error displaying analysis: {e}")
                print(f"   Raw data: {a}")
                print("-" * 60)
else:
    print("❌ Failed to save analysis")