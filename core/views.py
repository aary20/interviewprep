from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import os
import base64
import time
from django.core.files.base import ContentFile
from .forms import AnswerForm, ResumeUploadForm, JobPreferenceForm, FilterForm
from pyresparser import ResumeParser
from .utils.question_generator import generate_questions_based_on_role
from .analysis.grammar_check import check_grammar
from .analysis.keyword_check import check_keywords
from .analysis.score_calculator import calculate_score
from .models import Resume, UserAnswer, Testimonial, JobRole, Question, Answer
from django.contrib.auth.decorators import login_required
from dal import autocomplete
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google.cloud import speech


# Change this function
def home(request):
    return render(request, 'core/home.html', {})


def dashboard(request):
    # Show user-specific answers if authenticated; otherwise, an empty list
    if request.user.is_authenticated:
        user_answers = UserAnswer.objects.filter(user=request.user).order_by('-timestamp')
    else:
        user_answers = UserAnswer.objects.none()

    return render(request, 'core/dashboard.html', {'user_answers': user_answers})


def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register_user')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register_user')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('dashboard')

    return render(request, 'core/register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login_user')

    return render(request, 'core/login.html')


def logout_user(request):
    logout(request)
    return redirect('login_user')


def upload_resume(request):
    # Try to get existing resume for this user
    try:
        resume = Resume.objects.get(user=request.user)
    except (Resume.DoesNotExist, TypeError):
        resume = None

    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # If user already has a resume, update it instead of creating new
            if resume:
                resume.file = request.FILES['file']
                resume.save()
            else:
                resume = form.save(commit=False)
                resume.user = request.user
                resume.save()

            # Redirect to same page to show the preview
            return redirect('upload_resume')
    else:
        form = ResumeUploadForm()

    return render(request, 'core/upload_resume.html', {'form': form, 'resume': resume})


def generate_questions(request):
    questions = []
    job_preference_form = JobPreferenceForm()
    filter_form = FilterForm(request.GET or None)

    if request.method == 'POST':
        job_preference_form = JobPreferenceForm(request.POST)
        if job_preference_form.is_valid():
            selected_role = job_preference_form.cleaned_data['job_role'].title

            # Get difficulty from filter form if it exists
            difficulty = None
            if filter_form.is_valid() and filter_form.cleaned_data.get('difficulty'):
                difficulty = filter_form.cleaned_data.get('difficulty')

            # Generate questions and track for the user
            questions = generate_questions_based_on_role(
                selected_role, 
                num_questions=5, 
                difficulty=difficulty,
            )
            request.session['generated_questions'] = questions
            request.session['current_question_index'] = 0
            return redirect('mock_interview')  # Go to mock interview

    # For GET requests with filter parameters
    elif request.method == 'GET' and filter_form.is_valid() and any(filter_form.cleaned_data.values()):
        # Display filtered questions without redirecting
        job_role = None
        if filter_form.cleaned_data.get('job_role'):
            job_role = filter_form.cleaned_data['job_role'].title

        difficulty = filter_form.cleaned_data.get('difficulty')

        if job_role:
            questions = Question.objects.filter(job_role__iexact=job_role.lower())
            if difficulty:
                questions = questions.filter(difficulty=difficulty)
            questions = list(questions.values_list('text', flat=True))
            # Save to session so mock_interview has data
            request.session['generated_questions'] = questions
            request.session['current_question_index'] = 0

    return render(request, 'core/generate_questions.html', {
        'questions': questions, 
        'job_preference_form': job_preference_form,
        'filter_form': filter_form
    })


def mock_interview(request):
    questions = request.session.get('generated_questions', [])
    if not questions:
        # Fallback defaults so page always shows questions
        questions = [
            "Tell me about your experience with web development.",
            "How do you handle difficult team dynamics?",
            "Describe a challenging project you've worked on.",
            "What are your strengths and weaknesses?",
            "Where do you see yourself in 5 years?",
            "How do you stay updated with the latest technology trends?",
            "Describe a situation where you had to learn a new technology quickly.",
            "How do you handle conflicts in a team?",
            "What's your approach to problem-solving?",
            "Tell me about a time you had to meet a tight deadline."
        ]
        request.session['generated_questions'] = questions
        request.session['current_question_index'] = 0

    total_questions = len(questions)
    current_question_index = request.session.get('current_question_index', 0)

    if current_question_index < total_questions:
        question_text = questions[current_question_index]
        # Try to get the Question object from the database
        try:
            question = Question.objects.get(text=question_text)
        except Question.DoesNotExist:
            # If not found, create a temporary Question object with just the text
            # This handles cases where questions come from QUESTION_BANK and not the database
            class TempQuestion:
                def __init__(self, text):
                    self.id = None
                    self.text = text
            question = TempQuestion(question_text)
    else:
        question = None

    context = {
        'question': question,
        'current_index': current_question_index + 1,
        'total_questions': total_questions,
        'form': AnswerForm()
    }
    return render(request, 'core/mock_interview.html', context)


@login_required
def view_report(request, id):
    answer = UserAnswer.objects.get(id=id, user=request.user)
    return render(request, 'core/report.html', {'answer': answer})


def reports(request):
    return render(request, 'core/reports.html')


EXPECTED_KEYWORDS = ["Python", "Django", "API", "Database", "Authentication"]


@login_required
def analyze_answer(request):
    if request.method == "POST":
        answer = request.POST.get("answer")
        question = request.POST.get("question")  # Pass from form

        grammar_errors, grammar_matches = check_grammar(answer)
        found_keywords, missing_keywords = check_keywords(answer, EXPECTED_KEYWORDS)
        final_score, grammar_score, keyword_score = calculate_score(
            grammar_errors, found_keywords, len(EXPECTED_KEYWORDS)
        )

        # Save to DB
        UserAnswer.objects.create(
            user=request.user,
            question=question,
            answer=answer,
            grammar_errors=grammar_errors,
            grammar_score=grammar_score,
            keyword_score=keyword_score,
            final_score=final_score
        )

        context = {
            'answer': answer,
            'question': question,
            'grammar_errors': grammar_errors,
            'grammar_matches': grammar_matches,
            'found_keywords': found_keywords,
            'missing_keywords': missing_keywords,
            'final_score': final_score,
            'grammar_score': grammar_score,
            'keyword_score': keyword_score,
        }

        return render(request, 'core/feedback.html', context)


def thank_you(request):
    return render(request, 'core/thank_you.html')


class JobRoleAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return JobRole.objects.none()

        qs = JobRole.objects.filter(is_active=True)

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        return qs


@login_required
def submit_answer(request):
    if request.method == 'POST':
        # Get form data
        question_id = request.POST.get('question_id')
        answer_text = request.POST.get('answer_text')
        audio_data = request.POST.get('audio_data')

        try:
            question = Question.objects.get(id=question_id)
            
            # Create a new Answer instance
            answer = Answer(user=request.user, question=question, answer_text=answer_text)
            
            # Process audio data if provided
            if audio_data and audio_data.startswith('data:audio'):
                # Extract the base64 encoded data
                format, audiostr = audio_data.split(';base64,')
                ext = format.split('/')[-1]
                
                # Generate a unique filename
                filename = f"answer_{request.user.id}_{question_id}_{int(time.time())}.{ext}"
                
                # Convert base64 to file and save
                audio_file = ContentFile(base64.b64decode(audiostr), name=filename)
                answer.answer_audio = audio_file
            
            # Save the answer
            answer.save()
            
            # Add success message
            messages.success(request, "Your answer has been submitted successfully!")
            
            # Update session to move to next question
            questions = request.session.get('generated_questions', [])
            current_question_index = request.session.get('current_question_index', 0)
            
            current_question_index += 1
            request.session['current_question_index'] = current_question_index
            
            if current_question_index >= len(questions):
                return redirect('thank_you')
            
            return redirect('mock_interview')
            
        except Question.DoesNotExist:
            messages.error(request, "Question not found. Please try again.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    return redirect('mock_interview')


@csrf_exempt
def transcribe_chunk(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    audio_file = request.FILES.get('audio')
    if not audio_file:
        return JsonResponse({'error': 'Missing audio'}, status=400)

    try:
        client = speech.SpeechClient()
        content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            language_code='en-US',
            enable_automatic_punctuation=True,
            # sample_rate_hertz is optional for compressed formats like opus
        )

        response = client.recognize(config=config, audio=audio)
        text = ' '.join([result.alternatives[0].transcript for result in response.results]).strip()

        return JsonResponse({'text': text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
