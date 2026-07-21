# salary_estimator.py - Salary Estimation Engine

def estimate_salary(skills, experience_level, location):
    """
    Estimate salary based on skills, experience, and location
    """
    
    # Base salary by location
    location_multipliers = {
        "United States": 1.0,
        "United Kingdom": 0.8,
        "Canada": 0.7,
        "Germany": 0.75,
        "Australia": 0.7,
        "India": 0.3,
        "Uganda": 0.15,
        "Kenya": 0.2,
        "Nigeria": 0.18,
        "South Africa": 0.25,
        "Remote": 0.6
    }
    
    # Experience multipliers
    experience_multipliers = {
        "Entry": 0.6,
        "Junior": 0.8,
        "Mid-Level": 1.0,
        "Senior": 1.3,
        "Lead": 1.5,
        "Principal": 1.8,
        "Staff": 2.0
    }
    
    # Skill multipliers
    skill_multipliers = {
        "python": 1.2,
        "java": 1.15,
        "sql": 1.1,
        "javascript": 1.15,
        "react": 1.2,
        "docker": 1.15,
        "aws": 1.25,
        "kubernetes": 1.2,
        "machine learning": 1.4,
        "data science": 1.35,
        "leadership": 1.3,
        "project management": 1.15,
        "security": 1.2,
        "devops": 1.2,
        "cloud computing": 1.25,
        "tensorflow": 1.3,
        "pytorch": 1.3,
        "nlp": 1.25,
        "computer vision": 1.25,
        "golang": 1.2,
        "rust": 1.2,
        "typescript": 1.1
    }
    
    # Base salary (US average)
    base_salary = 60000
    
    # Location factor
    loc_mult = location_multipliers.get(location, 0.5)
    
    # Experience factor
    exp_mult = experience_multipliers.get(experience_level, 1.0)
    
    # Skill factor
    skill_mult = 1.0
    skill_count = 0
    for skill in skills:
        if skill.lower() in skill_multipliers:
            skill_mult += (skill_multipliers[skill.lower()] - 1) * 0.3
            skill_count += 1
    
    if skill_count > 3:
        skill_mult += 0.1  # Bonus for having many skills
    
    # Calculate estimated salary
    estimated = base_salary * loc_mult * exp_mult * skill_mult
    
    # Round to nearest 5000
    estimated = round(estimated / 5000) * 5000
    
    # Market insights
    market_ranges = {
        "United States": (70000, 150000),
        "United Kingdom": (50000, 100000),
        "Canada": (60000, 110000),
        "India": (15000, 50000),
        "Uganda": (8000, 25000)
    }
    
    market_min, market_max = market_ranges.get(location, (40000, 80000))
    
    return {
        "min": estimated - 15000,
        "max": estimated + 15000,
        "average": estimated,
        "base": int(estimated * 0.85),
        "skill_bonus": int(estimated * 0.08),
        "experience_bonus": int(estimated * 0.05),
        "location_bonus": int(estimated * 0.02),
        "market_min": market_min,
        "market_max": market_max,
        "percentile": min(100, max(0, int((estimated - market_min) / (market_max - market_min) * 100)))
    }