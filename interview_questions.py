# interview_questions.py - Interview Questions Generator

import random

INTERVIEW_QUESTIONS = {
    "Technical": {
        "Software Engineer": [
            "Explain the difference between Python lists and tuples.",
            "How would you optimize a slow SQL query?",
            "What is the virtual DOM and how does React use it?",
            "Explain the concept of RESTful APIs.",
            "What is the difference between SQL and NoSQL databases?",
            "How does garbage collection work in Python?",
            "Explain the SOLID principles in OOP.",
            "What is CI/CD and why is it important?",
            "What is the difference between TCP and UDP?",
            "Explain the concept of microservices architecture."
        ],
        "Data Scientist": [
            "Explain the difference between supervised and unsupervised learning.",
            "What is overfitting and how do you prevent it?",
            "How would you handle missing data in a dataset?",
            "Explain the bias-variance tradeoff.",
            "What is the difference between classification and regression?",
            "How do you evaluate the performance of a machine learning model?",
            "Explain what PCA does and when you would use it.",
            "What is the difference between L1 and L2 regularization?",
            "How does gradient descent work?",
            "Explain the concept of cross-validation."
        ],
        "DevOps Engineer": [
            "What is the difference between Docker and Kubernetes?",
            "Explain the CI/CD pipeline in detail.",
            "How do you handle infrastructure as code?",
            "What is the difference between blue-green and canary deployments?",
            "How do you monitor and log in a microservices architecture?",
            "Explain the concept of immutable infrastructure.",
            "What is the difference between Ansible and Terraform?"
        ],
        "Frontend Developer": [
            "What is the difference between CSS Flexbox and Grid?",
            "Explain the React component lifecycle.",
            "What is the difference between state and props in React?",
            "How do you optimize a website for performance?",
            "Explain the concept of hoisting in JavaScript.",
            "What is the difference between '==' and '===' in JavaScript?",
            "Explain how the event loop works in JavaScript."
        ],
        "Backend Developer": [
            "Explain the concept of middleware in Node.js.",
            "How do you handle authentication in a REST API?",
            "What is the difference between REST and GraphQL?",
            "Explain the ACID properties in databases.",
            "What is the difference between synchronous and asynchronous programming?",
            "How do you handle database migrations?",
            "Explain the concept of idempotency in APIs."
        ],
        "ML Engineer": [
            "How do you deploy a machine learning model to production?",
            "What is model drift and how do you detect it?",
            "Explain the difference between batch and real-time inference.",
            "How do you handle large datasets for training?",
            "What is feature engineering and why is it important?"
        ]
    },
    "Behavioral": [
        "Tell me about a time you faced a difficult challenge and how you overcame it.",
        "How do you handle disagreements with team members?",
        "Describe a situation where you showed leadership.",
        "How do you prioritize your work when facing multiple deadlines?",
        "Tell me about a time you made a mistake and how you handled it.",
        "How do you stay updated with new technologies?",
        "Describe a project you're most proud of.",
        "How do you handle feedback and criticism?",
        "Tell me about a time you worked in a team and faced challenges.",
        "How do you handle stress and pressure?",
        "Describe your ideal work environment.",
        "Why do you want to work in this industry?"
    ]
}

# Sample answers for technical questions
SAMPLE_ANSWERS = {
    "Explain the difference between Python lists and tuples.": "Lists are mutable (can be changed), tuples are immutable (cannot be changed). Lists use square brackets [], tuples use parentheses (). Lists are slower, tuples are faster.",
    "How would you optimize a slow SQL query?": "1. Use indexes on columns used in WHERE clauses. 2. Avoid SELECT * - only select needed columns. 3. Use JOIN instead of subqueries when possible. 4. Use query caching. 5. Analyze the query execution plan.",
    "What is the virtual DOM and how does React use it?": "The virtual DOM is a lightweight copy of the real DOM. React uses it to track changes in state and efficiently update only the parts of the real DOM that have changed, improving performance."
}

def generate_questions(job_title, experience_level, skills, num_technical=5, num_behavioral=3):
    """Generate interview questions based on job title, experience, and skills"""
    
    technical_questions = []
    behavioral_questions = []
    all_questions = []
    
    # Get technical questions for the job title
    job_questions = INTERVIEW_QUESTIONS["Technical"].get(job_title, [])
    
    if job_questions:
        num_tech = min(num_technical, len(job_questions))
        selected = random.sample(job_questions, num_tech)
        for q in selected:
            technical_questions.append({
                "question": q,
                "answer": SAMPLE_ANSWERS.get(q, "Think about the key concepts and provide a clear explanation with examples.")
            })
    
    # Get behavioral questions
    num_behav = min(num_behavioral, len(INTERVIEW_QUESTIONS["Behavioral"]))
    selected = random.sample(INTERVIEW_QUESTIONS["Behavioral"], num_behav)
    for q in selected:
        behavioral_questions.append({
            "question": q,
            "answer": "Use the STAR method: Situation, Task, Action, Result."
        })
    
    # Generate skill-based questions
    skill_questions = []
    for skill in skills[:3]:
        skill_questions.append({
            "question": f"How have you used {skill} in your previous projects?",
            "answer": f"Prepare a specific example of a project where you used {skill} and the impact it had."
        })
    
    return {
        "technical": technical_questions,
        "behavioral": behavioral_questions,
        "skill_questions": skill_questions
    }