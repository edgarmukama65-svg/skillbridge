# job_recommendations.py - Job Recommendations Engine

import random
import json

# ============================================
# JOB DATABASE
# ============================================

JOBS = [
    {
        "title": "Software Engineer",
        "company": "Google",
        "location": "Remote",
        "salary": "$120,000 - $180,000",
        "skills_required": ["python", "java", "sql", "javascript", "react", "docker", "aws", "git"],
        "experience_level": "Mid-Senior",
        "description": "Build and maintain scalable software solutions"
    },
    {
        "title": "Data Scientist",
        "company": "Amazon",
        "location": "New York, NY",
        "salary": "$130,000 - $190,000",
        "skills_required": ["python", "sql", "machine learning", "data science", "pandas", "numpy", "tensorflow"],
        "experience_level": "Mid-Senior",
        "description": "Analyze data and build ML models"
    },
    {
        "title": "DevOps Engineer",
        "company": "Microsoft",
        "location": "Seattle, WA",
        "salary": "$115,000 - $170,000",
        "skills_required": ["docker", "kubernetes", "aws", "azure", "jenkins", "ci/cd", "linux"],
        "experience_level": "Mid-Senior",
        "description": "Manage cloud infrastructure and CI/CD pipelines"
    },
    {
        "title": "Frontend Developer",
        "company": "Meta",
        "location": "Remote",
        "salary": "$110,000 - $160,000",
        "skills_required": ["javascript", "react", "html", "css", "typescript", "vue.js", "angular"],
        "experience_level": "Mid-Level",
        "description": "Build responsive user interfaces"
    },
    {
        "title": "Backend Developer",
        "company": "Netflix",
        "location": "Los Angeles, CA",
        "salary": "$125,000 - $175,000",
        "skills_required": ["python", "java", "sql", "node.js", "docker", "aws", "spring boot"],
        "experience_level": "Mid-Senior",
        "description": "Build and maintain backend services"
    },
    {
        "title": "Full Stack Developer",
        "company": "Spotify",
        "location": "Remote",
        "salary": "$120,000 - $170,000",
        "skills_required": ["python", "javascript", "react", "node.js", "sql", "docker", "aws"],
        "experience_level": "Mid-Senior",
        "description": "Build full-stack web applications"
    },
    {
        "title": "Machine Learning Engineer",
        "company": "OpenAI",
        "location": "San Francisco, CA",
        "salary": "$150,000 - $220,000",
        "skills_required": ["python", "machine learning", "tensorflow", "pytorch", "data science", "nlp"],
        "experience_level": "Senior",
        "description": "Build and deploy ML models"
    },
    {
        "title": "Cloud Engineer",
        "company": "AWS",
        "location": "Seattle, WA",
        "salary": "$120,000 - $180,000",
        "skills_required": ["aws", "azure", "gcp", "docker", "kubernetes", "linux", "ci/cd"],
        "experience_level": "Mid-Senior",
        "description": "Design and manage cloud infrastructure"
    },
    {
        "title": "Product Manager",
        "company": "Apple",
        "location": "Cupertino, CA",
        "salary": "$110,000 - $160,000",
        "skills_required": ["leadership", "communication", "agile", "scrum", "project management"],
        "experience_level": "Mid-Senior",
        "description": "Lead product development and strategy"
    },
    {
        "title": "Cybersecurity Engineer",
        "company": "Cisco",
        "location": "Remote",
        "salary": "$115,000 - $170,000",
        "skills_required": ["security", "linux", "networking", "python", "firewall", "encryption"],
        "experience_level": "Mid-Senior",
        "description": "Protect systems and data from security threats"
    }
]

# ============================================
# JOB RECOMMENDATION ENGINE
# ============================================

def recommend_jobs(skills, limit=5):
    """
    Recommend jobs based on user's skills
    
    Args:
        skills (list): List of user's skills
        limit (int): Number of jobs to return
    
    Returns:
        list: Recommended jobs with match scores
    """
    recommendations = []
    
    for job in JOBS:
        # Calculate match score
        required_skills = job.get("skills_required", [])
        matched_skills = [s for s in required_skills if s.lower() in [sk.lower() for sk in skills]]
        
        if required_skills:
            match_score = int((len(matched_skills) / len(required_skills)) * 100)
        else:
            match_score = 0
        
        # Only recommend jobs with at least 20% match
        if match_score >= 20:
            recommendations.append({
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "salary": job["salary"],
                "match_score": match_score,
                "matched_skills": matched_skills,
                "missing_skills": [s for s in required_skills if s.lower() not in [sk.lower() for sk in skills]],
                "experience_level": job.get("experience_level", "Not specified"),
                "description": job.get("description", "")
            })
    
    # Sort by match score (highest first)
    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    
    return recommendations[:limit]

def get_job_by_title(title):
    """Get job details by title"""
    for job in JOBS:
        if job["title"].lower() == title.lower():
            return job
    return None

def get_all_job_titles():
    """Get all job titles"""
    return [job["title"] for job in JOBS]

def get_skills_for_job(title):
    """Get skills required for a job"""
    job = get_job_by_title(title)
    if job:
        return job.get("skills_required", [])
    return []

def calculate_salary_estimate(skills, experience_level="Mid-Level"):
    """Estimate salary based on skills and experience"""
    base_salary = 80000
    
    # Skill multipliers
    skill_multipliers = {
        "python": 1.2,
        "java": 1.15,
        "sql": 1.1,
        "javascript": 1.15,
        "react": 1.2,
        "docker": 1.15,
        "aws": 1.25,
        "machine learning": 1.4,
        "data science": 1.35,
        "kubernetes": 1.2,
        "leadership": 1.3,
        "project management": 1.15,
        "security": 1.2
    }
    
    # Calculate average multiplier
    total_multiplier = 1.0
    count = 0
    for skill in skills:
        if skill.lower() in skill_multipliers:
            total_multiplier += skill_multipliers[skill.lower()] - 1
            count += 1
    
    avg_multiplier = total_multiplier if count == 0 else 1 + (total_multiplier - 1) / (count + 1)
    
    # Experience multiplier
    experience_multipliers = {
        "Entry": 0.8,
        "Junior": 0.9,
        "Mid-Level": 1.0,
        "Mid-Senior": 1.15,
        "Senior": 1.3,
        "Lead": 1.5
    }
    
    exp_multiplier = experience_multipliers.get(experience_level, 1.0)
    
    estimated_salary = int(base_salary * avg_multiplier * exp_multiplier)
    
    # Round to nearest 5000
    estimated_salary = round(estimated_salary / 5000) * 5000
    
    return {
        "min": estimated_salary - 10000,
        "max": estimated_salary + 10000,
        "average": estimated_salary
    }

# ============================================
# TEST FUNCTION
# ============================================

def test_recommendations():
    """Test the job recommendation engine"""
    print("=" * 50)
    print("JOB RECOMMENDATION ENGINE TEST")
    print("=" * 50)
    
    # Test with sample skills
    test_skills = ["python", "sql", "react", "javascript", "aws"]
    
    print(f"\n📋 User Skills: {', '.join(test_skills)}")
    
    recommendations = recommend_jobs(test_skills, limit=5)
    
    print(f"\n📊 Top {len(recommendations)} Job Recommendations:")
    print("-" * 50)
    
    for i, job in enumerate(recommendations, 1):
        print(f"\n{i}. {job['title']} at {job['company']}")
        print(f"   📍 {job['location']}")
        print(f"   💰 {job['salary']}")
        print(f"   🎯 Match Score: {job['match_score']}%")
        print(f"   ✅ Matched Skills: {', '.join(job['matched_skills'])}")
        if job['missing_skills']:
            print(f"   ❌ Missing Skills: {', '.join(job['missing_skills'])}")

if __name__ == "__main__":
    test_recommendations()