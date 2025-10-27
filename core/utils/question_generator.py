import random
from core.models import Question, UserQuestionSet

# Predefined questions for job roles - keep as fallback
QUESTION_BANK = {
    'backend developer': [
        "Explain the concept of RESTful APIs.",
        "What are the differences between SQL and NoSQL databases?",
        "How do you optimize a slow database query?",
        "What is middleware in web development?",
        "Explain caching strategies in backend development."
    ],
    'frontend developer': [
        "What is the Virtual DOM?",
        "Explain the difference between HTML and JSX.",
        "What are promises and async/await in JavaScript?",
        "What are key features of React?",
        "How do you optimize website performance?"
    ],
    'data scientist': [
        "What is the difference between supervised and unsupervised learning?",
        "Explain overfitting and how to prevent it.",
        "What are some common data preprocessing techniques?",
        "Describe the bias-variance tradeoff.",
        "How do you select important features?"
    ],
}

def generate_questions_based_on_role(role, num_questions=5, difficulty=None, user=None):
    # Try to get questions from the database first
    query = Question.objects.filter(job_role__iexact=role.lower())
    
    # Apply difficulty filter if provided
    if difficulty:
        query = query.filter(difficulty=difficulty)
    
    # Get questions from database
    db_questions = list(query.values_list('text', flat=True))
    
    # If not enough questions in DB, fall back to predefined questions
    if len(db_questions) < num_questions:
        fallback_questions = QUESTION_BANK.get(role.lower(), [])
        # Combine DB questions with fallback questions
        all_questions = db_questions + [q for q in fallback_questions if q not in db_questions]
    else:
        all_questions = db_questions
    
    # Select random questions
    selected_questions = random.sample(all_questions, min(num_questions, len(all_questions)))
    
    # If user is provided, track which questions they received
    if user and selected_questions:
        # Get question objects for the selected questions
        question_objects = Question.objects.filter(text__in=selected_questions)
        
        # Create a new UserQuestionSet
        question_set = UserQuestionSet.objects.create(
            user=user,
            job_role=role.lower()
        )
        
        # Add questions to the set
        question_set.questions.add(*question_objects)
    
    return selected_questions
