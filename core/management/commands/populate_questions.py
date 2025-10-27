from django.core.management.base import BaseCommand
from core.models import Question
from core.utils.question_generator import QUESTION_BANK

class Command(BaseCommand):
    help = 'Populates the database with initial questions'

    def handle(self, *args, **options):
        # Clear existing questions if needed
        # Question.objects.all().delete()
        
        # Count of questions added
        count = 0
        
        # Add questions from QUESTION_BANK
        for role, questions in QUESTION_BANK.items():
            # Assign difficulties in a round-robin fashion
            difficulties = ['Easy', 'Medium', 'Hard']
            
            for i, question_text in enumerate(questions):
                difficulty = difficulties[i % len(difficulties)]
                
                # Check if question already exists
                if not Question.objects.filter(text=question_text, job_role=role).exists():
                    Question.objects.create(
                        job_role=role,
                        text=question_text,
                        difficulty=difficulty
                    )
                    count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added {count} questions to the database'))